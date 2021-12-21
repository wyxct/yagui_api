
import time
#from ....base.taskcatch import catch_exception
from ...corntask.apscheduler_core import sched
from ...corntask.sql_manager import *
from ...settings import Database,area_map
import logging
logger = logging.getLogger(__name__)

'''
功能：WMS下架单分配到AGV系统，分配过的单号在TRM_Task_Sync_Status存在
'''

def get_taskXJ():
    sql_sentence = SQL.get_taskXJ
    rows, error_info = execute_commit_sql(Database.sqlserver, sql_sentence)
    if error_info is not None or rows is None:
        logger.info('get_taskXJ_from_DB failed! error_info: ' + str(error_info))
        return None
    else:
        return rows


class TaskXJ():
    def __init__(self):
        self.TaskId = None
        self.TaskType = None
        self.Status = None
        self.Prority = None
        self.FromLoc = None
        self.ToLoc = None
        self.empty_pallet_exist = None
        self.empty_pallet_pos = None
        self.i_flag = None
        self.WHAreaId = None
        self.empty_pallet_topos = None

def resolve_taskXJ(current_row)->TaskXJ or None:
    if current_row is None:
        logger.info('input current_row for resolve_taskXJ is None!')
        return None

    try:
        TaskXJ_info = TaskXJ()

        if current_row[0] is not None:
            TaskXJ_info.TaskId = current_row[0]
        if current_row[1] is not None:
            TaskXJ_info.TaskType = current_row[1]
        if current_row[2] is not None:
            TaskXJ_info.Status = current_row[2]
        if current_row[3] is not None:
            TaskXJ_info.Prority = int(current_row[3])
        if current_row[4] is not None and current_row[4] != '':
            TaskXJ_info.FromLoc = current_row[4]
        if current_row[5] is not None and current_row[5] != '':
            TaskXJ_info.ToLoc = current_row[5]
        if current_row[6] is not None:
            TaskXJ_info.empty_pallet_exist = current_row[6]
        if current_row[7] is not None:
            TaskXJ_info.empty_pallet_pos = current_row[7]
        if current_row[8] is not None:
            TaskXJ_info.i_flag = current_row[8]
        if current_row[9] is not None:
            TaskXJ_info.WHAreaId = current_row[9]
        if current_row[10] is not None:
            TaskXJ_info.empty_pallet_topos = current_row[10]

        return TaskXJ_info
    except Exception as e:
        logger.info("cannot resolve_taskXJ: " + str(current_row))
        logger.info(repr(e))
        return None



class taskXJ_switching():
    def __init__(self):
        self.__name = taskXJ_switching.get_name()
        self.cfg = {'cron': '0/2 * * * * * *',
                    'disurl': '{host}/api/p2ptasks/',
                    'desc':"金红叶下架任务下发AGV",'PROJECT_NO':'General'}

    @staticmethod
    def get_name():
        return "taskXJ_switching"

    @staticmethod
    def get_cfg():
        return {'cron': '0/2 * * * * * *'}

    def save_results(self, data):
        from ...base.models.public_model import CronTaskResult
        with sched.SessionFactory() as session:
            result = CronTaskResult(
                job_name=taskXJ_switching.get_name(), contents=data)
            session.add(result)
            session.commit()

    # @catch_exception
    def run(self):
        #from ...base.models.public_model import db,CronTaskResult
        import json
        # logger.info(self.__name+ ': taskXJ_switching running,'+ time.strftime(
        #     "%Y-%m-%d %H:%M:%S", time.localtime()))
        get_taskXJ_sql = SQL.get_taskXJ
        taskXJ_result = run_sql(get_taskXJ_sql)


        result_data = {"order": []}
        import requests
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        for current_task in taskXJ_result:
            try:
                pltask_json = {
                    "task_no": None,
                    "task_type": "mp",
                    "priority": None,
                    "status": None,
                    "ex": {"TaskType": "XJ"},
                    "optlist": []
                }
                # 1.通过接口下发agv动作任务
                current_taskXJ = resolve_taskXJ(current_task)
                pltask_json["task_no"] = current_taskXJ.TaskId
                pltask_json["priority"] = current_taskXJ.Prority
                pltask_json["status"] = 'created'

                if (current_taskXJ.FromLoc or current_taskXJ.ToLoc) is None:
                    logger.info('there is no FromLoc/ToLoc with order: '+ str(current_taskXJ.TaskId))
                    continue

                # 1.去check点 + 去起点取货——是否有check点；
                check_point_sql = SQL.get_check_point.format(LocationName=current_taskXJ.FromLoc)
                location_result = run_sql(check_point_sql)
                if location_result == []:
                    check_point = None
                else:
                    check_point = location_result[0][0]

                area_id_sql = SQL.get_WHarea.format(WHAreaId=current_taskXJ.WHAreaId)
                area_result = run_sql(area_id_sql)
                if area_result == []:
                    logger.info(str(current_taskXJ.WHAreaId) + ' without areaid!!!')
                    continue
                area_id = area_result[0][0]

                if check_point == '' or check_point is None:
                    prt_1 = {'pos': current_taskXJ.FromLoc, 'opt': 'load'}
                else:
                    prt_1 = {'pos': current_taskXJ.FromLoc, 'opt': 'load', 'check_point':check_point}
                pltask_json["optlist"].append(prt_1)

                # 2.去终点卸货——是否有交互【业务层为是否自动完成】；
                if current_taskXJ.i_flag == 'N':
                    i_flag = 0 # 不自动完成[False]
                else:
                    i_flag = 1 # 不自动完成[True]

                prt_2 = {'pos': current_taskXJ.ToLoc, 'opt': 'unload', 'i_flag': i_flag}
                pltask_json["optlist"].append(prt_2)

                # 3.是否带空托
                if current_taskXJ.empty_pallet_exist == 'Y' \
                        and current_taskXJ.empty_pallet_topos is not None \
                        and current_taskXJ.empty_pallet_pos is not None:
                    prt_3 = {'pos': current_taskXJ.empty_pallet_pos, 'opt': 'load'}
                    pltask_json["optlist"].append(prt_3)

                    prt_4 = {'pos': current_taskXJ.empty_pallet_topos, 'opt': 'unload'}
                    pltask_json["optlist"].append(prt_4)

                logger.info('pltask_json: ' + str(pltask_json))

                # 4.调用pltask接口
                if area_id not in area_map:
                    logger.info('setting.py no url map with area: ' +str(area_id))
                    continue
                from ...cornapi.cornapi import assign_task_to_AGV
                rst, code = assign_task_to_AGV(area_map[area_id], pltask_json)
                '''
                pltask_url =  self.cfg['disurl'].format(host = area_map[area_id])
                response = requests.request(
                    "POST",pltask_url, json=pltask_json, headers=headers)
                logger.info(response.status_code)
                logger.info(response.text)
                '''
                if code == 200:
                    # 5.插入任务反馈表
                    insert_Task_Sync_sql = SQL.insert_Task_Sync.format(TaskId = current_taskXJ.TaskId, Status = '10', CreateBy = 'taskXJ_switching')
                    run_sql(insert_Task_Sync_sql,'insert')

                    result_data["order"].append(pltask_json)
                else:
                    logger.info(rst, code)

            except Exception as e:
                logger.info({"error": str(e)})
        logger.info('result_data: ' + str(result_data))

