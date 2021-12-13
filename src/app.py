from .settings import Database
from flask_cors import CORS
import logging

from flask import Flask

from .base.logset import setup_logging
from .corntask.app import asyntask_bp
from .pltask.app import task_bp
from .modbustest.app import mt_bp
#from .modbus.app import mod_bp
from .version import version
#from .settings import brokers,backend
#from celery import Celery
logger = logging.getLogger('api')
from .error import exception

def create_app():
    setup_logging()
    #app = Flask(__name__,template_folder='../templates')
    app = Flask(__name__,template_folder='../templates',static_folder ='../static' ,static_url_path='/static')   
    CORS(app, resources=r'/*')
    #app.config.from_object(Database)
    app.register_blueprint(asyntask_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(mt_bp)
    #app.register_blueprint(exception,url_prefix='/api')
    #db.init_app(app)
    
    
    from flask import request
    import os
    import datetime

    @app.after_request
    def response_logger(response):
        pass
        # 获取接口响应数据
        api_path = request.full_path
        api_method = request.method
        ip_addr = request.remote_addr
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d")
        api_path_tmp = api_path.split('?')
        api_path = api_path_tmp[0]
        log_path = os.path.dirname(__file__) + '/log/' + str(nowtime) + api_path
        
        # 获取接口请求数据
        try:
            request_data = request.get_json(force=True)
        except Exception as e:
            request_data = request.form.to_dict()

        #request_data, response_data = str(request_data), str(response.json)
        logger.info('\n{} {}{}\n{}\n{} {}'.format(api_method,ip_addr,api_path,request_data,response.status_code,response.json))

        '''
        if not os.path.exists(log_path):
            # 如果不存在log目录则创建
            try:
                os.makedirs(log_path)
            except Exception as e:
                print('Error: when create log directory!')
                print(repr(e))
        with open(log_path + '/log.log', 'a+', encoding="utf-8") as f:
            asctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                asctime + " " + ip_addr + " " + api_method + " " + api_path + '->' + request_data + '\n' + response_data + '\n')
        '''
        return  response
    '''
    @app.teardown_request
    def teardown_request(error):
    # 数据库的扩展, 可以实现自动提交数据库
        print('teardown_request: error %s' % error)
    '''
    return app
