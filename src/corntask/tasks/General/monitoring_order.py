
import time
from ....base.taskcatch import catch_exception
if __name__ == '__main__':
    pass
else:
    from ...apscheduler_core import sched

import logging
logger = logging.getLogger(__name__)


class monitoring_order():
    def __init__(self):
        self.__name = monitoring_order.get_name()
        self.cfg = {'cron': '0/2 * * * * * *','desc':'order 执行情况监控',
                    'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/','PROJECT_NO':'General'}

    @staticmethod
    def get_name():
        return "monitoring_order"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *', 'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/'}

    def save_results(self, data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(
                job_name=monitoring_order.get_name(), contents=data)
            session.add(result)
            session.commit()

    def m_order(self):
        #获取活跃任务
        from ...base.models.layer2_pallet_model import PlTask,PlTaskType,PlTaskRelation
        #from ...base.webwmes import reportfinish
        import re
        import json
        from sqlalchemy import select,update

        with sched.SessionFactory() as session:            
            statement = select(PlTask.id,PlTask.task_no,PlTask.task_type,PlTask.status,PlTask.priority,PlTask.ex,PlTaskRelation.relation).outerjoin(PlTaskRelation).filter(PlTask.status.in_(['created','handle','active', 'in_progress'])).order_by(PlTask.id)
            result = session.execute(statement).all()
            session.commit()
        import json
        orderlist=[]
        taskdict = {}
        
        logger.info("获取{}个任务".format(len(result)))
        for row in result:
            if row.relation is None:
                with sched.SessionFactory() as session:
                    statement = select(PlTaskType.task_type,PlTaskType.ts_map).filter_by(task_type=row.task_type)
                    tasktsmap = session.execute(statement).one()
                    session.commit()
                with sched.SessionFactory() as session:
                    statement = select(PlTask.optlist).filter_by(id=row.id)
                    optlist = session.execute(statement).one()
                    session.commit()
                if tasktsmap is None:
                    continue   
                optdict = {}
                idx = 0

                for opt in optlist[0]["optlist"]:
                    idx = idx + 1 
                    optdict[str(idx)] = opt
                order_json = {
                "task_no": row.task_no,
                "priority": row.priority,
                "dead_line": "2020-02-01 16:00:00",
                "ts_name": tasktsmap.ts_map,
                "parameters": json.dumps({"optlist":json.dumps(optdict)}),

                }
                logger.info("开始发送任务（{}）目标点数{}".format(row.task_no,len(optlist[0]["optlist"])))
                from ...base.dispatchapi import sendorder
                redata,recode = sendorder(order_json)
                if recode == 200:
                    if row.id is not None:
                        with sched.SessionFactory() as session:
                            pltaskr = PlTaskRelation(relation = row.task_no,pl_task_id = row.id)
                            session.add(pltaskr)
                            session.commit()
                else:
                    logger.info("任务[{}]重发om失败，稍后继续重发{}".format(row.task_no,redata))
                    break
            else:
                orderlist.append(row.relation)
                taskdict[row.relation] = row


        #获取活跃任务对应的order
        if len(orderlist) == 0:
            return
        #print(str(orderlist).lstrip('[').rstrip(']'))
        sql = 'select * from layer4_1_om.order where order_name in({})'.format(str(orderlist).lstrip('[').rstrip(']'))
        #print(sql)
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            orderinfo = cursor.fetchall()
            session.commit()
        #waiting/active/finish/error/waiting_cancel/cancel_finish/waiting_manually_finish/manually_finish
        #print(orderinfo)
        completelist = []
        logger.info("待处理{}个order".format(len(orderinfo)))
        for row in orderinfo:
            #处理未发送成功的

            if row.status == 'waiting' or row.status == 'waiting_manually_finish' or row.status == 'waiting_cancel':
                pass
            elif row.status == 'active':
                with sched.SessionFactory() as session:
                        stmt = update(PlTask).where(PlTask.task_no == row.order_name).values(
                            status='active').execution_options(synchronize_session="fetch")
                        session.execute(stmt)
                        session.commit()
            elif row.status == 'finish' or row.status == 'manually_finish':

                with sched.SessionFactory() as session:
                    stmt = update(PlTask).where(PlTask.task_no == row.order_name).values(
                        status='completed').execution_options(synchronize_session="fetch")
                    session.execute(stmt)
                    session.commit()
                pos = re.sub('\(.*?\)','',row.current_destination)
                #print(PlTask.ex)
                data ={"TaskId":row.order_name,"UserId":"monitoring_order","ToLoc":pos,"ex":json.loads(taskdict[row.order_name].ex),"IP":"","ClientName":""}
                completelist.append(data)
                logger.info("任务[{}]已经完成，完成状态[{}],完成车辆[{}]".format(row.order_name,row.status,str(row.agv_list)))

            elif row.status == 'error':
                with sched.SessionFactory() as session:
                    stmt = update(PlTask).where(PlTask.task_no == row.order_name).values(
                        status='error').execution_options(synchronize_session="fetch")
                    session.execute(stmt)
                    session.commit()
                print('错误')
                logger.info("任务[{}]执行错误,车辆[{}]".format(row.order_name,str(row.agv_list)))

            else:
                logger.info("任务编号为[{}]的任务状态[{}]不存在".format(row.order_name, row.status))
    # @catch_exception
    def run(self):
        try:
            logger.debug("一轮定时任务开始")
            self.m_order()
            logger.debug("一轮定时任务结束")
        except (Exception) as e:
            logger.error("推送wms任务完成异常{}".format(str(e)))
            pass
 
               
    def deal(self, e):
        #self.save_results({"error": str(e)})
        logger.error("定时任务异常（{}）".format(str(e)))  


if __name__ == '__main__':
    do  = monitoring_order()
    do.run()