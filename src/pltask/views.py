from flask import request, jsonify, url_for
from flask_restful import Resource, reqparse, Api
import json
from ..settings import orderserver
from  ..corntask.apscheduler_core import sched
import logging
logger = logging.getLogger('api')

class p2ptasks(Resource):
    def __init__(self):
        pass   
    
    '''
    @api {post} /api/v1/p2ptasks/ 点任务
    @apiVersion 0.0.0
    @apiName cancel_pltasks
    @apiGroup pltasks
    '''

    def post(self):
        from ..base.models.layer2_pallet_model import PlTask,PlTaskType,PlTaskRelation
         
        from sqlalchemy import select,exists

        #waiting/active/finish/e
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"格式错误，非json格式"}, 400

        if "task_no" not in data or "task_type" not in data or "optlist" not in data:
            return {"error":"缺少字段必要字段，检查task_no，task_type，optlist"}, 400
       
        try:
            with sched.SessionFactory() as session:      
                statement = select(PlTaskType.task_type,PlTaskType.ts_map).filter_by(task_type = data["task_type"])      
                tasktsmap = session.execute(statement).all()
                session.commit()     


            if tasktsmap is None:
                return {"error":"不存在的类型"}, 400
        
            #t = PlTask.query.filter_by(task_no=data["task_no"]).first()
            with sched.SessionFactory() as session:      
                statement = select(PlTask.id).filter_by(task_no=data["task_no"])      
                t = session.execute(statement).first()
                statement2 = select(PlTask.id,PlTaskRelation.relation).filter_by(task_no=data["task_no"]).outerjoin(PlTaskRelation)
                d = session.execute(statement2).first()
                session.commit()     
        except (Exception) as e:
            logger.error(str(e))
            return {"error":"数据库异常，请联系相关人员"},500

        
        if t is not None:
      
            if d is None:
                return {'error': 'om 异常无法生成order'}, 200
            return {'task_no': data["task_no"]}, 200

        try:
            task = PlTask()
            task.task_no = data["task_no"]
            task.task_type = data["task_type"]
            task.optlist = {"optlist":data["optlist"]}
            task.ex = None if "ex" not in data else json.dumps(data["ex"])
            task.status = "created" if "status" not in data else data["status"]
            task.priority = 0 if "priority" not in data else data["priority"]
            with sched.SessionFactory() as session:      
                session.add(task)
                session.commit()
                session.flush()   

        except (Exception) as e:
            logger.error(str(e))
            pass

        optdict = {}
        idx = 0
        for row in data["optlist"]:
            idx = idx + 1 
            optdict[str(idx)] = row

  
        order_json = {
        "task_no": data["task_no"],
        "priority": data["priority"] if "priority" in data  else 0,
        "dead_line": "2020-02-01 16:00:00",
        "ts_name": tasktsmap.ts_map,
        "parameters": json.dumps({"optlist":json.dumps(optdict)}),
        "uid":hash(data["task_no"])
        }
        from ..base.dispatchapi import sendorder

        redata,recode = sendorder(order_json)
 
        if recode == 200:
            #order_id = json.loads(response.text)["data"]
            if task.id is not None:
                try:
                    pltaskr = PlTaskRelation(relation = data["task_no"],pl_task_id = task.id)
                    with sched.SessionFactory() as session:      
                        session.add(pltaskr)
                        session.commit()
                        session.flush()   

                except (Exception) as e:
                    logger.error(str(e))
                    pass
                

            return {'task_no': data["task_no"]}, 200
        else:
            logger.warning("创建order异常（{}）,将自动重试".format(data["task_no"]))
            return redata, recode


class p2ptasksInteractio(Resource):
    def __init__(self):
        pass   
    
    '''
    @api {get} /api/v1/p2ptasks/interaction/ 查询交互信息
    @apiVersion 0.0.0
    @apiName 查询交互信息
    @apiGroup p2ptasks
    '''
    def get(self):
         
        type_id = request.args.get("type_id") 
        info_status = request.args.get("info_status") 
        if type_id is  None or info_status is  None:
            return {"error":"缺少字段必要字段，检查info_status，type_id"}, 400

        import requests
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        }
        type_id = type_id.replace('[', '').replace(']', '')
        sql = 'select * from layer4_1_om.interaction_info where interaction_info_type_id in ({}) and info_status = \'{}\'  order by interaction_info_id '.format(type_id,info_status)

        try:
            with sched.SessionFactory() as session:            
                cursor = session.execute(sql)
                orderinfo = cursor.fetchall()
                session.commit()
        except (Exception) as e:
            logger.error(str(e))           
            return {"error":"数据库异常，请联系相关人员"},500

        data = [dict(zip(ininfo.keys(),ininfo)) for ininfo in orderinfo]
        return {"data":data},200

    
    def post(self):

        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error":"格式错误，非json格式"}, 400
        if "interaction_info_id" not in data or "info_status" not in data or "return_value" not in data:
            return {"error":"缺少字段必要字段，检查interaction_info_id，info_status，"}, 400
            
        import requests
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        }

        tsdata=    {
        "interaction_info_id": data['interaction_info_id'],
        "info_status":data['info_status'],
        "return_value": data['return_value']
        }
        
        try:
            response = requests.request("POST", orderserver.C_URI, json=tsdata, headers=headers)
        except (Exception) as e:
            print(e)
            return {"error":str(e)}, 400
     

        print(response.status_code)
        print(response.text)

        return json.loads(response.text), response.status_code



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
        self.batch = batch  
        self.equip = equip  
        self.child_list = []    # 子节点列表

    def add_child(self,node):
        self.child_list.append(node)
    def del_child(self):
        self.child_list=[]  

class tasktracebackdetail(Resource):
    def __init__(self):
        __process = [{'1':''},
        ]   

    def get(self,taskno):
        
        #print(str(orderlist).lstrip('[').rstrip(']'))
        sql = '''
    with "taskinfo" as
    (
        select '{}'::character varying as taskno
    ),
    --select taskinfo.taskno from taskinfo
    "pl" as(
        select pt.id,pt.task_type,pt.task_no,pt.from_pos, pt.to_pos, pt.start_time, pt.end_time, 
        pt.pos_list, pt.next_pos, pt.status, pt.priority, pt.cid, pt.cid_attribute, pt.custom_parm1, 
        pt.custom_parm2, pt.source, pt.ip, pt.client_name, pt.client_type, pt.memo, pt.ex, 
        pt.optlist,ptr.relation,ptrp.id as report_id from pl_task as pt 
        left join pl_task_relation as ptr on pt.id = ptr.pl_task_id 
        left join pl_task_report as ptrp on pt.id =  ptrp.pl_task_id
        where task_no = (select taskinfo.taskno from taskinfo)
    ),
    --select * from pl 
    "ordertask" as (
        select * from layer4_1_om."order" where order_name = (select taskinfo.taskno from taskinfo)
    )
    --select ordertask.order_id::character varying from ordertask
    ,
    --select * from ordertask
    "agvtask" as (
        select *,loc.location_name from agv_task as at 
        left join agv_task_execution_data as ated on at.id = ated.agv_task_id
        inner join location as loc on loc.id = at.destination_location_id
        where task_set_no = (select ordertask.order_id::character varying from ordertask)
    ),
    "agvcmd" as (
        select * from agv_command where id in (select agvtask.current_agv_command_id from agvtask)
    )
    select case 
    when (select count(*) from pl)=0 then '订单未下发' 
    when (select pl.relation from pl) is NULL then 'om接收任务不成功，正在尝试重发'
    when (select ordertask.error_code from ordertask) is not NULL then (select ordertask.error_code from ordertask)::character varying
    when (select count(*) from agvtask)=0 then 'om未下发'
    when (select count(*) from agvcmd)=0 then '调度未派车'
    when (select ordertask.status from ordertask) not in ('finish','manually_finish') then '进行中'
    when (select pl.status from pl) != 'completed' then '等待同步'
    when (select pl.report_id from pl) is NULL then '等待上报'
    when (select pl.report_id from pl) is not NULL then '上报完成'
    else '其他' end 
        '''.format(taskno)
        
         
        from sqlalchemy import select,exists
        with sched.SessionFactory() as session:            
            cursor = session.execute(sql)
            orderinfo = cursor.fetchall()
            session.commit()
        #waiting/active/finish/error/waiting_cancel/cancel_finish/waiting_manually_finish/manually_finish

        return  {}, 200
  
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