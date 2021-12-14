from datetime import datetime

from ..base.dbcon.sqlserver import *
from flask import request, jsonify, url_for
from flask_restful import Resource, reqparse, Api
import json
import logging
logger = logging.getLogger("flask")

class FinishTask(Resource):
    def __init__(self):
        self.FINISH_SJ_TASK = f'''
                            BEGIN
                        DECLARE @issuccess int,@errmsg VARCHAR(100)
                        SET @issuccess=1
                        SET @errmsg = 'success'
                            EXEC SP_TRM_TaskSJ_Charge @TaskId = %(TaskId)s,@UserId = %(UserId)s,@ToLoc = %(ToLoc)s,@IP = %(IP)s,@ClientName = %(ClientName)s
                        IF @@ERROR<>0
                        BEGIN
                            SET @issuccess = 0
                            SET @errmsg = 'Insert Order ERROR!'
                        END
                            SELECT @issuccess as issuccess,@errmsg as errmsg
                            RETURN
                        END
                    '''

        self.FINISH_XJ_TASK = '''
            BEGIN
                        DECLARE @issuccess int,@errmsg VARCHAR(100)
                        SET @issuccess=1
                        SET @errmsg = 'success'
                            EXEC SP_TRM_TaskXJ_Charge @TaskId = %(TaskId)s,@UserId = %(UserId)s,@IP = %(IP)s,@ClientName = %(ClientName)s
                        IF @@ERROR<>0
                        BEGIN
                            SET @issuccess = 0
                            SET @errmsg = 'Insert Order ERROR!'
                        END
                            SELECT @issuccess as issuccess,@errmsg as errmsg
                            RETURN
                        END
            '''

        self.FINISH_OTHER_TASK = '''
                    BEGIN
                        DECLARE @issuccess int,@errmsg VARCHAR(100)
                        SET @issuccess=1
                        SET @errmsg = 'success'
                            UPDATE TRM_TaskOther SET Status='40',IsAgvCompleted=1,Version=Version+1,ModifyBy=%(UserId)s,ModifyDate=GETDATE() WHERE TaskId=%(TaskId)s AND Status='10'
                        IF @@ERROR<>0
                        BEGIN
                            SET @issuccess = 0
                            SET @errmsg = 'Insert Order ERROR!'
                        END
                            SELECT @issuccess as issuccess,@errmsg as errmsg
                            RETURN
                        END
            '''

    def post(self):
        response = {'MSG_TYPE': 'S',
                    'MSG_TXT': 'SUCCESS'
                    }
        list = []
        data = json.loads(request.get_data())
        app = '/FinishTask'
        time = datetime.now().strftime("%H:%M:%S")
        ip = request.remote_addr
        datas = data['data']
        logger.debug(str(data))
        dd = {}
        for i in datas:
            try:
                if i['ex']['TaskType'] == 'SJ':
                    dd = {}
                    for j in i.keys():
                        if j != 'ex':
                            dd[j] = i[j]
                    res = handle(Database.sqlserver,self.FINISH_SJ_TASK, dd)
                elif i['ex']['TaskType'] == 'XJ':
                    dd = {}
                    for j in i.keys():
                        if j != 'ex':
                            dd[j] = i[j]
                    res = handle(Database.sqlserver,self.FINISH_XJ_TASK, dd)
                elif i['ex']['TaskType'] == 'Other':
                    dd = {}
                    for j in i.keys():
                        if j != 'ex':
                            dd[j] = i[j]
                    try:
                        res = execute(Database.sqlserver,self.FINISH_OTHER_TASK, dd)
                        logger.debug(time + ' ' + ip + ' ' + app + '  ' + str(data) + ' ' + str(response))
                        return response, 200
                    except:
                        response['MSG_TYPE'] = 'S'
                        response['MSG_TXT'] = 'Finish Task Error!'
                        logger.debug(time + ' ' + ip + ' ' + app + '  ' + str(data) + ' ' + str(response))
                        return response, 204
                else:
                    response['MSG_TYPE'] = 'E'
                    response['MSG_TXT'] = 'TaskType is None!'
                    logger.debug(time + ' ' + ip + ' ' + app + '  ' + str(data) + ' ' + str(response))
                    return response, 200
                if res[0][0] == 1:
                    response['MSG_TYPE'] = 'S'
                    try:
                        response['MSG_TXT'] = str(res[0][1].encode('latin-1').decode('gbk'))
                    except:
                        response['MSG_TXT'] = str(res[0][1])
                else:
                    response['MSG_TYPE'] = 'S'
                    try:
                        response['MSG_TXT'] = str(res[0][1])
                    except:
                        response['MSG_TXT'] = str(res[0][1].encode('latin-1').decode('gbk'))
            except Exception as e:
                response['MSG_TYPE'] = 'S'
                response['MSG_TXT'] = str(e)
                logger.debug(time + ' ' + ip + ' ' + app + '  ' + str(data) + ' ' + str(response))
                return response, 500
        logger.debug(time + ' ' + ip + ' ' + app + '  ' + str(data) + ' ' + str(response))
        return response, 200

