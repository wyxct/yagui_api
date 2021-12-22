import logging
logger = logging.getLogger("apscheduler")
g_task_table = {}
g_task_list = {}
import sys
from ..settings import server

def gettask(module):
    import inspect
    print(inspect.getmembers(sys.modules[module.__name__], inspect.isclass))
    for name, class_ in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
        try:
            project = class_().cfg
            if project['PROJECT_NO'] in ('General',server.PROJECT_NO):
                g_task_table[class_().get_name()] = {'obj': class_(),'module_name':module.__name__,"module":module}
            else:
                logger.error(f'{name} 不是此项目的定时任务')
            g_task_list[class_().get_name()] = {'obj': class_(),'module_name':module.__name__,"module":module}
        except Exception as e:
            logger.error(str(e))
            pass












