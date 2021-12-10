# -*- coding: UTF-8 -*-

def singleton(cls, *args, **kwargs):
    instances= {}
    def get_single():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_single

















