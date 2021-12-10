#coding:utf-8
import logging
import requests
import json
from ..settings import cornserver
logger = logging.getLogger("flask")

headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }


def general_post(url,type,data):
    '''
    :param type: "GET" or "POST"
    :param data: JSON
    :return: rdata, response.status_code
    '''
    logger.info("send {} to corn: {},{},{}）".format(type, url, data, headers))
    try:
        if type == "POST":
            response = requests.request("POST",url, json=data, headers=headers)
        elif type == "GET":
            response = requests.request("GET",url, headers=headers)
        else:
            logger.info('requst type is abnormol: '+ str(type))
            return None, 400
    except (Exception) as e:
        return {"error": str(e)}, 400

    try:
        rdata = json.loads(response.content)
        logger.info("corn response data:（{}）,{}".format(rdata, response.status_code))
    except (Exception) as e:
        logger.info("corn response data:（{}）,{}".format(response.content, response.status_code))
        logger.warning("corn response data formate is abnormal:（{}）".format(str(e)))
        return {"error": str(e)}, 400

    return rdata, response.status_code

def assign_task_to_AGV(host,data):
    '''
        下发任务给AGV系统
    '''
    url = cornserver.assign_agv_task_url.format(host = host)
    rst, code = general_post(url,"POST",data)
    return rst, code



def update_i_flag_interaction(host,data):
    '''
        更新人工交互反馈表
    '''
    url = cornserver.update_i_flag_url.format(host = host)
    rst, code = general_post(url,"POST", data)
    return rst, code


def get_interaction_by_type(host,interaction_type_list):
    '''
    通过交互类型获取交互信息
    '''
    url = cornserver.get_interaction_url.format(host = host,interaction_type = interaction_type_list)
    rst, code = general_post(url, "GET", 1)
    return rst, code


def update_interaction_return_value(host,data):
    '''
    更新交互表返回值
    '''
    url = cornserver.update_dest_url.format(host = host)
    rst, code = general_post(url, "POST", data)
    return rst, code


def get_slave_info(host,loc_name):
    '''
    通过设备名获取modbus空闲情况
    '''
    url = cornserver.get_slaver_info_disurl.format(host = host,loc_name = loc_name)
    rst, code = general_post(url, "GET", 1)
    return rst, code


