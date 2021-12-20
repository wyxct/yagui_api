
import time
#from ....base.taskcatch import catch_exception
from ...apscheduler_core import sched

class trans_task_to_object():
    def __init__(self):
        self.__name = trans_task_to_object.get_name()
        self.cfg = {'cron' :'0/2 * * * * * *','disurl':'http://127.0.0.1:2000/api/om/order/','PROJECT_NO':'General'}
    @staticmethod      
    def get_name():
        return "trans_task_to_object"
    @staticmethod      
    def get_cfg():
        return {'cron' :'0/2 * * * * * *','disurl':'http://127.0.0.1:2000/api/om/order/'}
    def save_results(self,data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(job_name = trans_task_to_object.get_name(),contents = data )
            session.add(result)
            session.commit() 
    
    #@catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        print(self.__name ,' trans_task_to_object running',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        
        from ...base.models.layer2_pallet_model import ObjectTask,PlTask,Object,Location,ObjectLocation
        from sqlalchemy import select,update,insert
        result = None
        with sched.SessionFactory() as session:
            from sqlalchemy import and_
            statement = select(PlTask.id,PlTask.to_pos, PlTask.cid).filter(and_(PlTask.status == '10' ,PlTask.task_type == 'P2A'))
            result = session.execute(statement).all()
            session.commit()

        # order_json = {
        #     "order_name": "trans_task_to_object",
        #     "priority": 2,
        #     "dead_line": "2020-02-01 16:00:00",
        #     "parameters": "{\"object_id\":None,\"to_pos\":None}",
        #     "uid": None
        # }
        # result_data = {"order": []}

        for row in result:
            with sched.SessionFactory() as session:
                object_statement = select(Object).filter_by(object_name = row.cid)
                object_result = session.execute(object_statement).first()[0]
                # session.commit()

                location_statement = select(Location).filter_by(location_name=row.to_pos)
                location_result = session.execute(location_statement).first()[0]
                # session.commit()

                statement = insert(ObjectTask).values(task_type_id = 1, object_id = object_result.id, status_id = 1, destination_location_id = location_result.id, created_user = 'DBAI')
                session.execute(statement).all()
                stmt = update(PlTask).where(PlTask.id == row.id).values(status='30').execution_options(synchronize_session="fetch")
                session.execute(stmt)
                session.commit()

        with sched.SessionFactory() as session:
            object_task_statement = select(ObjectTask.id, ObjectTask.object_id).filter_by(status_id=1).order_by(ObjectTask.task_priority)
            object_task_result = session.execute(object_task_statement).all()
            # session.commit()

            for row in object_task_result:
                object_location_statement = select(ObjectLocation).filter_by(object_id = row.object_id)
                object_location_result = session.execute(object_location_statement).first()[0]
                # session.commit()

                if object_location_result.current_object_task_id is None:
                    stmt = update(ObjectLocation).where(ObjectLocation.object_id == row.object_id, last_updated_user = 'cron').values(current_object_task_id = row.id)
                    session.execute(stmt)
                    stmt = update(ObjectTask).where(ObjectTask.object_id == row.object_id).values(status_id=2).execution_options(synchronize_session="fetch")
                    session.execute(stmt)
                    session.commit()

                    # order_json["parameters"] = json.dumps({'object_id':row.object_id})

        # result_data["order"].append(row)
        # self.save_results(result_data)

        
    
    def deal(self,e):
        self.save_results({"error":str(e)})

    
