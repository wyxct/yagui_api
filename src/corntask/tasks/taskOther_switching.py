
import time
#from ...base.taskcatch import catch_exception
from ..apscheduler_core import sched
from ..sql_manager import *
from ...settings import Database,area_map
import logging
logger = logging.getLogger(__name__)

'''
功能：WMS其他单分配到AGV系统，分配过的单号在TRM_Task_Sync_Status存在
'''


def get_taskOther():
    sql_sentence = SQL.get_taskOther
    rows, error_info = execute_commit_sql(Database.sqlserver, sql_sentence)
    if error_info is not None or rows is None:
        logger.info('get_taskOther from DB failed! error_info: ' + str(error_info))
        return None
    else:
        return rows


class TaskOther():
    def __init__(self):
        self.TaskId = None
        self.TaskType = None
        self.Status = None
        self.Prority = None
        self.FromLoc = None
        self.ToLoc = None
        self.WHAreaId = None

def resolve_taskOther(current_row)->TaskOther or None:
    if current_row is None:
        logger.info('input current_row for resolve_taskOther is None!')
        return None

    try:
        TaskOther_info = TaskOther()

        if current_row[0] is not None:
            TaskOther_info.TaskId = current_row[0]
        if current_row[1] is not None:
            TaskOther_info.TaskType = current_row[1]
        if current_row[2] is not None:
            TaskOther_info.Status = current_row[2]
        if current_row[3] is not None:
            TaskOther_info.Prority = int(current_row[3])
        if current_row[4] is not None and current_row[4] != '':
            TaskOther_info.FromLoc = current_row[4]
        if current_row[5] is not None and current_row[5] != '':
            TaskOther_info.ToLoc = current_row[5]
        if current_row[6] is not None:
            TaskOther_info.WHAreaId = current_row[6]

        return TaskOther_info
    except Exception as e:
        logger.info("cannot resolve_taskOther: " + str(current_row))
        logger.info(repr(e))
        return None



class taskOther_switching():
    def __init__(self):
        self.__name = taskOther_switching.get_name()
        # todo:update_dest_disurl 变更
        self.cfg = {'cron': '0/2 * * * * * *',
                    'disurl': '{host}/api/p2ptasks/',
                    'update_dest_disurl': '{host}/api/p2ptasks/dest/change/',
                    'update_i_flag_disurl': '{host}/api/p2ptasks/goon/'}

    @staticmethod
    def get_name():
        return "taskOther_switching"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *'}

    # @catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        # logger.info(self.__name, ' taskOther_switching running', time.strftime(
        #     "%Y-%m-%d %H:%M:%S", time.localtime()))
        get_taskOther_sql = SQL.get_taskOther
        taskOther_result = run_sql(get_taskOther_sql)


        result_data = {"order": []}
        import requests
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        for current_task in taskOther_result:
            try:
                pltask_json = {
                    "task_no": None,
                    "task_type": "mp",
                    "priority": None,
                    "status": None,
                    "ex": {"TaskType": "Other"},
                    "optlist": []
                }
                # 通过接口下发agv动作任务
                current_taskOther = resolve_taskOther(current_task)
                area_id_sql = SQL.get_WHarea.format(WHAreaId=current_taskOther.WHAreaId)
                area_result = run_sql(area_id_sql)
                if area_result == []:
                    logger.info(str(current_taskOther.WHAreaId) + ' without areaid!!!')
                    continue
                area_id = area_result[0][0]

                if current_taskOther.TaskType in ('20','60','50'):
                    pltask_json["task_no"] = current_taskOther.TaskId
                    pltask_json["priority"] = current_taskOther.Prority
                    pltask_json["status"] = 'created'
                    if (current_taskOther.FromLoc or current_taskOther.ToLoc) is None:
                        continue
                    if current_taskOther.TaskType == '20':
                        location_name = current_taskOther.FromLoc
                    else:
                        location_name = current_taskOther.ToLoc
                    check_point_sql = SQL.get_check_point.format(LocationName=location_name)
                    location_result = run_sql(check_point_sql)
                    if location_result == []:
                        check_point = None
                    else:
                        check_point = location_result[0][0]

                    if current_taskOther.TaskType == '20':
                        # 1.叫空托（类出库下架）
                        if check_point == '' or check_point is None:
                            prt_1 = {'pos': current_taskOther.FromLoc, 'opt': 'load', 'i_flag': 0}
                        else:
                            prt_1 = {'pos': current_taskOther.FromLoc, 'opt': 'load', 'check_point': check_point, 'i_flag': 0}
                        prt_2 = {'pos': current_taskOther.ToLoc, 'opt': 'unload', 'i_flag': 0}

                    elif current_taskOther.TaskType == '60':
                        # 2.回空托（类入库上架）
                        prt_1 = {'pos': current_taskOther.FromLoc, 'opt': 'load', 'i_flag': 0}
                        if check_point == '' or check_point is None:
                            prt_2 = {'pos': current_taskOther.ToLoc, 'opt': 'unload', 'i_flag': 0}
                        else:
                            prt_2 = {'pos': current_taskOther.ToLoc, 'opt': 'unload', 'check_point': check_point,'i_flag': 0}

                    else:
                        # 3.调拨（无check点）
                        prt_1 = {'pos': current_taskOther.FromLoc, 'opt': 'load', 'i_flag': 0}
                        prt_2 = {'pos': current_taskOther.ToLoc, 'opt': 'unload', 'i_flag': 0}

                    pltask_json["optlist"].append(prt_1)
                    pltask_json["optlist"].append(prt_2)
                    logger.info('pltask_json: ' + str(pltask_json))

                    # 调用pltask接口
                    if area_id not in area_map:
                        logger.info('setting.py no url map with area: ' + str(area_id))
                        continue
                    from ...cornapi.cornapi import assign_task_to_AGV
                    rst, code = assign_task_to_AGV(area_map[area_id], pltask_json)
                    '''pltask_url = self.cfg['disurl'].format(host=area_map[area_id])
                    response = requests.request(
                        "POST", pltask_url, json=pltask_json, headers=headers)
                    logger.info(response.status_code)
                    logger.info(response.text)'''
                    if code == 200:
                        # 插入任务反馈表
                        insert_Task_Sync_sql = SQL.insert_Task_Sync.format(TaskId=current_taskOther.TaskId, Status='10',
                                                                           CreateBy='taskOther_switching')
                        run_sql(insert_Task_Sync_sql, 'insert')
                        result_data["order"].append(pltask_json)
                    else:
                        logger.info(rst, code)

                elif current_taskOther.TaskType == '52':
                    # 4.再启动
                    interact_json = {
                        'task_no': current_taskOther.TaskId,
                        'info_status': 'invalid'
                    }

                    if area_id not in area_map:
                        logger.info('setting.py no url map with area: ' + str(area_id))
                        continue
                    from ...cornapi.cornapi import update_i_flag_interaction
                    rst, code = update_i_flag_interaction(area_map[area_id], interact_json)
                    '''update_interact_url = self.cfg['update_i_flag_disurl'].format(host=area_map[area_id])
                    response = requests.request(
                        "POST", update_interact_url, json=interact_json, headers=headers)
                    logger.info(response.status_code)
                    logger.info(response.text)'''
                    if code == 200:
                        # 5.插入任务反馈表
                        insert_Task_Sync_sql = SQL.insert_Task_Sync.format(TaskId=current_taskOther.TaskId, Status='20',
                                                                           CreateBy='taskOther_switching')
                        run_sql(insert_Task_Sync_sql, 'insert')
                        result_data["order"].append(interact_json)
                    else:
                        logger.info(rst, code)

                elif current_taskOther.TaskType in ('49','51'):
                    # 5.取消 & 退回
                    continue
                else:
                    logger.info('order_task task_type is not exist!! task_id: ' + str(current_taskOther.TaskId))
                    continue
            except Exception as e:
                logger.info({"error": str(e)})
        logger.info('result_data: ' + str(result_data))


