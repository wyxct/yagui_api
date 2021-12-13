import logging.config
import os
import json

from src.settings import Logging
from src.base.gettask import g_task_table
import copy
'''
级别          数值
CRITICAL      50
ERROR         40
WARNING       30
INFO          20
DEBUG         10
NOTSET        0
'''
def update_config(config):
    #获取所有定时任务模块 根据配置模板，生成日志。需要给默认值。
    cronhtmp =  config["handlers"]["crontemplate"]
    cronltmp =  config["loggers"]["crontemplate"]

    for key,value in g_task_table.items():
        htmp = copy.deepcopy(cronhtmp)
        ltmp = copy.deepcopy(cronltmp)
        ltmp["handlers"].remove("crontemplate")
        ltmp["handlers"].append(value["module_name"])
        tpath = htmp["filename"].replace("crontemplate.log", value["module_name"])
        if os.path.exists(tpath) == False:
            os.mkdir(tpath)
        htmp["filename"] = htmp["filename"].replace("crontemplate.log", '/'+value["module_name"]+'/'+value["module_name"]+'.log')
        if value["module_name"] not in config["handlers"]:
            config["handlers"][value["module_name"]] = htmp
        if value["module_name"] not in config["loggers"]:
            config["loggers"][value["module_name"]] = ltmp


    return config

#异常日志推送代码   
import requests
class CustomHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # some code....
        url = 'url'
        # some code....
        return requests.post(url, log_entry, headers={"Content-type": "application/json"}).content
        
def setup_logging():   
    default_path = os.path.abspath("./src/logger.json")
    if os.path.exists("./log") == False:
        os.mkdir("./log")
    if os.path.exists("./log/api") == False:
        os.mkdir("./log/api")
    if os.path.exists("./log/fs") == False:
        os.mkdir("./log/fs")
    if os.path.exists("./log/apscheduler") == False:
        os.mkdir("./log/apscheduler")
        
    if os.path.exists(default_path):
        with open(default_path, "r") as f:
            cfg = json.load(f)
            #logging.config.dictConfig(config)
    else:
        #logging.config.dictConfig(Logging.LOGGING)
        cfg = Logging.LOGGING

    config = update_config(cfg)
    logging.config.dictConfig(config)

