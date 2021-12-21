
import time
if __name__ == '__main__':
    pass
else:
    from ...corntask.apscheduler_core import sched

import logging
logger = logging.getLogger(__name__)


class mock_modbus():
    def __init__(self):
        self.__name = mock_modbus.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/','PROJECT_NO':'General'}

    @staticmethod
    def get_name():
        return "mock_modbus"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *', 'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/'}

    def save_results(self, data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(
                job_name=mock_modbus.get_name(), contents=data)
            session.add(result)
            session.commit()

    def set_status_value(self,location_name,object_put_type):
        sql = 'update layer2_pallet.location_object set object_put_type = \'{}\',last_updated_timestamp = now() where location_name ={}'.format(object_put_type,location_name)
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            session.commit()

    # @catch_exception
    def run(self):
        '''
        如果标志位1，
        读取批次数据
        '''
        from ...modbus import get_data_sync,set_data_sync
        from ...settings import modbus_cfg
        import re
        import json
        '''
        开始取料on 设置不可取，开始取料off设置可取
        垛口1：读 40010 = 1 set 45010 =0  读40010 =0 set 45010=1
        垛口2：读 40011 = 1 set 45011 =0  读40011 =0 set 45011=1
        1：读 40060 set 45060
        2：读 40061 set 45061
        3：读 40062 set 45062
        4：读 40063 set 45063
        int(not(0))
        '''
        
        addmap = {9:109,10:110,59:159,60:160,61:161,62:162}
        addr = modbus_cfg["outloc"]["addrs"].values()
        '''
        flg,data = get_data_sync("outloc",addr)
        if flg == True:
            for key,row in data.items():
                if row == 1:
                    time.sleep(10)
                    sflg,dat = set_data_sync("outloc",{key:0})
                    print(sflg,dat)   

            print(data)
        '''
        '''
        #垛口1：       
        flg,data = get_data_sync("outloc",[9,10],False)
        if flg == True:
            for key,row in data.items():
                sflg,dat = set_data_sync("outloc",{addmap[key]:int((row))},False)
        '''
        #入库口
        flg,data = get_data_sync("inloc1",[59,60,61,62],False)
        if flg == True:
            for key,row in data.items():
                sflg,dat = set_data_sync("inloc1",{addmap[key]:int(not(row))},False)
                #sflg,dat = set_data_sync("outloc",{45011:int(not(row))})
        
               
    def deal(self, e):
        self.save_results({"error": str(e)})


if __name__ == '__main__':
    do  = mock_modbus()
    do.run()