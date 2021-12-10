
from ..settings import wmsserver,wmsserver2
import json

import logging
logger = logging.getLogger("flask")

def reportfinish(data):
    import requests
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'charset':'utf-8',
    }
    logger.info("向wms发送请求{},{},{}）".format( wmsserver.T_URI,data ,headers))
    try:
        response = requests.request("POST", wmsserver.T_URI, json=data, headers=headers)
    except (Exception) as e:        
        return {"error":str(e)}, 400
    
    try:
        rdata = json.loads(response.text)
        logger.info("wms 返回数据（{}）,{}".format(rdata,response.status_code))
        if "MSG_TYPE" not in rdata:
            return  {"error":"MSG_TYPE 不在返回的数据中"}, 400
    except (Exception) as e:
        logger.info("wms 返回数据（{}）,{}".format(response.text,response.status_code))  
        logger.warning("wms 返回数据格式异常（{}）".format(str(e)))
        return {"error":str(e)}, 400  
 
    return rdata,response.status_code


def reporteport(data):
    '''
    三种情况：
    1、托盘就位，返回正常批号
    2、位置上不存在托盘，返回unready
    3、相机异常，返回error
    '''

    import requests
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'charset':'utf-8',
    }
    #return {"data":""},200
    flag = 1
    msg = 'success'
    d = None
    if data["data"] == 'unready':
        flag = 2
        msg = data["data"]
    elif data["data"] == 'error':
        flag = 3
        msg = data["data"]
    else:
        d = data["data"]
        pass

    rst = {"DeviceId":'{0:03d}'.format(data["dev"]),"Flag":flag,"Msg":msg,"BatchNo":d}
    
    try:
        response = requests.request("POST", wmsserver2.R_URI, json={"data":rst}, headers=headers)
    except (Exception) as e:

        return {"error":str(e)}, 400

    try:
        rdata = json.loads(response.text)
        logger.info("wms 返回数据（{}）,{}".format(rdata,response.status_code))
        if "code" not in rdata:
            return  {"error":"code 不在返回的数据中"}, 400
    except (Exception) as e:
        logger.info("wms 返回数据（{}）,{}".format(response.text,response.status_code))  
        logger.warning("wms 返回数据格式异常（{}）".format(str(e)))
        return {"error":str(e)}, 400  
    return rdata,response.status_code
    #return response.text.encode('latin-1').decode('gbk'),response.status_code

if __name__ == '__main__':
    pass
