import os
import importlib
import inspect
import sys
from datetime import datetime
import time
import json
#from flask_apscheduler import APScheduler
from pytz import utc, timezone
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_SCHEDULER_SHUTDOWN  # 调度器事件类型
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging
logger = logging.getLogger("apscheduler")

def datetime2str(dt):
    if dt:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return ''

# 监听根据event.code判断，参考文档Event codes


def job_run_listener(event):
    if event.code == EVENT_SCHEDULER_SHUTDOWN:
        logger.error('监听-> 调度器关闭')
    else:
        # print(event.job_id, event.scheduled_run_time)
        job_id = event.job_id

        scheduled_run_time = datetime2str(event.scheduled_run_time)
        if event.exception:
            logger.error('监听-> 作业ID：{} 在 {} 执行失败 :(错误原因：{}'.format(job_id,
                  scheduled_run_time, event.exception.args[0]))
        else:
            logger.info('监听({})-> 作业ID：{} 在 {} 执行成功 :)'.format(event.code,job_id, scheduled_run_time))
            
            
        


def run_scheduler():
    """
    使用SQLAlchemyJobStore，需要pip install sqlalchemy，否则会提示ImportError: SQLAlchemyJobStore requires SQLAlchemy installed
    """
    # 配置作业存储器
    # redis_store = RedisJobStore(host='192.168.1.100', port='6379', db=0)
    # mysql_store = SQLAlchemyJobStore(url='mysql+pymysql://root:password@192.168.1.100:3306/apscheduler_db?charset=utf8')
    # postgres_store = SQLAlchemyJobStore(url='postgresql://postgres:postgres@192.168.1.100:5432')
    jobstores = {
        # 会自动在当前目录创建该sqlite文件
        'default': SQLAlchemyJobStore(url='sqlite:///apscheduler_db.sqlite')
    }

    # 配置执行器，并设置线程数
    executors = {
        'default': ThreadPoolExecutor(max_workers=20)  # 派生线程的最大数目
    }

    job_defaults = {
        'coalesce': False,  # 累计的作业是否执行。True不执行，False,执行。比如进场挂了，导致任务多次没有调用，则前几次的累计任务的任务是否执行的策略。
        'max_instances': 1  # 同一个任务在线程池中最多跑的实例数
    }

    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors,
                                    job_defaults=job_defaults, timezone=timezone('Asia/Shanghai'))
    # scheduler = BlockingScheduler()
    #scheduler = APScheduler()
    scheduler.start()

    # 当任务执行完或任务出错时，调用job_run_listener
    scheduler.add_listener(job_run_listener, EVENT_JOB_EXECUTED |
                           EVENT_JOB_ERROR | EVENT_SCHEDULER_SHUTDOWN)
    return scheduler


class SchedulerManage(object):
    def __init__(self, sch, jobstore='default'):
        self.sch = sch
        self.jobstore = jobstore
#        from ..app import create_app
        from ..settings import Database,Scheduler
        #self.engine = create_engine('postgresql://postgres:admin@127.0.0.1:5432/longji0628')
        self.engine = create_engine(Database.postgresql.DB_URI, echo=True)
        self.SessionFactory = sessionmaker(bind=self.engine)
        

    # 暂停作业
    def pause_job(self, job_id):
        flg = True
        try:
            self.sch.pause_job(job_id, jobstore=self.jobstore)
            msg = '暂停-> 作业ID：{} 暂停成功，暂停时间：{}'.format(
                job_id, datetime2str(datetime.now()))
            flg = True
        except JobLookupError as e:
            msg = '暂停-> 作业ID：{}不存在：{}'.format(job_id, e)
            flg = False
        logger.info(msg)
        return flg,msg

    # 恢复作业，或在作业完成后（下次运行时间为None）删除作业
    def resume_job(self, job_id):
        flg = False
        try:
            self.sch.resume_job(job_id, jobstore=self.jobstore)
            msg = '恢复-> 作业ID：{} 恢复成功，恢复时间：{}，恢复后将在 {} 执行'.format(job_id, datetime2str(
                datetime.now()), self.get_job(job_id).get('next_run_time'))
            flg = True
        except JobLookupError as e:
            msg = '恢复-> 作业ID：{}不存在：{}'.format(job_id, e)
            flg = False
        logger.info(msg)
        return flg,msg

    # 删除作业
    def remove_job(self, job_id=None):
        flg = False
        if job_id is None:
            self.sch.remove_all_jobs(jobstore=self.jobstore)
            msg = '删除-> 所有作业删除成功'
            flg = True
        else:
            try:
                self.sch.remove_job(job_id, jobstore=self.jobstore)
                msg = '删除-> 作业ID：{} 删除成功，删除时间：{}'.format(
                    job_id, datetime2str(datetime.now()))
                flg = True
            except JobLookupError as e:
                msg = '删除-> 作业ID：{}不存在：{}'.format(job_id, e)
                flg = False
        logger.info(msg)
        return flg,msg

    # 获取作业的触发器和配置的时间字符串，以及作业下次运行时间等信息
    def get_job(self, job_id):
        """
        获取作业的所有信息
        :param job_id: 作业ID
        :return: id、name、func、func_args、func_kwargs、trigger、trigger_time、state、next_run_time
        """
        job = self.sch.get_job(job_id, self.jobstore)
        if job is None:
            return None

        job_info = dict()
        job_info['id'] = job.id
        job_info['name'] = job.name
        job_info['func'] = job.func.__name__
        #job_info['func_args'] = job.args
        job_info['func_kwargs'] = job.kwargs

        if isinstance(job.trigger, DateTrigger):
            job_info['trigger'] = 'date'
            job_info['trigger_time'] = datetime2str(job.trigger.run_date)
        elif isinstance(job.trigger, IntervalTrigger):
            job_info['trigger'] = 'interval'
            # print(job.trigger.interval.days)
            w, d = divmod(job.trigger.interval.days, 7)  # 天转换为周、天
            # print(job.trigger.interval.seconds)
            m, s = divmod(job.trigger.interval.seconds, 60)  # 秒转换为时、分、秒
            h, m = divmod(m, 60)
            job_info['trigger_time'] = '{} {} {} {} {}'.format(s, m, h, d, w)
            job_info['start_date'] = datetime2str(job.trigger.start_date)
            job_info['end_date'] = datetime2str(job.trigger.end_date)
        elif isinstance(job.trigger, CronTrigger):
            job_info['trigger'] = 'cron'
            job_info['trigger_time'] = '{} {} {} {} {} {} {}'.format(job.trigger.fields[7],
                                                                     job.trigger.fields[6],
                                                                     job.trigger.fields[5],
                                                                     job.trigger.fields[4],
                                                                     job.trigger.fields[3],
                                                                     job.trigger.fields[2],
                                                                     job.trigger.fields[1])
            job_info['start_date'] = datetime2str(job.trigger.start_date)
            job_info['end_date'] = datetime2str(job.trigger.end_date)
        else:
            job_info['trigger'] = job_info['trigger_time'] = None
        next_run_time = job.next_run_time
        if next_run_time:
            # 作业运行中
            job_info['state'] = '运行中'
            job_info['next_run_time'] = datetime2str(next_run_time)
        else:
            # 作业暂停中，next_run_time为None，进行获取
            job_info['state'] = '暂停中'
            job_info['next_run_time'] = '{}(恢复运行后)'.format(datetime2str(
                job.trigger.get_next_fire_time(None, datetime.now(timezone('Asia/Shanghai')))))
        # print(job_info)
        return job_info

    # 获取所有作业
    def get_jobs(self):
        all_jobs = self.sch.get_jobs()
        job_infos = []
        for job in all_jobs:
            job_infos.append(self.get_job(job.id))
        return json.dumps(job_infos)

    # 处理add、modify传入的kwargs：触发器时间字符串->触发器时间参数
    @staticmethod
    def trigger_time2trigger_args(trigger, trigger_time, start_date=None, end_date=None):
        """
        根据触发器别名str，将触发时间字符串转触发器时间参数
        :param trigger: 触发器别名str
        :param trigger_time: 触发时间str
        :param start_date: （str）interval和cron的开始时间
        :param end_date: （str）interval和cron的结束时间
        :return: 触发时间的dict
        """
        kwargs = {}
        if trigger == 'date':
            kwargs['run_date'] = trigger_time
        elif trigger == 'interval':
            """
            :param int weeks: number of weeks to wait
            :param int days: number of days to wait
            :param int hours: number of hours to wait
            :param int minutes: number of minutes to wait
            :param int seconds: number of seconds to wait
            """
            kwargs['seconds'], kwargs['minutes'], kwargs['hours'], kwargs['days'], kwargs['weeks'] = map(
                int, trigger_time.split(' '))
        elif trigger == 'cron':
            """
            :param int|str year: 4-digit year
            :param int|str month: month (1-12)
            :param int|str day: day of the (1-31)
            :param int|str day_of_week: number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
            :param int|str hour: hour (0-23)
            :param int|str minute: minute (0-59)
            :param int|str second: second (0-59)
            """
            kwargs['second'], kwargs['minute'], kwargs['hour'], kwargs['day'], kwargs[
                'month'], kwargs['day_of_week'], kwargs['year'] = trigger_time.split(' ')
        else:
            pass
        # 添加起止日期
        if trigger != 'date':
            if start_date:
                kwargs['start_date'] = start_date
            if end_date:
                kwargs['end_date'] = end_date
        return kwargs


    @staticmethod
    def trigger_time2trigger(trigger, trigger_time, start_date=None, end_date=None):
        ct = None
        """
        根据触发器别名str，将触发时间字符串转触发器时间参数
        :param trigger: 触发器别名str
        :param trigger_time: 触发时间str
        :param start_date: （str）interval和cron的开始时间
        :param end_date: （str）interval和cron的结束时间
        :return: 触发时间的dict
        """
        kwargs = {}
        if trigger == 'date':
            kwargs['run_date'] = trigger_time
    # 添加作业
        elif trigger == 'interval':
            """
            :param int weeks: number of weeks to wait
            :param int days: number of days to wait
            :param int hours: number of hours to wait
            :param int minutes: number of minutes to wait
            :param int seconds: number of seconds to wait
            """
            kwargs['seconds'], kwargs['minutes'], kwargs['hours'], kwargs['days'], kwargs['weeks'] = map(
                int, trigger_time.split(' '))
        elif trigger == 'cron':
            """
            :param int|str year: 4-digit year
            :param int|str month: month (1-12)
            :param int|str day: day of the (1-31)
            :param int|str day_of_week: number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
            :param int|str hour: hour (0-23)
            :param int|str minute: minute (0-59)
            :param int|str second: second (0-59)
            """
            kwargs['second'], kwargs['minute'], kwargs['hour'], kwargs['day'], kwargs[
                'month'], kwargs['day_of_week'], kwargs['year'] = trigger_time.split(' ')
            ct = CronTrigger(year=kwargs['year'], month=kwargs['month'], day=kwargs['day'], day_of_week=kwargs['day_of_week'], hour=kwargs['hour'], minute=kwargs['minute'], second=kwargs['second'])
        else:
            pass
        # 添加起止日期
        if trigger != 'date':
            if start_date:
                kwargs['start_date'] = start_date
            if end_date:
                kwargs['end_date'] = end_date
        return ct
    # 添加作业
    def add_job(self, func, trigger, trigger_time, job_id=None, func_args=None, func_kwargs=None, start_date=None, end_date=None):
        """
        date:
            .add_job(job_function, 'date', args=['msg'], run_date='2020-02-20 12:12:00')
        interval:
            .add_job(job_function, 'interval', hours=2, start_date='2020-02-20 12:12:00', end_date='2020-02-22 12:12:00')
        cron:
            .add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')

        :param func: 执行的函数名
        :param trigger: （str）触发器类型：date、interval、cron
        :param trigger_time: （str）执行时间信息：
                            date->'2020-02-20 12:12:00'
                            interval->'秒 分 时 日 周'：每2s（2 0 0 0 0），每1天12小时（0 0 12 1 0），每1周（0 0 0 0 1）
                            cron->'秒 分 时 日 月 周 年'：每日xx:xx:00（0 x x * * * *）、每周x（0 x x * * x *）、每月x日（0 x x x * * *）、每年x月x日（0 x x x x * *）
        :param func_args: (tuple|list)要调用func的参数list
        :param func_kwargs: (dict)调用func的关键字参数dict
        :param start_date: （str）interval和cron的开始时间，格式为：xxxx-xx-xx xx:xx:xx
        :param end_date: （str）interval和cron的结束时间
        :return: job_id
        """
        if job_id is None:
            import random
            random_num = random.randint(100, 999)
            job_id = '{}_{}_{}'.format(trigger, int(
                time.time()), random_num)  # 时间戳+随机数为id
            job_name = '{}_{}'.format(func.__name__, random_num)
        job_name = job_id

        prejob = self.get_job(job_id)
        if prejob is not None:
            logger.info('创建-> 已存在任务，如果需要修改参数，请调用修改接口！')
            return prejob["id"]
        add_kwargs = {'func': func, 'trigger': trigger, 'args': func_args,
                      'kwargs': func_kwargs, 'id': job_id, 'name': job_name}  # 指定添加作业的参数
        triggerptr = self.trigger_time2trigger_args(
            trigger=trigger, trigger_time=trigger_time, start_date=start_date, end_date=end_date)
        add_kwargs.update(triggerptr)  # 将触发器时间参数合并
        logger.info(add_kwargs)
        
        # print(add_kwargs)
        if trigger in ('date', 'interval', 'cron'):
            try:
                """
                add_job()
                    'func': '函数名', 
                    'trigger': '触发器别名', 
                    'args': '函数参数', 
                    'func_kwargs': '函数参数',
                    'id': '作业ID',
                    'name': '作业名称',
                    '**trigger_args': 触发器时间参数，trigger_time字符串转换来，
                    jobstore='default'：指定存储器名称
                    executor='default'：指定执行器名称
                    另外还有3个参数：
                    misfire_grace_time=undefined：如果一个job本来14:00有一次执行，但是由于某种原因没有被调度上，现在14:01了，这个14:00的运行实例被提交时，
                        会检查它预订运行的时间和当下时间的差值（这里是1分钟），大于我们设置的30秒限制，那么这个运行实例不会被执行。
                    coalesce=undefined：最常见的情形是scheduler被shutdown后重启，某个任务会积攒了好几次没执行，
                        如5次，下次这个job被submit给executor时，执行5次。将coalesce=True后，只会执行一次
                    replace_existing=False：如果在程序初始化时，是从数据库读取任务的，那么必须为每个任务定义一个明确的ID，
                        并且使用replace_existing=True，否则每次重启程序，你都会得到一份新的任务拷贝，也就意味着任务的状态不会保存。
                """
                print(self.sch.add_job)
                #job = self.sch.add_job(**add_kwargs)
                #bb = CronTrigger(second='1/3')
                bb = self.trigger_time2trigger(trigger=trigger, trigger_time=trigger_time, start_date=start_date, end_date=end_date)
                job = self.sch.add_job(func =add_kwargs["func"],trigger=bb,id =add_kwargs["id"], name = job_name,coalesce=True,replace_existing=True,misfire_grace_time = None)

                logger.info('创建-> 当前新建任务{}：'.format(job.id) )
                # 获取当前创建作业的下次运行时间
                # next_run_time = scheduler.get_job(job_id).next_run_time
                # <class 'datetime.datetime'>offset-aware类型，包含时区的
                next_run_time = job.next_run_time
                # offset-aware类型的datetime转换为offset-naive类型的datetime，即去掉时间戳
                next_run_time = next_run_time.replace(tzinfo=None)

                now_datetime = datetime.now()  # 获取当前时间
                if next_run_time <= now_datetime:
                    logger.error('创建-> 任务时间需大于当前时间，任务已被系统自动删除，创建失败！')
                else:
                    week = {
                        '0': '日',
                        '1': '一',
                        '2': '二',
                        '3': '三',
                        '4': '四',
                        '5': '五',
                        '6': '六',
                    }
                    logger.info('创建-> 定时任务创建成功，job_id：{}，下次运行时间：{}（周{}）'.format(job_id,
                          next_run_time, week[next_run_time.strftime('%w')]))
            except ValueError as e:
                logger.error('创建-> 异常：', e)
            return job.id
        else:
            logger.error('创建-> 创建失败，指定触发器错误')
            return None

    # 修改作业
    def modify_job(self, job_id, trigger=None, trigger_time=None, name=None, func=None, func_args=None, func_kwargs=None, start_date=None, end_date=None, reschedule=True):
        """
        可以修改任务当中除了id的任何属性
        :param job_id:
        :param trigger:
        :param trigger_time:
        :param name: （str） - 此作业的描述
        :param func: 可执行的调用函数
        :param func_args: （tuple|list） - 可调用位置参数
        :param func_kwargs: （dict） - 可调用的关键字参数
        :param start_date: （str）interval和cron的开始时间
        :param end_date: （str）interval和cron的结束时间
        :param reschedule: 是否重新计算时间
        :return:
        """
        changes = {'job_id': job_id, 'jobstore': self.jobstore}
        if trigger and trigger_time:
            # if trigger == 'date':
            #     trigger_obj = DateTrigger(**self.trigger_time2trigger_args(trigger, trigger_time))
            # elif trigger == 'interval':
            #     trigger_obj = IntervalTrigger(**self.trigger_time2trigger_args(trigger, trigger_time))
            # elif trigger == 'cron':
            #     trigger_obj = CronTrigger(**self.trigger_time2trigger_args(trigger, trigger_time))
            # else:
            #     trigger_obj = None
            # print(trigger_obj)
            trigger_obj_dict = {  # 构建触发器别名和对象字典
                'date': DateTrigger,
                'interval': IntervalTrigger,
                'cron': CronTrigger
            }
            # 传入触发器时间参数，返回dict，在进行触发器实例化得到新触发器对象
            trigger_obj = trigger_obj_dict[trigger](
                **self.trigger_time2trigger_args(trigger, trigger_time, start_date, end_date))
            print('修改-> 原计划，下次运行时间：{}'.format(self.get_job(job_id).get('next_run_time')))
            changes['trigger'] = trigger_obj
        if name:
            changes['name'] = name
        if func:
            changes['func'] = func
        if func_args:
            changes['args'] = func_args
        if func_kwargs:
            changes['kwargs'] = func_kwargs

        # print(changes)
        # 执行修改
        self.sch.modify_job(**changes)
        if reschedule and trigger and trigger_time:
            # 修改触发器时间参数后，重新计算下次运行时间，即按照新的触发时间执行下一次作业
            self.sch.reschedule_job(
                job_id=job_id, jobstore=self.jobstore, trigger=changes['trigger'])
        logger.info('修改-> 修改触发器时间后，下次运行时间：{}'.format(self.get_job(job_id).get('next_run_time')))
        return job_id

    # 退出
    def shutdown(self):
        self.sch.shutdown()

# 实例化
sched = SchedulerManage(run_scheduler())