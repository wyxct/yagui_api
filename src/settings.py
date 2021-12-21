# 日志文件

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_ROOT = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)

import json
import os
import json
import  sys
import codecs

import re

#module_logger = logging.getLogger("main.sub")



def getConfigData(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file_object:
            contents = file_object.read()
            if contents.startswith(bytes.decode(codecs.BOM_UTF8)):
                contents = contents.encode('utf-8').decode('utf-8-sig')
    except (Exception) as identifier:
            return None  
    return json.loads(contents)

def getALLconfig():
    errmsg = None
    basepath = os.path.dirname(os.path.realpath(sys.argv[0]))
    print("basepath2:",basepath)
    allCfg = getConfigData(os.path.join(basepath+"/src", "settings.json"))
    return allCfg
'''   
    try:
        allCfg = getConfigData(os.path.join(basepath, "settings.json"))
    except (Exception) as identifier:
        print(identifier)
        allCfg  =None 
        errmsg = identifier    
    return  allCfg,errmsg     
'''       
sinleCfg = getALLconfig()
print(sinleCfg)

class Config(object):
    DEBUG= False
    TESTING= False

 

class server(Config):
    CFG = None if sinleCfg is None or "server" not in sinleCfg else sinleCfg["server"]
    THREADED = False if CFG is None or "THREADED" not in CFG else CFG["THREADED"]
    PORT = 8700 if CFG is None or "PORT" not in CFG else CFG["PORT"]
    SYSTEM = "linux" if CFG is None or "SYSTEM" not in CFG else CFG["SYSTEM"]
    VERSION = "0.0.0.0" if CFG is None or "VERSION" not in CFG else CFG["VERSION"]
    PROJECT_NO = "None" if CFG is None or "PROJECT_NO" not in CFG else CFG["PROJECT_NO"]
    
class Scheduler:
    CFG = None if sinleCfg is None or "scheduler" not in sinleCfg else sinleCfg["scheduler"]
    """App configuration."""
    SCHEDULER_API_ENABLED = False
    SELF_BOOT =[] if CFG is None or "SELF_BOOT" not in CFG else CFG["SELF_BOOT"]
    print(SELF_BOOT)

class Logging:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                # 'format': '%(asctime)s [%(levelname)s] [%(threadName)s] [%(name)s:%(lineno)d] - %(message)s'
                'format': '%(asctime)s [%(levelname)s] [%(threadName)s] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] - %(message)s'
            },
            'simple': {
                'format': '%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            # 按大小回滚
            # 'file': {
            #     'level': 'INFO',
            #     'class': 'logging.handlers.RotatingFileHandler',
            #     'filename': os.path.join(LOG_ROOT, "graceops.log"),  # 日志文件的位置
            #     'maxBytes': 300 * 1024 * 1024,
            #     'backupCount': 10,
            #     'formatter': 'verbose'
            # },

            # 按时间回滚 保留30天日志
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_ROOT, "fs","fs.log"),
                # S Seconds
                # M Minutes
                # H Hours
                # D Days
                # 'W0'-'W6'  Weekday (0=Monday)
                # 'midnight' Roll over at midnight, if atTime not specified, else at time atTime
                'when': 'midnight',
                'formatter': 'verbose',
                'interval': 1,
                'backupCount': 30,
            },
            'crontemplate': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_ROOT, "crontemplate.log"),
                # S Seconds
                # M Minutes
                # H Hours
                # D Days
                # 'W0'-'W6'  Weekday (0=Monday)
                # 'midnight' Roll over at midnight, if atTime not specified, else at time atTime
                'when': 'midnight',
                'formatter': 'verbose',
                'interval': 1,
                'backupCount': 30,
            },
            'apscheduler': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_ROOT, "apscheduler","apscheduler.log"),
                # S Seconds
                # M Minutes
                # H Hours
                # D Days
                # 'W0'-'W6'  Weekday (0=Monday)
                # 'midnight' Roll over at midnight, if atTime not specified, else at time atTime
                'when': 'midnight',
                'formatter': 'verbose',
                'interval': 1,
                'backupCount': 30,
            },
            'api': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_ROOT, "api","api.log"),
                # S Seconds
                # M Minutes
                # H Hours
                # D Days
                # 'W0'-'W6'  Weekday (0=Monday)
                # 'midnight' Roll over at midnight, if atTime not specified, else at time atTime
                'when': 'midnight',
                'formatter': 'verbose',
                'interval': 1,
                'backupCount': 30,
            },
            'test': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_ROOT,"test.log"),
                # S Seconds
                # M Minutes
                # H Hours
                # D Days
                # 'W0'-'W6'  Weekday (0=Monday)
                # 'midnight' Roll over at midnight, if atTime not specified, else at time atTime
                'when': 'midnight',
                'formatter': 'verbose',
                'interval': 1,
                'backupCount': 30,
            },
            "http": {
            "level": "ERROR",
            "class": "logging.handlers.HTTPHandler",
            "host": "127.0.0.1:4444",
            "url": "/api/p2ptasks/",
            "method": "POST",
            "formatter": "verbose"

            }
        },
        'loggers': {
            'flask': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'api': {
                'handlers': ['api'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'crontemplate': {
                'handlers': ['crontemplate'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'apscheduler': {
                'handlers': ['apscheduler'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'main.sub': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'sqlalchemy.engine' :{

                'handlers': ['test'],
                'level': 'DEBUG',
                'propagate': True,
        }
    }
    }


def tran(src):
    if src == None:
        return None
    dst = None
    codemap= {' ':'%20','"':'%22','#':'%23','%':'%25',
    '&':'%26',
    '(':'%28',
    ')':'%29',
    '+':'%2B',
    ',':'%2C',
    '/':'%2F',
    ':':' %3A',
    ';':'%3B',
    '<':'%3C',
    '=':'%3D',
    '>':'%3E',
    '?':'%3F',
    '@':'%40',
    '\\':'%5C',
    '|':'%7C'}
    for row in range(len(src)):

        if src[row] in codemap.keys():
            #src[row] = codemap[src[row]]
            dst =dst + codemap[src[row]]
        else:
            if dst ==None:
                dst = src[row]
            else:
                dst =dst + src[row]
    return dst    

def dbin(dbtype):
    if sinleCfg is not None and "db" in sinleCfg  and dbtype in sinleCfg["db"]:
        return sinleCfg["db"][dbtype]
    else:
        return None
class Database(Config):
    '''
    CFG = None if sinleCfg is None or "Database" not in sinleCfg else sinleCfg["Database"]
    HOST = '10.10.90.84' if CFG is None or "HOST" not in CFG else CFG["HOST"]
    PORT = '5432' if CFG is None or "PORT" not in CFG else CFG["PORT"]
    DATABASE = 'IWMS' if CFG is None or "DATABASE" not in CFG else CFG["DATABASE"]
    USERNAME = 'sa' if CFG is None or "USERNAME" not in CFG else tran(CFG["USERNAME"]) 
    PASSWORD = 'wms@123' if CFG is None or "PASSWORD" not in CFG else tran(CFG["PASSWORD"])

    DB_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)
    '''
    #@staticmethod

    class postgresql():
        CFG = dbin('postgresql')
        HOST = '10.10.90.84' if CFG is None or "HOST" not in CFG else CFG["HOST"]
        PORT = '5432' if CFG is None or "PORT" not in CFG else CFG["PORT"]
        DATABASE = 'IWMS' if CFG is None or "DATABASE" not in CFG else CFG["DATABASE"]
        USERNAME = 'sa' if CFG is None or "USERNAME" not in CFG else CFG["USERNAME"]
        PASSWORD = 'wms@123' if CFG is None or "PASSWORD" not in CFG else CFG["PASSWORD"]

        DB_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}".format(username=tran(USERNAME),password=tran(PASSWORD), host=HOST,port=PORT, db=DATABASE)

    class sqlserver():
        CFG = dbin('sqlserver')
        HOST = '10.10.90.84' if CFG is None or "HOST" not in CFG else CFG["HOST"]
        PORT = '5432' if CFG is None or "PORT" not in CFG else CFG["PORT"]
        DATABASE = 'IWMS' if CFG is None or "DATABASE" not in CFG else CFG["DATABASE"]
        USERNAME = 'sa' if CFG is None or "USERNAME" not in CFG else CFG["USERNAME"]
        PASSWORD = 'wms@123' if CFG is None or "PASSWORD" not in CFG else CFG["PASSWORD"]


    #SQLALCHEMY_DATABASE_URI = DB_URI
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = True

'''
class Database(Config):
    HOST = '127.0.0.1'
    PORT = '5432'
    DATABASE = 'longjiqiepian'
    USERNAME = 'postgres'
    PASSWORD = 'admin'

    DB_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
'''
class orderserver(Config):
    CFG = None if sinleCfg is None or "orderserver" not in sinleCfg else sinleCfg["orderserver"]
    HOST = 'http://10.10.100.32' if CFG is None or "HOST" not in CFG else CFG["HOST"]
    PORT = '2016' if CFG is None or "PORT" not in CFG else CFG["PORT"]
    S_URI = "{host}:{port}/api/om/order/".format(host=HOST,port=PORT)
    I_URI = "{host}:{port}/api/om/interaction_info/find_by_type/".format(host=HOST,port=PORT)
    C_URI = "{host}:{port}/api/om/interaction_info/update/".format(host=HOST,port=PORT)  

'''
class orderserver(Config):
    HOST = 'http://127.0.0.1'

    PORT = '2000'
    S_URI = "{host}:{port}/api/om/order/".format(host=HOST,port=PORT)
    I_URI = "{host}:{port}/api/om/interaction_info/find_by_type/".format(host=HOST,port=PORT)
    C_URI = "{host}:{port}/api/om/interaction_info/update/".format(host=HOST,port=PORT)  
'''
class wmsserver(Config):
    CFG = None if sinleCfg is None or "wmsserver" not in sinleCfg else sinleCfg["wmsserver"]
    HOST = 'http://10.20.180.205' if CFG is None or "HOST" not in CFG else CFG["HOST"]
    #HOST = 'http://127.0.0.1'
    #HOST = 'http://10.10.90.84'
    PORT = '5000' if CFG is None or "PORT" not in CFG else CFG["PORT"]
    T_URI = "{host}:{port}/FinishTask".format(host=HOST,port=PORT)


class wmsserver2(Config):
    CFG = None if sinleCfg is None or "wmsserver2" not in sinleCfg else sinleCfg["wmsserver2"]
    HOST = 'http://10.20.180.205' if CFG is None or "HOST" not in CFG else CFG["HOST"]
    #HOST = 'http://127.0.0.1'
    #HOST = 'http://10.10.90.84'
    PORT = '5000' if CFG is None or "PORT" not in CFG else CFG["PORT"]
    R_URI = "{host}:{port}/gui/v1/QLSH/device/info/receive".format(host=HOST,port=PORT)

class appserver(Config):
    CFG = None if sinleCfg is None or "appserver" not in sinleCfg else sinleCfg["appserver"]
    HOST = 'http://10.20.180.205' if CFG is None or "HOST" not in CFG else CFG["HOST"]
    PORT = '4000' if CFG is None or "PORT" not in CFG else CFG["PORT"]
    get_to_loc_URI = "{host}:{port}/gui/v1/QLSH/replen/target/location".format(host=HOST,port=PORT)

area_map = {'B01': 'http://10.20.181.144:8000'} if sinleCfg is None or "area_map" not in sinleCfg else sinleCfg["area_map"]
class cornserver():
    # 获取指定交互类型的交互任务
    get_interaction_url = '{host}/api/p2ptasks/interaction/?info_status=active&type_id={interaction_type}'
    # 更新交互任务的返回值
    update_dest_url= '{host}/api/p2ptasks/interaction/'
    # 请求modbus设备是否可以上料
    get_slaver_info_disurl = '{host}/api/p2ptasks/accessibleloc/?loc_n={loc_name}'
    # 下发pl_task和order
    assign_agv_task_url = '{host}/api/p2ptasks/'
    # 处理人工交互任务
    update_i_flag_url = '{host}/api/p2ptasks/goon/'

modbus_cfg = {
        "outloc":[
            {
                "ip":"127.0.0.1",
                "port":502,
                "id":1,
                "raddr":[5010,5011],
                "waddr":[]
            }
        ]       
    } if sinleCfg is None or "modbus" not in sinleCfg else sinleCfg["modbus"]
