import os

from flask import request, jsonify, url_for
from flask_restful import Resource, reqparse, Api
from ..settings import server
import json
from .tasks_manage import g_task_table, tm, d_task_table
from .apscheduler_core import sched

class tasks(Resource):
    def __init__(self):
        pass

    def post(self):
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"格式错误"}, 400

        value = g_task_table[data["name"]]
        #job = add_task(value['obj'].run,value['obj'].cfg['corn'])
        cron = value['obj'].cfg['corn'] if 'cron' not in data or data['cron'] is None else data['cron']
        job_id = sched.add_job(
            value['obj'].run, 'cron', cron, job_id=value['obj'].get_name())
        return {'taskid': job_id}, 404
    def search_task(self,src,dst:list):
        for row in dst:
            if src == row["id"]:
                idx = dst.index(row)
                return idx
        return  None

    def get(self):

        data = sched.get_jobs()
        d = json.loads(data)

        for taskname,taskobj in g_task_table.items():           
            idx = self.search_task(taskname,d)
            if idx != None:
                d[idx]['desc'] = None if 'desc' not in taskobj['obj'].cfg else taskobj['obj'].cfg['desc']
                pass
            else:
                ntask = {          
                'id':taskname,
                'name':taskname,
                'desc':None if 'desc' not in taskobj['obj'].cfg else taskobj['obj'].cfg['desc'],
                'func':None,
                'func_kwargs':None,
                'trigger':'cron',
                'trigger_time':None,
                'start_date':None,
                'end_date':None,
                'state':'未加载',
                'next_run_time':None
                }
                d.append(ntask)
            
        return d, 200


class reloadtask(Resource):
    def __init__(self):
        pass

    def post(self):

        from ..base.models.public_model import  CronTask
        data = list(tm.reloadtask())
        try:
            for row in data:
                d = CronTask.query.filter_by(job_name=row).first()
                if d:
                    pass
                else:
                    
                    use = CronTask(job_name=row, active_flag=True)
                    with sched.SessionFactory() as session:      
                        session.add(use)
                        session.commit()
                        session.flush()   
        except (Exception) as e:

            return {"error":"数据库记录失败"}, 200
        return data, 200

    def get(self):
        data = list(tm.taskslist())
        return data, 200


class onetask(Resource):
    def __init__(self):
        pass

    def get(self, taskid):
        data = sched.get_job(taskid)
        return data, 200

    def put(self, taskid):
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"json 格式错误"}, 400
        if taskid not in g_task_table:
            return  {"error":"任务编号[{}]未找到".format(taskid)}, 404
        value = g_task_table[taskid]
        #job = add_task(value['obj'].run,value['obj'].cfg['corn'])
        cron = value['obj'].cfg['corn'] if 'cron' not in data or data['cron'] is None else data['cron']

        job_id = sched.modify_job(taskid, 'cron', cron)
        job = sched.get_job(taskid)
        return job, 200

    def delete(self, taskid):
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"json 格式错误"}, 400

        value = g_task_table[taskid]
        #job = add_task(value['obj'].run,value['obj'].cfg['corn'])
        #cron = value['obj'].cfg['corn'] if 'cron' not in data or data['cron'] is None else data['cron']

        job_id = sched.remove_job(taskid)
        return {'taskid': job_id}, 202


class pausetask(Resource):
    def __init__(self):
        pass

    def post(self, taskid):
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"json 格式错误"}, 400

        value = g_task_table[taskid]
        #job = add_task(value['obj'].run,value['obj'].cfg['corn'])
        #cron = value['obj'].cfg['corn'] if 'cron' not in data or data['cron'] is None else data['cron']

        flg,msg = sched.pause_job(taskid)
        if flg == True:
            job = sched.get_job(taskid)
            job['desc'] = None if 'desc' not in value['obj'].cfg else value['obj'].cfg['desc'] 
        else:
            return {'error':msg} 
        return job, 200


class resumetask(Resource):
    def __init__(self):
        pass

    def post(self, taskid):
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"json 格式错误"}, 400

        value = g_task_table[taskid]
        #job = add_task(value['obj'].run,value['obj'].cfg['corn'])
        cron = value['obj'].cfg['corn'] if 'cron' not in data or data['cron'] is None else data['cron']

        flg,msg = sched.resume_job(taskid)
        if flg == True:
            job = sched.get_job(taskid)
            job['desc'] = None if 'desc' not in value['obj'].cfg else value['obj'].cfg['desc'] 
        else:
            return {'error':msg} 
        return job, 200


class starttask(Resource):
    def __init__(self):
        pass

    def post(self, taskid):
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"格式错误"}, 400
        if taskid not in g_task_table:
            return  {"error":"定时任务（{}）不存在".format(taskid)}, 400
        value = g_task_table[taskid]
        #job = add_task(value['obj'].run,value['obj'].cfg['corn'])
        cron = value['obj'].cfg['cron'] if 'cron' not in data or data['cron'] is None else data['cron']
        job_id = sched.add_job(
            value['obj'].run, 'cron', cron, job_id=value['obj'].get_name())

        return {"task":job_id}, 200


class resultstask(Resource):
    def __init__(self):
        pass

    def get(self, taskid):
        #data = sched.get_job(taskid)
        from ..base.models.public_model import db, CronTaskResult
        r = CronTaskResult.query.filter_by(job_name=taskid).all()

        return {"job_name": taskid, "results": []}, 200

class check_crontask(Resource):
    def __init__(self):
        pass

    def get(self,project):
        # data = json.loads(request.data)
        L=[]
        if project != 'all':
            for taskname,taskobj in d_task_table.items():
                taskdetail = {}
                if taskobj['obj'].cfg['PROJECT_NO'] == project:
                    taskdetail['name'] = taskname
                    taskdetail['PROJECT_NO'] = taskobj['obj'].cfg['PROJECT_NO']
                    L.append(taskdetail)
        else:
            for taskname, taskobj in d_task_table.items():
                taskdetail = {}
                taskdetail['name'] = taskname
                taskdetail['PROJECT_NO'] = taskobj['obj'].cfg['PROJECT_NO']
                L.append(taskdetail)

        return L,200