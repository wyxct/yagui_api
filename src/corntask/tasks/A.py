
import time
#from ...base.taskcatch import catch_exception
from ..apscheduler_core import sched
import logging
logger = logging.getLogger(__name__)
class A_job():
    def __init__(self):
        self.__name =  A_job.get_name()
        self.cfg = A_job.get_cfg()
    @staticmethod      
    def get_name():
        return "A_job"
    @staticmethod      
    def get_cfg():
        return {'corn' :'0/1 * * * * * *'}
    #@catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        print(self.__name ,' job A_job running',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        logger.info('job A_job running {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
        time.sleep(6)
    
    def deal(self,e):
        from sqlalchemy.orm import Session
        from ...base.models.public_model import CronTaskResult  
        import json
        with sched.SessionFactory() as session:
            result = CronTaskResult(job_name = A_job.get_name(),contents = {"error":str(e)})
            session.add(result)
            session.commit() 
