#coding:utf-8


from ..corntask.sql_manager import *
from ..settings import Database,area_map
import logging
logger = logging.getLogger(__name__)

def get_empty_pallet_FromLoc(WHAreaId):
    '''
    叫空托订单，获取空托盘的起始位置
    check点要重新请求位置，因此此处可以随意给个空托盘位置
    :param WHAreaId:str
    :return: {'FromLoc':str, 'CID':str}
    '''

    get_empty_loc_sql = SQL.get_empty_pallet_loc.format(WHAreaId = WHAreaId)
    empty_loc_result = run_sql(get_empty_loc_sql)
    if empty_loc_result != []:
        empty_loc = empty_loc_result[0][0]
        cid = empty_loc_result[0][1]

    else:
        logger.warning('get_empty_pallet_FromLoc, there is no empty pallet for replen!!')
        return {'FromLoc':None, 'CID':None}

    # 维护库位状态
    update_loc_sql = SQL.update_location.format(Status = 'lock', OPT_By = 'get_empty_pallet_FromLoc()',LocationName = empty_loc)
    run_sql(update_loc_sql,'update')


    return {'FromLoc':empty_loc, 'CID':cid}


