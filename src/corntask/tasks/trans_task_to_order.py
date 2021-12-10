
import time
#from ...base.taskcatch import catch_exception
from ..apscheduler_core import sched

class trans_task_to_order():
    def __init__(self):
        self.__name = trans_task_to_order.get_name()
        self.cfg = {'cron' :'0/2 * * * * * *','disurl':'http://127.0.0.1:2000/api/om/order/'}
    @staticmethod      
    def get_name():
        return "trans_task_to_order"
    @staticmethod      
    def get_cfg():
        return {'cron' :'0/2 * * * * * *','disurl':'http://127.0.0.1:2000/api/om/order/'}
    def save_results(self,data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(job_name = trans_task_to_order.get_name(),contents = data )
            session.add(result)
            session.commit() 
    
    #@catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        print(self.__name ,' trans_task_to_order running',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        
        from ...base.models.layer2_pallet_model import PlTask
        from sqlalchemy import select,update
        result = None
        with sched.SessionFactory() as session:
            #result = session.query(ObjectTask).filter_by(keep_object_bound = None).all()
            from sqlalchemy import and_
            statement = select(PlTask.id, PlTask.to_pos, PlTask.from_pos).filter(and_(PlTask.status == '10' ,PlTask.task_type == 'P2P'))
            #result = session.execute(statement).all()
            #statement = select(ObjectTask.object_id, ObjectTask.id,Object.object_name)
            result = session.execute(statement).all()
            session.commit() 

        order_json = {
        "order_name": "P2PTask",
        "priority": 1,
        "dead_line": "2020-02-01 16:00:00",
        "ts_name": "P2P_test",
        "parameters": "{\"agv_type\":4,\"dst\":None,\"src\":None}",
        "uid":None
        }
        result_data ={"order":[]}
        import requests
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
         }

        for row in result:
            order_json['order_name'] = 'P2PTask_' + str(row.id)
            prt = json.dumps({'agv_type':4, 'dst':row.to_pos, 'scr':row.from_pos})
            order_json["parameters"] = prt
            order_json["uid"] = row.id
            print(order_json)
            response = requests.request("POST", self.cfg['disurl'], json=order_json, headers=headers)
            print(response.status_code)
            print(response.text)
            if response.status_code == 200:

                with sched.SessionFactory() as session:
                    stmt = update(PlTask).where(PlTask.id == row.id).values(status = '30').execution_options(synchronize_session="fetch")
                    session.execute(stmt)
                    session.commit()
                result_data["order"].append(order_json)
                   
        self.save_results(result_data)

        
    
    def deal(self,e):
        self.save_results({"error":str(e)})

    
