import os
import importlib
import sys
from ..settings import server,Scheduler
from .apscheduler_core import sched
from ..base.gettask import g_task_table,gettask

def listscript(path):  # 传入存储的list
    list_name = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            pass
        else:
            if os.path.splitext(file)[1] == '.py':
                list_name.append(os.path.splitext(file)[0])
    return list_name





def loadtask(listfile,project_no):
    if len(listfile) == 0:
        return
    for row in listfile:
        mName = f"src.corntask.tasks.{project_no}.{row}"
        #mName = "tasks." + row
        module = importlib.import_module(mName)
        gettask(module)


def init():
    general_path = os.getcwd()+'/src/corntask/tasks/General'
    general_file = listscript(general_path)
    loadtask(general_file,'General')
    project_no = server.PROJECT_NO
    project_file = []
    if project_no != 'None':
        project_path = os.getcwd()+'/src/corntask/tasks/{}'.format(project_no)
        project_file = listscript(project_path)
        loadtask(project_file,project_no)



class task_man:
    def init_selfboot(self):
        selfboot = Scheduler.SELF_BOOT
        for cron in selfboot:
            task = g_task_table[cron]
            CFG = task['obj']
            cron = CFG.cfg
            sched.add_job(task['obj'].run, 'cron', cron['cron'], job_id=task['obj'].get_name())
            # print(sched.get_jobs())

    def reloadtask(self):
        general_path = os.getcwd()+'/src/corntask/tasks/'
        general_file = listscript(general_path)
        loadtask(general_file,'General')
        project_no = server.PROJECT_NO
        project_file = []
        if project_no != 'None':
            project_path = os.getcwd() + '/src/corntask/tasks/{}'.format(project_no)
            project_file = listscript(project_path)
            loadtask(project_file, project_no)
        return g_task_table.keys()

    def taskslist(self):
        return g_task_table.keys()


init()
tm = task_man()
tm.init_selfboot()

if __name__ == '__main__':
    task_path = os.getcwd()+'/src/corntask/tasks/General'
    list_file = listscript(task_path)
    loadtask(list_file)
