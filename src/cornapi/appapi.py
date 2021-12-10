#coding:utf-8
import logging
import requests
import json
logger = logging.getLogger("flask")


headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

def get_replen_ToLoc(task_id):
    '''
        齐鲁石化入库请求定制，由于不知道货物属性，不知道第二层是否能放货物
        通过接口跟app交互获取放货目的地，反馈给AGV系统
        :param task_id: 上架单编号
        :return: 可放置的空位 or None
    '''
    from ..settings import appserver
    data_json =  { "app_name": "AGV",
                    "data": {
                    "TaskId": task_id}
                  }
    empty_loc = None
    logger.info("send post to app: {},{},{}）".format(appserver.get_to_loc_URI, data_json, headers))
    try:
        response = requests.request("POST", appserver.get_to_loc_URI, json=data_json, headers=headers)
    except (Exception) as e:
        logger.warning("app response data formate is abnormal:（{}）".format(str(e)))
        return None

    try:
        rdata = json.loads(response.content)
        logger.info("app response data:（{}）,{}".format(rdata, response.status_code))
        if rdata.get('code',-1) == 0 and response.status_code == 200:
            empty_loc =  rdata.get('data',{}).get('LocationId',None)
            return empty_loc

    except (Exception) as e:
        logger.info("app response data:（{}）,{}".format(response.content, response.status_code))
        logger.warning("app response data formate is abnormal:（{}）".format(str(e)))
        return None

    return empty_loc

