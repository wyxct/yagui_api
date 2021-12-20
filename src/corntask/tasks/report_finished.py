
import time
#from ...base.taskcatch import catch_exception
if __name__ == '__main__':
    pass
else:
    from ..apscheduler_core import sched

import logging
logger = logging.getLogger(__name__)


class report_finished():
    def __init__(self):
        self.__name = report_finished.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/'}

    @staticmethod
    def get_name():
        return "report_finished"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *', 'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/'}

    def save_results(self, data):
        logger.error("异常{}".format(data["error"]))
        '''
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(
                job_name=monitoring_e_port.get_name(), contents=data)
            session.add(result)
            session.commit()
        '''
    def report(self):
         #获取活跃任务
        from ...base.models.layer2_pallet_model import PlTask,PlTaskType,PlTaskRelation,PlTaskReport
        from ...base.webwmes import reportfinish
        import re
        import json
        from sqlalchemy import select,update,exists

        with sched.SessionFactory() as session:            
            statement = select(PlTask.id,PlTask.task_no,PlTask.task_type,PlTask.status,PlTask.priority,PlTask.ex,PlTaskRelation.relation).filter(~exists().where(PlTaskReport.pl_task_id == PlTask.id),PlTask.source =='iwms').join(PlTaskRelation).filter(PlTask.status.in_(['completed']))
            result = session.execute(statement).all()
            session.commit()
        import json
        orderlist=[]
        taskdict = {}
        
        logger.info("获取{}个任务".format(len(result)))
        for row in result:
            orderlist.append(row.relation)
            taskdict[row.relation] = row


        #获取活跃任务对应的order
        if len(orderlist) == 0: 
            return

        sql = 'select * from layer4_1_om.order where order_name in({})'.format(str(orderlist).lstrip('[').rstrip(']'))
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            orderinfo = cursor.fetchall()
            session.commit()
        #waiting/active/finish/error/waiting_cancel/cancel_finish/waiting_manually_finish/manually_finish

        logger.info("待处理{}个order".format(len(orderinfo)))
        for row in orderinfo:
            completelist = []
            #处理未发送成功的
            pos = re.sub('\(.*?\)','',row.current_destination)
            data ={"TaskId":row.order_name,"UserId":"monitoring_order","ToLoc":pos,"ex":json.loads(taskdict[row.order_name].ex) if taskdict[row.order_name].ex is not None else None,"IP":"","ClientName":""}
            completelist.append(data)
  
            logger.info({"data":completelist})
            logger.info("任务号（{}）目的地({}) 已经上报".format(row.order_name,pos))
            rst,code = reportfinish({"data":completelist})

            if code == 200 and  rst["MSG_TYPE"] != 'E':
                with sched.SessionFactory() as session:
                    result = PlTaskReport(
                        pl_task_id=taskdict[row.order_name].id)
                    session.add(result)
                    session.commit()

            else:
                logger.info("上报异常（{}）下次重新上报".format(rst["MSG_TXT"]))    
    #@catch_exception
    def run(self):
        try:
            logger.debug("一轮定时任务开始")
            self.report()
            logger.debug("一轮定时任务结束")

        except (Exception) as e:
            logger.error("推送wms任务完成异常{}".format(str(e)))
            pass
 

               
    def deal(self, e):
        #self.save_results({"error": str(e)})
        logger.error("定时任务异常（{}）".format(str(e)))  


if __name__ == '__main__':
    do  = report_finished()
    do.run()