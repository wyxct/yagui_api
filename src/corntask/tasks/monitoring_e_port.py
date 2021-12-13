
import time
from ...base.taskcatch import catch_exception
if __name__ == '__main__':
    pass
else:
    from ..apscheduler_core import sched

import logging
logger = logging.getLogger(__name__)


class monitoring_e_port():
    def __init__(self):
        self.__name = monitoring_e_port.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/'}

    @staticmethod
    def get_name():
        return "monitoring_e_port"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *', 'disurl': 'http://127.0.0.1:2000/api/om/interaction_info/find_by_type/'}

    def save_results(self, data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(
                job_name=monitoring_e_port.get_name(), contents=data)
            session.add(result)
            session.commit()

    def set_status_value(self,location_name,object_put_type):
        sql = 'update layer2_pallet.location_object set object_put_type = \'{}\',last_updated_timestamp = now() where location_name =\'{}\''.format(object_put_type,location_name)
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            session.commit()

    # @catch_exception
    def run(self):
        '''
        如果标志位1，
        读取批次数据
        '''
        from ...modbus import get_string_batch
        from ...settings import modbus_cfg
        from ...base.webwmes import reporteport
        import re
        import json
        from sqlalchemy import select
        from sqlalchemy import update


        slavelist = {"inloc1":"S1-01-01-01","inloc2":"S2-01-01-01","inloc3":"S3-01-01-01","inloc4":"S4-01-01-01"}
        reslavelist = {"S1-01-01-01":"inloc1","S2-01-01-01":"inloc2","S3-01-01-01":"inloc3","S4-01-01-01":"inloc4"}
        #tmp = modbus_cfg["outloc"]["addrs"].keys()
        tmp = str(list(slavelist.values())).lstrip('[').rstrip(']')
        sql = 'SELECT object_put_type, location_name FROM layer2_pallet.location_object where opt_condition = \'modbus\' and location_name in({})'.format(tmp)
        
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            write_status = cursor.fetchall()
            session.commit()
        for row in write_status:
            #空的时候可读，非空不读
            if row.object_put_type == 0:
                #空，开始读数据，直到读到有托盘
                '''
                找到目标点一致的取货交互表已经完成的最新一条数据，查对应order。如果有设置为0，并设置交互的interaction_info_desp
                '''
                sql = 'SELECT interaction_info_id, interaction_info_name, interaction_info_desp FROM layer4_1_om.interaction_info where interaction_info_type_id = 3 and interaction_info_desp is null and return_value = \'{}\' order by interaction_info_id desc limit 1;'.format(row.location_name)
                with sched.SessionFactory() as session:            
                    cursor = session.execute(sql)
                    inter = cursor.fetchall()
                    session.commit()

                if inter is None or len(inter) ==0:
                    continue
                
                sql = 'update layer2_pallet.location_object set object_put_type = 0,last_updated_timestamp = now() where location_name =\'{}\''.format(row.location_name)
                sql2 = 'update layer4_1_om.interaction_info set interaction_info_desp = \'set\' where interaction_info_id ={}'.format(inter[0].interaction_info_id)
                
                with sched.SessionFactory() as session:            
                    cursor = session.execute(sql2)
                    cursor2 = session.execute(sql)
                    session.commit()
            else: #非空，查看是否被取走，

                loc = reslavelist[row.location_name]
                '''
                addr_list =[]
                addr_list.append(addr)
                flag,data = get_string_sync(loc,addr_list)
                
                '''          
                flag,data = get_string_batch(loc)
                if flag == True:
                    #将从设备查到的批次信息传给wms
                    rst,code = reporteport({"dev":  modbus_cfg[loc]["id"],"data":data})
                    if code == 200:
                        self.set_status_value(row.location_name,0)
                    else:
                        #sql = 
                        logger.error("上报失败不处理{}".format(row.location_name))
                        continue

                

                

               
    def deal(self, e):
        #self.save_results({"error": str(e)})
        logger.error("定时任务异常（{}）".format(str(e)))  


if __name__ == '__main__':
    do  = monitoring_e_port()
    do.run()