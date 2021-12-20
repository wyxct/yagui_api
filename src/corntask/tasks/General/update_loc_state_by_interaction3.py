
import time
#from ....base.taskcatch import catch_exception
from ...apscheduler_core import sched
from ...sql_manager import *
from ....settings import Database,area_map
import requests
import logging
logger = logging.getLogger(__name__)

'''
功能：维护库位空满状态，处理交互type为3的交互信息
interaction_info_type = 3：库位更新为空库位
interaction_info_type = 6：库位更新为满库位
'''

class update_loc_state_by_interaction3():
    def __init__(self):
        self.__name = update_loc_state_by_interaction3.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'get_interaction_disurl':'{host}/api/p2ptasks/interaction/?info_status=active&type_id=[3,6]',
                    'update_dest_disurl': '{host}/api/p2ptasks/interaction/',
                    'desc':"通用库位状态维护策略",'PROJECT_NO':'General'}
        self.update_type = 'false'
        self.update_list = "('P1-01-01-01','P1-01-02-01')"

    @staticmethod
    def get_name():
        return "update_loc_state_by_interaction3"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *'}


    # @catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        # logger.info(self.__name+ ': update_loc_state_by_interaction3 running,'+time.strftime(
        #     "%Y-%m-%d %H:%M:%S", time.localtime()))

        result_data = {"order": []}
        import requests
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }


        for area_id, area_url in area_map.items():
            try:
                # 模拟传送带置空满
                if self.update_type == 'full_to_empty':
                    update_loc_sql = SQL.update_location_1.format(Status='empty', OPT_By='interaction3()',
                                                                LocationName=self.update_list,old_Status = 'full')
                    run_sql(update_loc_sql, 'update')

                elif self.update_type == 'empty_to_full':
                    update_loc_sql = SQL.update_location_1.format(Status='full', OPT_By='interaction6()',
                                                                LocationName=self.update_list, old_Status='empty')
                    run_sql(update_loc_sql, 'update')

                from ...cornapi.cornapi import get_interaction_by_type
                rst, code = get_interaction_by_type(area_url, str([3,6]))
                '''get_interaction_url = self.cfg['get_interaction_disurl'].format(host=area_url)
                get_interaction_response = requests.request("GET", get_interaction_url, headers=headers)
                if 200 != get_interaction_response.status_code:
                    logger.info(get_interaction_url + str(get_interaction_response.status_code))
                else:
                    logger.info("get_interaction success, type_id = 3&6")'''
                if code == 200:
                    interaction_info = rst
                    if interaction_info['data'] is None:
                        logger.info('there is no message when get interaction by type_id = 3&6')
                        continue
                    else:
                        re_data_list = interaction_info['data']
                        for re_data in re_data_list:
                            interaction_info_id = re_data['interaction_info_id']
                            task_id = re_data['interaction_info_name']
                            interaction_info_type_id = re_data['interaction_info_type_id']
                            pos_loc = re_data['value_json'].get('pos',None)
                            if pos_loc is None:
                                logger.info('there is no pos in interaction.value_json, info_id = ' + str(interaction_info_id))
                                continue
                            else:
                                # 检验单子的任务类型
                                get_task_type_sql = SQL.get_taskOther_by_taskid.format(TaskId=task_id)
                                task_type_result = run_sql(get_task_type_sql)

                                if task_type_result != [] and task_type_result[0][0] in ['98','99'] and pos_loc[:6] == 'B01-T1':
                                    # 空托垛任务
                                    get_groupid_sql = SQL.get_loc_groupid.format(LocationName=pos_loc)
                                    groupid_result = run_sql(get_groupid_sql)
                                    if groupid_result != []:
                                        GroupId = groupid_result[0][0]
                                    else:
                                        logger.info('stack loc without groupid,loc: '+ str(pos_loc))
                                        return

                                    if interaction_info_type_id == 3:
                                        update_loc_sql = SQL.update_stack_location.format(Status='empty', OPT_By='interaction3()',GroupId = GroupId,LLayer=10)
                                        run_sql(update_loc_sql, 'update')
                                    elif interaction_info_type_id == 6:
                                        PalletCount = task_type_result[0][1]
                                        if PalletCount is not None:
                                            update_loc_sql = SQL.update_stack_location.format(Status='full', OPT_By='interaction6()',GroupId = GroupId,LLayer=PalletCount)
                                            run_sql(update_loc_sql, 'update')
                                        else:
                                            logger.info('there is no palletcount with stack task,task_id: ' + str(task_id))
                                    else:
                                        return
                                else:
                                    if interaction_info_type_id == 3:
                                        update_loc_sql = SQL.update_location.format(Status='empty', OPT_By='interaction3()',
                                                                                    LocationName=pos_loc)
                                        run_sql(update_loc_sql, 'update')
                                    elif interaction_info_type_id == 6:
                                        update_loc_sql = SQL.update_location.format(Status='full', OPT_By='interaction6()',
                                                                                    LocationName=pos_loc)
                                        run_sql(update_loc_sql, 'update')
                                    else:
                                        return

                                interact_json = {
                                    'interaction_info_id': interaction_info_id,
                                    'info_status': 'invalid',
                                    'return_value': pos_loc
                                }
                                from ...cornapi.cornapi import update_interaction_return_value
                                rst, code = update_interaction_return_value(area_url, interact_json)
                                '''update_dest_url = self.cfg['update_dest_disurl'].format(host=area_url)
                                response = requests.request(
                                    "POST", update_dest_url, json=interact_json, headers=headers)
                                logger.info(response.status_code)
                                logger.info(response.text)'''
                                if code == 200:
                                    result_data["order"].append(interact_json)
                                else:
                                    logger.info(rst, code)
            except Exception as e:
                logger.info({"error": str(e)})
        logger.info('result_data: ' + str(result_data))



