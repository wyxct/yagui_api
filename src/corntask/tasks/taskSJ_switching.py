
import time
# from ...base.taskcatch import catch_exception
from ..apscheduler_core import sched
from ..sql_manager import *
from ...settings import Database,area_map
import logging
logger = logging.getLogger(__name__)

'''
功能：WMS上架单分配到AGV系统，分配过的上架单号在TRM_Task_Sync_Status存在
'''

def get_taskSJ():
    sql_sentence = SQL.get_taskSJ
    rows, error_info = execute_commit_sql(Database.sqlserver, sql_sentence)
    if error_info is not None or rows is None:
        logger.info('get_taskSJ_from_DB failed! error_info: ' + str(error_info))
        return None
    else:
        return rows


class TaskSJ():
    def __init__(self):
        self.TaskId = None
        self.TaskType = None
        self.Status = None
        self.Prority = None
        self.FromLoc = None
        self.ToLoc = None
        self.WHAreaId = None

def resolve_taskSJ(current_row)->TaskSJ or None:
    if current_row is None:
        logger.info('input current_row for resolve_taskSJ is None!')
        return None

    try:
        TaskSJ_info = TaskSJ()

        if current_row[0] is not None:
            TaskSJ_info.TaskId = current_row[0]
        if current_row[1] is not None:
            TaskSJ_info.TaskType = current_row[1]
        if current_row[2] is not None:
            TaskSJ_info.Status = current_row[2]
        if current_row[3] is not None:
            TaskSJ_info.Prority = int(current_row[3])
        if current_row[4] is not None and current_row[4] != '':
            TaskSJ_info.FromLoc = current_row[4]
        if current_row[5] is not None and current_row[5] != '':
            TaskSJ_info.ToLoc = current_row[5]
        if current_row[6] is not None:
            TaskSJ_info.WHAreaId = current_row[6]

        return TaskSJ_info
    except Exception as e:
        logger.info("cannot resolve_taskSJ: " + str(current_row))
        logger.info(repr(e))
        return None



class taskSJ_switching():
    def __init__(self):
        self.__name = taskSJ_switching.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'disurl': '{host}/api/p2ptasks/'}

    @staticmethod
    def get_name():
        return "taskSJ_switching"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *'}

    def save_results(self, data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(
                job_name=taskSJ_switching.get_name(), contents=data)
            session.add(result)
            session.commit()

    # @catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        # logger.info(self.__name+ ': taskSJ_switching running,'+ time.strftime(
        #     "%Y-%m-%d %H:%M:%S", time.localtime()))
        get_taskSJ_sql = SQL.get_taskSJ
        taskSJ_result = run_sql(get_taskSJ_sql)

        result_data = {"order": []}
        import requests
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        for current_task in taskSJ_result:
            try:
                pltask_json = {
                    "task_no": None,
                    "task_type": "mp",
                    "priority": None,
                    "status": None,
                    "ex": {"TaskType": "SJ"},
                    "optlist": []
                }
                # 通过接口下发agv动作任务
                current_taskSJ = resolve_taskSJ(current_task)
                pltask_json["task_no"] = current_taskSJ.TaskId
                pltask_json["priority"] = current_taskSJ.Prority
                pltask_json["status"] = 'created'

                if (current_taskSJ.FromLoc or current_taskSJ.ToLoc) is None:
                    logger.info('there is no FromLoc/ToLoc with order: ' + str(current_taskSJ.TaskId))
                    continue

                # 1.去起点取货
                prt_1 = {'pos': current_taskSJ.FromLoc, 'opt': 'load', 'i_flag': 0}
                pltask_json["optlist"].append(prt_1)

                # 2.去check点
                check_point_sql = SQL.get_check_point.format(LocationName = current_taskSJ.ToLoc)
                location_result = run_sql(check_point_sql)
                if location_result == []:
                    check_point = None
                else:
                    check_point = location_result[0][0]

                area_id_sql = SQL.get_WHarea.format(WHAreaId = current_taskSJ.WHAreaId)
                area_result = run_sql(area_id_sql)
                if area_result == []:
                    logger.info(str(current_taskSJ.WHAreaId) + ' without areaid!!!')
                    continue
                area_id = area_result[0][0]

                if check_point == '' or check_point is None:
                    prt_2 = {'pos': current_taskSJ.ToLoc, 'opt': 'unload', 'i_flag': 0}
                else:
                    prt_2 = {'pos': current_taskSJ.ToLoc, 'opt': 'unload', 'check_point': check_point, 'i_flag': 0}
                pltask_json["optlist"].append(prt_2)

                logger.info('pltask_json: ' + str(pltask_json))

                # 4.调用pltask接口
                if area_id not in area_map:
                    logger.info('setting.py no url map with area: ' +str(area_id))
                    continue
                from ...cornapi.cornapi import assign_task_to_AGV
                rst, code = assign_task_to_AGV(area_map[area_id],pltask_json)
                '''
                pltask_url =  self.cfg['disurl'].format(host = area_map[area_id])
                response = requests.request(
                    "POST",pltask_url, json=pltask_json, headers=headers)
                logger.info(response.status_code)
                logger.info(response.text)
                '''
                # todo:超时捕获异常和错误码两种情况
                if code == 200:
                    # 5.插入任务反馈表
                    insert_Task_Sync_sql = SQL.insert_Task_Sync.format(TaskId = current_taskSJ.TaskId, Status = '10', CreateBy = 'taskSJ_switching')
                    run_sql(insert_Task_Sync_sql,'insert')

                    result_data["order"].append(pltask_json)
                else:
                    logger.info(rst, code)

            except Exception as e:
                logger.info({"error": str(e)})
        logger.info('result_data: ' + str(result_data))

