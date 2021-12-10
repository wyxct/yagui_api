import os
import importlib
import sys
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





def loadtask(listfile):
    if len(listfile) == 0:
        return
    for row in listfile:
        mName = "src.corntask.tasks." + row
        #mName = "tasks." + row
        module = importlib.import_module(mName)
        gettask(module)


def init():
    task_path = os.getcwd()+'/src/corntask/tasks/'
    list_file = listscript(task_path)
    print(list_file)
    loadtask(list_file)


class task_man:

    def reloadtask(self):
        task_path = os.getcwd()+'/src/corntask/tasks/'
        list_file = listscript(task_path)
        print(list_file)
        loadtask(list_file)
        return g_task_table.keys()

    def taskslist(self):
        return g_task_table.keys()


init()
print(g_task_table)
tm = task_man()


if __name__ == '__main__':
    task_path = os.getcwd()+'/src/corntask/tasks/'
    list_file = listscript(task_path)
    print(list_file)
    loadtask(list_file)
