import time
# from ...base.taskcatch import catch_exception
from ...corntask.apscheduler_core import sched
import logging

logger = logging.getLogger(__name__)


class A_job():
    def __init__(self):
        self.__name = A_job.get_name()
        self.cfg = {'cron': '0/2 * * * * * *', 'desc': '测试用例',
                    'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/','PROJECT_NO':'QLSH0001' }

    @staticmethod
    def get_name():
        return "test2"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *', 'desc': '测试用例',
                'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/', }

    # @catch_exception
    def run(self):
        # from ...base.models.public_model import db,CronTaskResult
        import json
        print(self.__name, ' job test2 running', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logger.info('job test2 running {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        time.sleep(6)

    def deal(self, e):
        from sqlalchemy.orm import Session
        from ....base.models.public_model import CronTaskResult
        import json
        with sched.SessionFactory() as session:
            result = CronTaskResult(job_name=A_job.get_name(), contents={"error": str(e)})
            session.add(result)
            session.commit()
