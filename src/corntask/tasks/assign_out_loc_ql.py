
import time
#from ...base.taskcatch import catch_exception
from ..apscheduler_core import sched
from ..sql_manager import *
from ...settings import Database,area_map
import requests
import logging
logger = logging.getLogger(__name__)




class assign_out_loc():
    def __init__(self):
        self.__name = assign_out_loc.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'get_interaction_disurl':'{host}/api/p2ptasks/interaction/?info_status=active&type_id=[1,4]',
                    'update_dest_disurl': '{host}/api/p2ptasks/interaction/','desc':"齐鲁石化装车出库选垛口逻辑"}

    @staticmethod
    def get_name():
        return "assign_out_loc"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *'}

    # @catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        logger.info(self.__name+ ':running,'+ time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()))

        sql = 'select * from layer4_1_om.interaction_info where interaction_info_type_id = 1 and info_status = \'active\' order by interaction_info_id desc'
        print(sql)
 
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            iinfo = cursor.fetchall()
            session.commit()

        '''
        1、查询交互表信息类型1且活跃的交互（check）
        2、查询location 位置 是否是不可直达的location，如果是，查询该类型check type下所有location
        3、查询location的状态

        '''
        for row in iinfo:

            try:
                get_interaction_url = self.cfg['get_interaction_disurl'].format(host=area_url)
                get_interaction_response = requests.request("GET", get_interaction_url, headers=headers)
                if 200 != get_interaction_response.status_code:
                    logger.info(get_interaction_response.status_code)
                else:
                    logger.info("get_interaction success, type_id = 1")
                    interaction_info = json.loads(get_interaction_response.content)
                    if interaction_info['data'] is None:
                        logger.info('there is no message when get interaction by type_id = 1')
                        continue
                    else:
                        re_data_list = interaction_info['data']
                        for re_data in re_data_list:
                            interaction_info_id = re_data['interaction_info_id']
                            interaction_info_type_id = re_data['interaction_info_type_id']
                            pos_loc = re_data['value_json'].get('pos',None)
                            if pos_loc is None:
                                logger.info('there is no pos in interaction.value_json, info_id = ' +str(interaction_info_id))
                                continue
                            else:
                                if interaction_info_type_id == 1:
                                    # 取货
                                    new_loc = get_FromLoc_in_check(pos_loc)
                                elif interaction_info_type_id == 4:
                                    # 卸货
                                    new_loc = get_ToLoc_in_check(pos_loc)
                                else:
                                    new_loc = None

                                if new_loc is None:
                                    # todo: 分配目的地无位置，如何处理？
                                    return

                                interact_json = {
                                    'interaction_info_id': interaction_info_id,
                                    'info_status': 'invalid',
                                    'return_value': new_loc
                                }

                                update_dest_url = self.cfg['update_dest_disurl'].format(host=area_url)
                                response = requests.request(
                                    "POST", update_dest_url, json=interact_json, headers=headers)
                                logger.info(response.status_code)
                                logger.info(response.text)
                                if response.status_code == 200:
                                    result_data["order"].append(interact_json)
            except Exception as e:
                logger.info({"error": str(e)})

        logger.info(result_data)



def get_ToLoc_in_check(pos_loc):
    get_empty_loc_sql = SQL.get_empty_loc.format(pos_loc=pos_loc)
    empty_loc_result = run_sql(get_empty_loc_sql)[0]
    empty_loc = empty_loc_result[0]

    if empty_loc == '':
        print()
        return None

    # 维护库位状态，此处不需要维护库位状态？还是和空托统一维护（暂时不维护出入库的lock状态）
    # update_loc_sql = SQL.update_location.format(Status='lock', OPT_By='get_ToLoc_in_check()',
    #                                             LocationName=empty_loc)
    # run_sql(update_loc_sql, 'update')

    return empty_loc


def get_FromLoc_in_check(pos_loc):
    get_full_loc_sql = SQL.get_full_pallet_loc.format(pos_loc=pos_loc)
    full_loc_result = run_sql(get_full_loc_sql)[0]
    full_loc = full_loc_result[0]

    if full_loc == '':
        print()
        return None

    # # 维护库位状态，此处不需要维护库位状态？还是和空托统一维护。（暂时不维护出入库的lock状态）
    # update_loc_sql = SQL.update_location.format(Status='lock', OPT_By='get_FromLoc_in_check()',
    #                                             LocationName=full_loc)
    # run_sql(update_loc_sql, 'update')

    return full_loc
