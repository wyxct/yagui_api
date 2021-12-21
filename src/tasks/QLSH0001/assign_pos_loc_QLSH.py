
import time
#from ....base.taskcatch import catch_exception
from ...corntask.apscheduler_core import sched
from ...corntask.sql_manager import *
from ...settings import Database,area_map
import requests
import logging
logger = logging.getLogger(__name__)
import json

'''
【齐鲁石化】
功能：check点分配目的地，处理交互type为1、4、5的交互信息，入库目的地分配通过接口向上游请求
type1：check 取货交互
type4：check 卸货交互
type5：传送带check点交互
'''
headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

class assign_pos_loc_QLSH():
    def __init__(self):
        self.__name = assign_pos_loc_QLSH.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'get_interaction_disurl':'{host}/api/p2ptasks/interaction/?info_status=active&type_id=[1,4,5]',
                    'update_dest_disurl': '{host}/api/p2ptasks/interaction/',
                    'get_slaver_info_disurl': '{host}/api/p2ptasks/accessibleloc/?loc_n=',
                    'desc':"齐鲁石化check点目的地分配策略",'PROJECT_NO':'General'}

    @staticmethod
    def get_name():
        return "assign_pos_loc_QLSH"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *'}

    # @catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        # logger.info(self.__name+ ': assign_pos_loc_QLSH running,'+ time.strftime(
        #     "%Y-%m-%d %H:%M:%S", time.localtime()))

        result_data = {"order": []}
        import requests



        for area_id, area_url in area_map.items():
            try:
                from ...cornapi.cornapi import get_interaction_by_type
                rst, code = get_interaction_by_type(area_url, str([1,4,5]))
                '''get_interaction_url = self.cfg['get_interaction_disurl'].format(host=area_url)
                get_interaction_response = requests.request("GET", get_interaction_url, headers=headers)
                if 200 != get_interaction_response.status_code:
                    logger.info(get_interaction_url + str(get_interaction_response.status_code))
                else:
                    interaction_info = json.loads(get_interaction_response.content)'''
                if code == 200:
                    interaction_info = rst
                    if interaction_info['data'] is None:
                        logger.info('there is no message when get interaction by type_id = 1&4&5')
                        continue
                    else:
                        re_data_list = interaction_info['data']
                        for re_data in re_data_list:
                            interaction_info_id = re_data['interaction_info_id']
                            interaction_info_type_id = re_data['interaction_info_type_id']
                            task_id = re_data['interaction_info_name']
                            pos_loc = re_data['value_json'].get('pos',None)
                            if pos_loc is None:
                                logger.info('there is no pos in interaction.value_json, info_id = ' + str(interaction_info_id))
                                continue
                            else:
                                if interaction_info_type_id == 1:
                                    # 取货
                                    new_loc = get_FromLoc_in_check(pos_loc)
                                elif interaction_info_type_id == 4:
                                    # 卸货
                                    new_loc = get_ToLoc_by_url(task_id)
                                elif interaction_info_type_id == 5:
                                    # 传动带check点卸货
                                    new_loc = get_ToLoc_in_trans_check(area_url)
                                else:
                                    new_loc = None

                                if new_loc is None:
                                    # todo: 分配目的地无位置，如何处理？
                                    logger.warning('there is no pos for order: ' +str(interaction_info_id))
                                    continue

                                interact_json = {
                                    'interaction_info_id': interaction_info_id,
                                    'info_status': 'invalid',
                                    'return_value': new_loc
                                }
                                from ...cornapi.cornapi import update_interaction_return_value
                                rst, code = update_interaction_return_value(area_url, interact_json)
                                '''update_dest_url = self.cfg['update_dest_disurl'].format(host=area_url)
                                response = requests.request(
                                    "POST", update_dest_url, json=interact_json, headers=headers)
                                logger.info(response.status_code)
                                logger.info(response.text)
                                if response.status_code == 200:'''
                                if code == 200:
                                    result_data["order"].append(interact_json)
                                    if interaction_info_type_id == 5:
                                        # 维护库位lock状态
                                        update_loc_sql = SQL.update_location.format(Status='lock',
                                                                                    OPT_By='Cron',
                                                                                    LocationName=new_loc)
                                        run_sql(update_loc_sql, 'update')
                                else:
                                    logger.info(rst, code)
            except Exception as e:
                logger.info({"error": str(e)})

        logger.info('result_data: ' + str(result_data))



def get_ToLoc_in_check(pos_loc):
    get_empty_loc_sql = SQL.get_empty_loc.format(pos_loc=pos_loc)
    empty_loc_result = run_sql(get_empty_loc_sql)
    if empty_loc_result != []:
        empty_loc = empty_loc_result[0][0]
    else:
        logger.warning('there is no empty des for ' + str(pos_loc))
        return None

    # 维护库位状态，此处不需要维护库位状态？还是和空托统一维护（暂时不维护出入库的lock状态）
    # update_loc_sql = SQL.update_location.format(Status='lock', OPT_By='get_ToLoc_in_check()',
    #                                             LocationName=empty_loc)
    # run_sql(update_loc_sql, 'update')

    return empty_loc

def get_ToLoc_by_url(task_id):
    '''
        齐鲁石化定制，由于不知道货物属性，不知道第二层是否能放货物
        通过接口跟app交互获取放货目的地，反馈给AGV系统
        :return:可用的卸货位置 or None
        '''
    from ...cornapi.appapi import get_replen_ToLoc
    empty_loc = get_replen_ToLoc(task_id)
    return empty_loc



def get_FromLoc_in_check(pos_loc):
    get_full_loc_sql = SQL.get_full_pallet_loc.format(pos_loc=pos_loc)
    full_loc_result = run_sql(get_full_loc_sql)
    if full_loc_result != []:
        full_loc = full_loc_result[0][0]
    else:
        print()
        return None

    # # 维护库位状态，此处不需要维护库位状态？还是和空托统一维护。（暂时不维护出入库的lock状态）
    # update_loc_sql = SQL.update_location.format(Status='lock', OPT_By='get_FromLoc_in_check()',
    #                                             LocationName=full_loc)
    # run_sql(update_loc_sql, 'update')

    return full_loc


def get_ToLoc_in_trans_check(host):
    '''
    通过接口跟传送带交互获取空闲目的地，反馈给AGV系统
    :return:可用的传送带入口位置 or None
    '''
    try:
        empty_loc = None

        get_empty_loc_sql = SQL.get_empty_loc_in_trans
        empty_loc_result = run_sql(get_empty_loc_sql)
        if empty_loc_result is None:
            return None
        for pos_loc_result in empty_loc_result:
            pos_loc = pos_loc_result[0]
            '''get_slaves_response = requests.request("GET", disurl+pos_loc, headers=headers)
            if 200 != get_slaves_response.status_code:
                logger.warning(disurl+pos_loc + str(get_slaves_response.status_code))
            else:'''
            from ...cornapi.cornapi import get_slave_info
            rst, code = get_slave_info(host, pos_loc)
            if code == 200:
                slaves_info = rst
                if slaves_info[pos_loc] != []:
                    empty_loc = slaves_info[pos_loc][0]
                    break

        return empty_loc

    except Exception as e:
        logger.info({"error": str(e)})





