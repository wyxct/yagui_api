
import time
if __name__ == '__main__':
    pass
else:
    from ..apscheduler_core import sched
from ...pltask.orderm import createoder
import logging
logger = logging.getLogger(__name__)


class create_task_QLSH():
    def __init__(self):
        self.__name = create_task_QLSH.get_name()
        self.cfg = {'cron': '0/2 * * * * * *','desc':"齐鲁石化空托仓呼叫任务"}

    @staticmethod
    def get_name():
        return "create_task_QLSH"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *','desc':"齐鲁石化空托仓呼叫任务"}
        
    def save_results(self, data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(
                job_name=create_task_QLSH.get_name(), contents=data)
            session.add(result)
            session.commit()

    def get_put_info(self,loc):
        sql = 'select id,status from pl_task where source =\'self\' and to_pos = \'{}\' and client_name=\'{}\' order by id desc limit 1'.format(loc,self.get_name())
        try:
            with sched.SessionFactory() as session:            
                cursor = session.execute(sql)
                task_status = cursor.fetchall()
                session.commit()
        except (Exception) as e:
            logger.error("数据库操作异常{}".format(str(e)))
            return False


        if task_status is None or len(task_status) ==0 or task_status[0] != 'completed':
            return False  

        sql = 'update layer2_pallet.location_object set object_put_type = 1,last_updated_timestamp = now() where location_name =\'{}\''.format(loc)
        try:
            with sched.SessionFactory() as session:            
                cursor2 = session.execute(sql)
                session.commit()
        except (Exception) as e:
            logger.error("数据库操作异常{}".format(str(e)))
            return False        
        return True
    
    def create_order(self,src,dst):
        '''
        pltask_json: {'task_no': 'TSJ21800121111100010368', 'task_type': 'mp', 'priority': 0, 'status': 'created', 'ex': {'TaskType': 'SJ'}, 'optlist': [{'pos': 'B01-Z1-02-01-01', 'opt': 'load', 'i_flag': 0}, {'pos': 'B01-C1-01-09-01', 'opt': 'unload', 'i_flag': 0}]}
        '''
        from ...base.models.layer2_pallet_model import PlTask,PlTaskType,PlTaskRelation
        from sqlalchemy import select,exists
        import json
        start = time.time()
        timeArray = time.localtime(start)
        timesn = time.strftime("C%Y%m%d%H%M%S",timeArray)
        print(timesn)
        pltaskd = {'task_no':timesn,'task_type': 'pp','priority': 0, 'status': 'created','source':'self','client_name':self.get_name(),
        'optlist': [{'pos': src, 'opt': 'load', 'i_flag': 0}, {'pos': dst, 'opt': 'unload', 'i_flag': 0}]}
        
        
        try:
            with sched.SessionFactory() as session:      
                statement = select(PlTaskType.task_type,PlTaskType.ts_map).filter_by(task_type = 'mp')      
                tasktsmap = session.execute(statement).all()
                session.commit()     

            if tasktsmap is None:
                return {"error":"不存在的类型"}, 400
  
        except (Exception) as e:
            logger.error(str(e))
            return {"error":"数据库异常，请联系相关人员"},500
        
        optdict = {}
        idx = 0
        for row in pltaskd["optlist"]:
            idx = idx + 1 
            optdict[str(idx)] = row

        order_json = {
        "task_no": pltaskd["task_no"],
        "priority": pltaskd["priority"],
        "dead_line": "2020-02-01 16:00:00",
        "ts_name": tasktsmap[0].ts_map,
        "parameters": json.dumps({"optlist":json.dumps(optdict)}),
        "uid":hash(timesn)
        }
        from ...base.dispatchapi import sendorder

        redata,recode = sendorder(order_json)

        if recode != 200:
            #order_id = json.loads(response.text)["data"]
            try:
                sql = 'update layer2_pallet.location_object set object_put_type = 0,last_updated_timestamp = now() where location_name =\'{}\''.format(dst)
                task = PlTask()
                task.task_no = pltaskd["task_no"]
                task.task_type = pltaskd["task_type"]
                task.to_pos = dst
                task.source = pltaskd["source"]
                task.client_name = pltaskd["client_name"]
                task.optlist = {"optlist":pltaskd["optlist"]}
                task.ex = None if "ex" not in pltaskd else json.dumps(pltaskd["ex"])
                task.status = "created" if "status" not in pltaskd else pltaskd["status"]
                task.priority = 0 if "priority" not in pltaskd else pltaskd["priority"]
                with sched.SessionFactory() as session:      
                    session.add(task)
                    cursor = session.execute(sql)
                    session.commit()
                    session.flush()  

                if task.id is not None:                    
                    pltaskr = PlTaskRelation(relation = pltaskd["task_no"],pl_task_id = task.id)
                    with sched.SessionFactory() as session:      
                        session.add(pltaskr)
                        session.commit()
                        session.flush()  

            except (Exception) as e:
                 logger.error(str(e))
                 pass 


    
    def main(self):
        from ...modbus import get_data_need_pallet
        #'LC-07-07-01'输送线,'LC-10-01-01' 空托仓
        unload_pallet = 'LC-10-01-01'
        load_pallet = 'LC-07-07-01'
        sql = 'SELECT object_put_type, location_name FROM layer2_pallet.location_object where opt_condition = \'modbus\' and location_name in(\'{}\')'.format(unload_pallet)
        sql2 = 'select id from pl_task where source =\'self\' and status in(\'created\', \'in_progress\' ) and to_pos = \'{}\' and \'client_name\'=\'{}\''.format(unload_pallet,self.get_name())
        
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            write_status = cursor.fetchall()
            cursor2 = session.execute(sql2)
            task_status = cursor2.fetchall()
            session.commit()

        if write_status is not None and len(write_status) != 0:
            row = write_status[0]
            #有的时候去读信号
            if row.object_put_type == 1:
                flg ,data = get_data_need_pallet('unload_pallet')
                if flg ==True:
                    if data == 1 and (task_status is None or len(task_status) == 0):#要托盘
                        #有信号，无任务，创建任务,并置空
                        self.create_order(load_pallet,unload_pallet)
                        #self.set_status_value(unload_pallet,0)                   
                else:
                    logger.error("获取数据异常{}".format(data))  
                    return 
                
            else: #空的时候判断有没有搬到，如果搬到设置为满
                if self.get_put_info(unload_pallet) == True:
                    self.main()                
        else:
            logger.error("数据库数据异常，库位（{}）信息没有配置".format(unload_pallet))      

    def run(self):
        try:
            logger.debug("一轮定时任务开始")
            self.main()
            logger.debug("一轮定时任务结束")
        except (Exception) as e:
            logger.error("创建任务异常{}".format(str(e)))
            pass
  
                

                

               
    def deal(self, e):
        #self.save_results({"error": str(e)})
        logger.error("定时任务异常（{}）".format(str(e)))  


if __name__ == '__main__':
    do  = create_task_QLSH()
    do.run()