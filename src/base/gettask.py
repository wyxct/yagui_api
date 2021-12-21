import logging
logger = logging.getLogger(__name__)
g_task_table = {}
d_task_table = {}
import sys
from ..settings import server

def gettask(module):
    import inspect
    print(inspect.getmembers(sys.modules[module.__name__], inspect.isclass))
    for name, class_ in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
        try:
            project = class_().cfg
            if project['PROJECT_NO'] in ('General',server.PROJECT_NO):
                g_task_table[class_().get_name()] = {'obj': class_(),'module_name':module.__name__}
            else:
                logger.error(f'{name} 不是此项目的定时任务')
            d_task_table[class_().get_name()] = {'obj': class_(),'module_name':module.__name__}
        except Exception as e:
            pass












