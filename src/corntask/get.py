import os
import importlib
import inspect
import sys
from datetime import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


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


g_task_table = {}

def gettask(module):
    print(inspect.getmembers(sys.modules[module.__name__], inspect.isclass))
    for name, class_ in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
        print(class_().__name__)
        g_task_table[class_().get_name()] = {'obj': class_()}


def loadtask(listfile):
    if len(listfile) == 0:
        return
    for row in listfile:
        mName = "tasks." + row
        module = importlib.import_module(mName)
        gettask(module)


sched = BlockingScheduler()


def add_task(func, corn):
    corn_str = corn
    strlist = corn_str.split(' ')
    lens = len(strlist)
    print(func)
    if lens == 0:
        pass
    s = strlist[0] if lens >= 1 else 0
    m = strlist[1] if lens >= 2 else '*'
    h = strlist[2] if lens >= 3 else '*'
    d = strlist[3] if lens >= 4 else '*'
    M = strlist[4] if lens >= 5 else '*'
    w = strlist[5] if lens >= 6 else '*'
    y = strlist[6] if lens >= 7 else '*'
    job = sched.add_job(func, 'cron', year=y, month=M, day=d,
                        day_of_week='*', hour=h, minute=m, second=s,next_run_time = datetime.now())
    return job


def strat_task(sched):
    sched.start()


def init():
    task_path = os.getcwd()+'/src/corntask/tasks/'
    list_file = listscript(task_path)
    print(list_file)
    loadtask(list_file)


init()
# print(g_task_table)

if __name__ == '__main__':
    task_path = os.getcwd()+'/src/corntask/tasks/'
    list_file = listscript(task_path)
    print(list_file)
    loadtask(list_file)

    for key, value in g_task_table.items():
        value['obj'].run()
        job = add_task(value['obj'].run, value['obj'].cfg['corn'])
        g_task_table[key]['job'] = job
        # print(job.id)
    sched.start()
