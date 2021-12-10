g_task_table = {}
import sys

def gettask(module):
    import inspect
    print(inspect.getmembers(sys.modules[module.__name__], inspect.isclass))
    for name, class_ in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
        try:
            g_task_table[class_().get_name()] = {'obj': class_(),'module_name':module.__name__}
        except Exception as e:
            pass












