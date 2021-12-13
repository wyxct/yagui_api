from flask import request, jsonify, url_for
from flask_restful import Resource, reqparse, Api
import json
from ..settings import orderserver
from  ..corntask.apscheduler_core import sched
import logging
logger = logging.getLogger('api')

from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime



class addropt(Resource):
    def __init__(self):
        pass   
    
    '''
    @发送modbus操作
    参数：ip,port,slave_id：,funccode ：,addr ：，len：，value:[]
    '''

    def post(self):

        from ..modbus import mtexcute

        #waiting/active/finish/e
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"格式错误，非json格式"}, 400

        if "port" not in data or  "ip" not in data or "slave" not in data or "funccode" not in data or "addr" not in data:
            return {"error":"缺少字段必要字段，检查slave_id：,funccode ：,addr，optlist"}, 400
        
        try:
            if "value" in data:
                value = mtexcute(data["ip"],data["port"],data["slave"],data["funccode"],data["addr"],data["len"],data["value"])
            else:
                value = mtexcute(data["ip"],data["port"],data["slave"],data["funccode"],data["addr"],data["len"] )

        except (Exception) as e:
            logger.error(str(e))
            return  {"error":"{}".format(str(e))}, 500

        return {"data":value}, 200


class functest(Resource):
    def __init__(self):
        pass   
    
    '''
    @api {get} /api/v1/p2ptasks/interaction/ 查询交互信息
    @apiVersion 0.0.0
    @apiName 查询交互信息
    @apiGroup p2ptasks
    '''
    def post(self):
         
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"格式错误，非json格式"}, 400

        type = data["type"] 
        dev = data["dev"]
        if type is  None or type =='' or dev is None or dev =='':
            return {"error":"缺少字段必要字段，检查type，dev"}, 400
        if type == 1:
            from ..modbus import get_string_batch
            flag,err = get_string_batch(dev)
        return {"batch":err},200

    



class p2ptasksgoon(Resource):
    def __init__(self):
        pass   
    
    '''
    @api {get} /api/v1/p2ptasks/p2ptasksgoon/ 任务继续
    @apiVersion 0.0.0
    @apiName 修改目的地
    @apiGroup p2ptasks

    interaction_info_id
    required
    integer (Interaction Info Id)
    交互信息的info ID

    info_status
    required string
    需要更新的交互信息状态
    return_value
    required
    '''

    def post(self):

        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"格式错误，非json格式"}, 400
        if "task_no" not in data or 'info_status' not in data:
            return {"error":"缺少字段必要字段，检查task_no是否存在"}, 400
        
        try:       
            from ..base.models.layer2_pallet_model import PlTask,PlTaskRelation
            from sqlalchemy import select,exists
             
            with sched.SessionFactory() as session:            
                statement = select(PlTask.task_no,PlTask.status,PlTask.ex,PlTaskRelation.relation).filter_by(task_no=data["task_no"]).join(PlTaskRelation.pl_task)
                result = session.execute(statement).all()
                session.commit()  
        
        except (Exception) as e:
            logger.error(str(e))           
            return {"error":"数据库异常，请联系相关人员"},500

        curorderno= None
        if result is None:
            return {'error': '任务不存在'}, 400
        for row in result:  
            curorderno = row.task_no
            break
        if curorderno is None:
            return {'error': 'order 未创建'}, 400     
        
        try:       
            sql = 'select * from layer4_1_om.interaction_info where interaction_info_type_id = 1 and info_status = \'active\' and interaction_info_name ={} order by interaction_info_id desc'.format(curorderno)        
            with sched.SessionFactory() as session:            
                cursor = session.execute(sql)
                ininfo = cursor.fetchall()
                session.commit()
        except (Exception) as e:
            logger.error(str(e))           
            return {"error":"数据库异常，请联系相关人员"},500

        cur_in = None
        for row in ininfo:
            cur_in = row.interaction_info_id
            break
            
        if cur_in is None:
                return {"error":'没有生成交互,或者已经完成'}, 400
        
                
        import requests
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        }

        tsdata=    {
        "interaction_info_id": cur_in,
        "info_status":data['info_status'],
        "return_value": 'done'
        }
        
        try:
            response = requests.request("POST", orderserver.C_URI, json=tsdata, headers=headers)
        except (Exception) as e:
            print(e)
            return {"error":str(e)}, 400
     


        print(response.status_code)
        print(response.text)

        return json.loads(response.text), response.status_code



  
class accessiblelocation(Resource):
    def __init__(self):
        pass   
    #如果是区域，需要重新建立映射关系
    def get(self):
        from ..modbus import get_data_sync
        from ..settings import modbus_cfg
        dev_no = "outloc"
        loc_n = request.args.get("loc_n") 

        if loc_n is  None or loc_n =='':
            return {"error":"loc_n 不存在"}, 400

        loc_n = loc_n.replace('[', '').replace(']', '')
        loc_list = loc_n.split(',')
        keymap ={}
        if modbus_cfg is None or dev_no not in modbus_cfg or "addrs" not in modbus_cfg[dev_no]or len(modbus_cfg[dev_no]["addrs"]) ==0:
            return {"error":"配置文件错误，缺少outloc或者outloc.addrs配置"},500
        
        addr_list =[]
        for row in loc_list:
            if row not in modbus_cfg[dev_no]["addrs"].keys():
                return {"error":"{} 不在配置文件中".format(row)},400
            else:
                addr = modbus_cfg[dev_no]["addrs"][row]
                keymap[addr] = row
                addr_list.append(addr)

        flag, data = get_data_sync(dev_no,addr_list)
        if flag == False:
            return {'error':data},500
        #0可以入
        rst ={}
        for key,value in data.items():
            if value == 0 :
                rst[keymap[key]] = []
                rst[keymap[key]].append(keymap[key])

        return  rst, 200

class Node(object):
    # 初始化一个节点
    def __init__(self,name = None,batch = None,equip = None):
        self.name = name  # 节点名称
        self.l = None  
        self.child_list = []    # 子节点列表

    def add_child(self,node):
        self.child_list.append(node)
    def del_child(self):
        self.child_list=[]  
    def set_parent(self,node):
        self.l =  node

class tasktracebackdetail(Resource):
    def __init__(self):
        self.mprocess = None
        pass
    def initmap(self,taskno):
        '''
        self.mprocess = [{'0':'{} 订单未下发'.format(taskno),'l':'-1'},
                    {'1':'{} 订单已接收'.format(taskno),'l':'0'},
                    {'2':'{} 订单已下发'.format(taskno),'l':'1'},
                    {'3':'{} 订单下发失败正在重发'.format(taskno),'l':'1'},
                    {'4':'{} 调度已分派车辆'.format(taskno),'l':'2'},
                    {'5':'{} agv开始执行'.format(taskno),'l':'4'},
                    {'6':'{} agv执行完成等待数据同步'.format(taskno),'l':'5'},
                    {'7':'{} 任务完成等待上报wms'.format(taskno),'l':'6'},
                    {'8':'{} 上报完成'.format(taskno),'l':'7'},
        ]
        '''
        self.mprocess = [{'0':'订单未下发','l':'-1'},
                    {'1':'订单已接收','l':'0'},
                    {'2':'订单已下发','l':'1'},
                    {'3':'订单下发失败正在重发','l':'1'},
                    {'4':'调度已分派车辆','l':'2'},
                    {'5':'agv开始执行','l':'4'},
                    {'6':'agv执行完成等待数据同步','l':'5'},
                    {'7':'任务完成等待上报wms','l':'6'},
                    {'8':'上报完成','l':'7'},
        ]
        index ={}
        for row in self.mprocess:
            #tmep = None
            for key,value in row.items():              
                if key not in index and key !='-1':
                    tmep = Node(key)
                    index[key] = tmep
                    no = key
                if key =='l' and value != '-1':
                    index[value].add_child(tmep)
                    index[no].set_parent(index[value])
        return index
    
    def searchsql(self,taskno):
        sql = '''
        with "taskinfo" as
        (
            select '{}'::character varying as taskno
        ),
        "pl" as(
            select pt.id,pt.task_type,pt.task_no,pt.from_pos, pt.to_pos, pt.start_time, pt.end_time, 
            pt.pos_list, pt.next_pos, pt.status, pt.priority, pt.cid, pt.cid_attribute, pt.custom_parm1, 
            pt.custom_parm2, pt.source, pt.ip, pt.client_name, pt.client_type, pt.memo, pt.ex, 
            pt.optlist,ptr.relation,ptrp.id as report_id from pl_task as pt 
            left join pl_task_relation as ptr on pt.id = ptr.pl_task_id 
            left join pl_task_report as ptrp on pt.id =  ptrp.pl_task_id
            where task_no = (select taskinfo.taskno from taskinfo)
        ),
        "ordertask" as (
            select order_id,order_name,agv_list,ts_id,status,current_destination,current_operation,current_omi,create_time,active_time,finished_time,cancel_time,error_code
            from layer4_1_om."order" where order_name = (select taskinfo.taskno from taskinfo)
        )
        --select ordertask.order_id::character varying from ordertask
        ,
        "agvtask" as (
            select *,loc.location_name from agv_task as at 
            left join agv_task_execution_data as ated on at.id = ated.agv_task_id
            inner join location as loc on loc.id = at.destination_location_id
            where task_set_no = (select ordertask.order_id::character varying from ordertask)
        ),
        "agvcmd" as (
            select * from agv_command where id in (select agvtask.current_agv_command_id from agvtask)
        )
        select ordertask.order_name,agv_list,ordertask.ts_id,ordertask.status,ordertask.current_destination,ordertask.current_operation,
        ordertask.current_omi,ordertask.create_time::character varying,ordertask.active_time::character varying,ordertask.finished_time::character varying,ordertask.cancel_time::character varying,ordertask.error_code,
        (case 
        when (select count(*) from pl)=0 then '0' 
        when (select pl.relation from pl) is NULL then '3'
        when (select ordertask.error_code from ordertask) is not NULL then 'e'
        when (select count(*) from agvtask)=0 then '2'
        when (select count(*) from agvcmd)=0 then '4'
        when (select ordertask.status from ordertask) not in ('finish','manually_finish') then '5'
        when (select pl.status from pl) != 'completed' then '6'
        when (select pl.report_id from pl) is NULL then '7'
        when (select pl.report_id from pl) is not NULL then '8'
        else '其他' end) as process
        from ordertask
        '''.format(taskno)
        return sql
    
    def get(self,taskno):
           
        #print(str(orderlist).lstrip('[').rstrip(']'))
        
        sql = self.searchsql(taskno)
        promap =  self.initmap(taskno)  
        cmppro = []


        try:
            from sqlalchemy import select,exists
            with sched.SessionFactory() as session:            
                cursor = session.execute(sql)
                orderinfo = cursor.all()
                session.commit()

        except (Exception) as e:
            logger.error(str(e))
            return  {"error":"数据库查询异常"}, 500

        data = [dict(zip(ininfo.keys(),ininfo)) for ininfo in orderinfo]
        resdata = {"process":[],"info":{}}
        from ..base.errormap import ordererror
        if len(data)==0:
            return  {'error':"未查到信息"}, 404
        for  row in data:
            if row["process"] == 'e':
                if row["error_code"] in ordererror:
                    row["reason"] = ordererror[str(row["error_code"])]
                else:
                    row["reason"] = 'unkonw'
                break    
            node = promap[row["process"]]
            cmppro.append(node.name)
            while True:
                if node.l is None:
                    break
                else:
                    node = promap[node.l.name]
                    cmppro.append(node.name)
            resdata["process"] = cmppro
            resdata["info"] = row
            resdata["map"] = self.mprocess
            break
        
        return  resdata, 200
  
class tasktraceback(Resource):
    
    def __init__(self):
        pass   

    def get(self):
       
        offset = request.args.get("offset") 
        limit = request.args.get("limit")
        offset = 0 if offset is None else offset
        limit = 100 if limit is None else limit

        import re
        import json
   

        try:       
            from ..base.models.layer2_pallet_model import  PlTask,PlTaskType,PlTaskRelation,PlTaskReport
            from sqlalchemy import select,exists
             
            with sched.SessionFactory() as session:            
                statement = select(PlTask.id,PlTask.task_no,PlTask.task_type,PlTask.status,PlTask.priority,PlTask.ex,PlTaskRelation.relation).outerjoin(PlTaskRelation).filter(PlTask.status.in_(['created','handle','active', 'in_progress','completed','error'])).order_by(PlTask.id).offset(offset).limit(limit)
                result = session.execute(statement).all()
                session.commit()     
        except (Exception) as e:
            logger.error(str(e))           
            return {"error":"数据库异常，请联系相关人员"},500

        import copy
        orderlist=[]
        tasktmp = {"task_no":None,"agv_list":None,"status":None,"cur_dest":None,"cur_omi":"","c_t":None,"a_t":None,"cel_t":None,"fin_t":None,"reason":None,"err_code":0}
        taskdict = {}
        rstdata = {}
        for row in result:
            tasktmp["task_no"] = row.task_no
            tasktmp["status"] = row.status 
            if row.relation is None:
                tasktmp["reason"] = "未下发给OM" 
            else:               
                orderlist.append(row.relation)
                taskdict[row.relation] = row
            rstdata[row.task_no] = copy.deepcopy(tasktmp)

        #获取活跃任务对应的order
        if len(orderlist) == 0:
            print("empty")
            return rstdata, 200
        #print(str(orderlist).lstrip('[').rstrip(']'))
        sql = 'select * from layer4_1_om.order where order_name in({})'.format(str(orderlist).lstrip('[').rstrip(']'))
        #print(sql)
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            orderinfo = cursor.fetchall()
            session.commit()
        #waiting/active/finish/error/waiting_cancel/cancel_finish/waiting_manually_finish/manually_finish

        for row in orderinfo:
            #处理未发送成功的
            rstdata[row.order_name]["agv_list"] = row.agv_list
            rstdata[row.order_name]["cur_dest"] = row.current_destination
            rstdata[row.order_name]["cur_omi"] = row.current_omi
            rstdata[row.order_name]["c_t"] = row.create_time.strftime('%Y-%m-%d %H:%M:%S') if row.create_time is not None else ''
            rstdata[row.order_name]["a_t"] = row.active_time.strftime('%Y-%m-%d %H:%M:%S') if row.active_time is not None else ''
            rstdata[row.order_name]["cel_t"] = row.cancel_time.strftime('%Y-%m-%d %H:%M:%S') if row.cancel_time is not None else ''
            rstdata[row.order_name]["fin_t"] = row.finished_time.strftime('%Y-%m-%d %H:%M:%S') if row.finished_time is not None else ''
            rstdata[row.order_name]["err_code"] = row.error_code if row.error_code is not None else 0
            if row.status == 'error':
                rstdata[row.order_name]["status"] = row.status
                pass
            elif row.status == 'finish' or row.status == 'manually_finish':
                if rstdata[row.order_name]["status"] != 'completed':
                   rstdata[row.order_name]["reason"] = "数据尚未同步，长期不同步需要检查监控定时任务"  
                else:
                    with sched.SessionFactory() as session:            
                        statement = select(PlTaskReport.id).filter(~exists().where(PlTaskReport.pl_task_id ==taskdict[row.order_name].id))
                        result = session.execute(statement).all()
                        session.commit()
                    rstdata[row.order_name]["reason"] = "数据未上报给wms"
            else:
                rstdata[row.order_name]["status"] = row.status

        return  rstdata, 200