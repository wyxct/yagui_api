from flask import request
from flask_restful import Resource
import json
from ..settings import orderserver
from ..corntask.apscheduler_core import sched
import logging

logger = logging.getLogger('api')

from datetime import datetime


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
        from ..base.models.layer2_pallet_model import PlTask, PlTaskType, PlTaskRelation

        from sqlalchemy import select, exists

        # waiting/active/finish/e
        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error": "格式错误，非json格式"}, 400

        if "task_no" not in data or "task_type" not in data or "optlist" not in data:
            return {"error": "缺少字段必要字段，检查task_no，task_type，optlist"}, 400

        try:
            with sched.SessionFactory() as session:
                statement = select(PlTaskType.task_type, PlTaskType.ts_map).filter_by(task_type=data["task_type"])
                tasktsmap = session.execute(statement).all()
                session.commit()

            if tasktsmap is None:
                return {"error": "不存在的类型"}, 400

            # t = PlTask.query.filter_by(task_no=data["task_no"]).first()
            with sched.SessionFactory() as session:
                statement = select(PlTask.id).filter_by(task_no=data["task_no"])
                t = session.execute(statement).first()
                statement2 = select(PlTask.id, PlTaskRelation.relation).filter_by(task_no=data["task_no"]).outerjoin(
                    PlTaskRelation)
                d = session.execute(statement2).first()
                session.commit()
        except (Exception) as e:
            logger.error(str(e))
            return {"error": "数据库异常，请联系相关人员"}, 500

        if t is not None:

            if d is None:
                return {'error': 'om 异常无法生成order'}, 200
            return {'task_no': data["task_no"]}, 200

        try:
            task = PlTask()
            task.task_no = data["task_no"]
            task.task_type = data["task_type"]
            task.source = data["source"] if "source" in data and data["source"] != '' else None
            task.client_name = data["client_name"] if "client_name" in data and data["client_name"] != '' else None
            task.optlist = {"optlist": data["optlist"]}
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
            "priority": data["priority"] if "priority" in data else 0,
            "dead_line": "2020-02-01 16:00:00",
            "ts_name": tasktsmap.ts_map,
            "parameters": json.dumps({"optlist": json.dumps(optdict)}),
            "uid": hash(data["task_no"])
        }
        from ..base.dispatchapi import sendorder

        redata, recode = sendorder(order_json)

        if recode == 200:
            # order_id = json.loads(response.text)["data"]
            if task.id is not None:
                try:
                    pltaskr = PlTaskRelation(relation=data["task_no"], pl_task_id=task.id)
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
        if type_id is None or info_status is None:
            return {"error": "缺少字段必要字段，检查info_status，type_id"}, 400

        import requests
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }
        type_id = type_id.replace('[', '').replace(']', '')
        sql = 'select * from layer4_1_om.interaction_info where interaction_info_type_id in ({}) and info_status = \'{}\'  order by interaction_info_id '.format(
            type_id, info_status)

        try:
            with sched.SessionFactory() as session:
                cursor = session.execute(sql)
                orderinfo = cursor.fetchall()
                session.commit()
        except (Exception) as e:
            logger.error(str(e))
            return {"error": "数据库异常，请联系相关人员"}, 500

        data = [dict(zip(ininfo.keys(), ininfo)) for ininfo in orderinfo]
        return {"data": data}, 200

    def post(self):

        try:
            data = json.loads(request.data)
        except (Exception) as e:
            print(e)
            return {"error": "格式错误，非json格式"}, 400
        if "interaction_info_id" not in data or "info_status" not in data or "return_value" not in data:
            return {"error": "缺少字段必要字段，检查interaction_info_id，info_status，"}, 400

        import requests
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        tsdata = {
            "interaction_info_id": data['interaction_info_id'],
            "info_status": data['info_status'],
            "return_value": data['return_value']
        }

        try:
            response = requests.request("POST", orderserver.C_URI, json=tsdata, headers=headers)
        except (Exception) as e:
            print(e)
            return {"error": str(e)}, 400

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
            return {"error": "格式错误，非json格式"}, 400
        if "task_no" not in data or 'info_status' not in data:
            return {"error": "缺少字段必要字段，检查task_no是否存在"}, 400

        try:
            from ..base.models.layer2_pallet_model import PlTask, PlTaskRelation
            from sqlalchemy import select, exists

            with sched.SessionFactory() as session:
                statement = select(PlTask.task_no, PlTask.status, PlTask.ex, PlTaskRelation.relation).filter_by(
                    task_no=data["task_no"]).join(PlTaskRelation.pl_task)
                result = session.execute(statement).all()
                session.commit()

        except (Exception) as e:
            logger.error(str(e))
            return {"error": "数据库异常，请联系相关人员"}, 500

        curorderno = None
        if result is None:
            return {'error': '任务不存在'}, 400
        for row in result:
            curorderno = row.task_no
            break
        if curorderno is None:
            return {'error': 'order 未创建'}, 400

        try:
            sql = 'select * from layer4_1_om.interaction_info where interaction_info_type_id = 2 and info_status = \'active\' and interaction_info_name =\'{}\' order by interaction_info_id desc'.format(
                curorderno)
            with sched.SessionFactory() as session:
                cursor = session.execute(sql)
                ininfo = cursor.fetchall()
                session.commit()
        except (Exception) as e:
            logger.error(str(e))
            return {"error": "数据库异常，请联系相关人员"}, 500

        cur_in = None
        for row in ininfo:
            cur_in = row.interaction_info_id
            break

        if cur_in is None:
            return {"error": '没有生成交互,或者已经完成'}, 400

        import requests
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        tsdata = {
            "interaction_info_id": cur_in,
            "info_status": data['info_status'],
            "return_value": 'done'
        }

        try:
            response = requests.request("POST", orderserver.C_URI, json=tsdata, headers=headers)
        except (Exception) as e:
            print(e)
            return {"error": str(e)}, 400

        print(response.status_code)
        print(response.text)

        return json.loads(response.text), response.status_code


class accessiblelocation(Resource):
    def __init__(self):
        pass
        # 如果是区域，需要重新建立映射关系

    def get(self):
        from ..modbus import get_data_sync
        from ..settings import modbus_cfg
        dev_no = "outloc"
        loc_n = request.args.get("loc_n")

        if loc_n is None or loc_n == '':
            return {"error": "loc_n 不存在"}, 400

        loc_n = loc_n.replace('[', '').replace(']', '')
        loc_list = loc_n.split(',')
        keymap = {}
        if modbus_cfg is None or dev_no not in modbus_cfg or "addrs" not in modbus_cfg[dev_no] or len(
                modbus_cfg[dev_no]["addrs"]) == 0:
            return {"error": "配置文件错误，缺少outloc或者outloc.addrs配置"}, 500

        addr_list = []
        for row in loc_list:
            if row not in modbus_cfg[dev_no]["addrs"].keys():
                return {"error": "{} 不在配置文件中".format(row)}, 400
            else:
                addr = modbus_cfg[dev_no]["addrs"][row]
                keymap[addr] = row
                addr_list.append(addr)

        flag, data = get_data_sync(dev_no, addr_list)
        if flag == False:
            return {'error': data}, 500
        # 0可以入
        rst = {}
        for key, value in data.items():
            if value == 0:
                rst[keymap[key]] = []
                rst[keymap[key]].append(keymap[key])

        return rst, 200


class Node(object):
    # 初始化一个节点
    def __init__(self, name=None):
        self.name = name  # 节点名称
        self.l = None
        self.child_list = []  # 子节点列表

    def add_child(self, node):
        self.child_list.append(node)

    def del_child(self):
        self.child_list = []

    def set_parent(self, node):
        self.l = node


class tasktracebackdetail(Resource):
    """
                    @api {GET} /api/p2ptasks/tasktraceback/{taskid} 查看Agv链路细节
                    @apiVersion 1.0.0
                    @apiName Agv_Links
                    @apiGroup pltask
                    @apiDescription 用于查看Agv运行到什么程度下了，便于查问题

                    @apiSuccess {Object} status 状态码
                    @apiSuccess {Object} process 走过的链路
                    @apiSuccess {Object} info 订单细节
                    @apiSuccess {Object} map 完整的链路
                    @apiSuccessExample {Json} 成功返回:
                        HTTP 1.1/ 200K
                        {
                        "process": [
                            "13",
                            "12",
                            "11",
                            "10",
                            "9",
                            "8",
                            "7",
                            "6",
                            "5",
                            "4",
                            "2",
                            "1",
                            "0"
                        ],
                        "info": {
                            "order_name": "TSJ11111211021000100992",
                            "agv_list": [
                                2
                            ],
                            "ts_id": "multi_point_task",
                            "status": "finish",
                            "current_destination": "RA-01-01-01(1)",
                            "current_operation": "1",
                            "current_omi": "goto_location(RA-01-01-01,True)",
                            "create_time": "2021-11-12 16:48:09.620617+08",
                            "active_time": "2021-11-12 16:48:10.987838+08",
                            "finished_time": "2021-11-12 17:09:19.988596+08",
                            "cancel_time": null,
                            "error_code": null,
                            "process": "13"
                        },
                        "map": [
                            {
                                "id": "0",
                                "label": "订单未下发",
                                "l": "-1"
                            },
                            {
                                "id": "1",
                                "label": "订单已接收",
                                "l": "0"
                            },
                            {
                                "id": "2",
                                "label": "订单已下发",
                                "l": "1"
                            },
                            {
                                "id": "3",
                                "label": "订单下发失败正在重发",
                                "l": "1"
                            },
                            {
                                "id": "4",
                                "label": "调度已分派车辆",
                                "l": "2"
                            },
                            {
                                "id": "5",
                                "label": "AGV开始执行",
                                "l": "4"
                            },
                            {
                                "id": "6",
                                "label": "AGV已经生成前往取货点S1-04-01-01的任务",
                                "l": "5"
                            },
                            {
                                "id": "7",
                                "label": "AGV正在前往取货点S1-04-01-01",
                                "l": "6"
                            },
                            {
                                "id": "8",
                                "label": "AGV已经生成前往货区LC-02-01-01的任务",
                                "l": "7"
                            },
                            {
                                "id": "9",
                                "label": "AGV正在前往货区LC-02-01-01",
                                "l": "8"
                            },
                            {
                                "id": "10",
                                "label": "AGV已经生成前往卸货点RA-01-01-01的任务",
                                "l": "9"
                            },
                            {
                                "id": "11",
                                "label": "AGV正在前往卸货点RA-01-01-01",
                                "l": "10"
                            },
                            {
                                "id": "12",
                                "label": "AGV执行任务完成等待数据同步",
                                "l": "11"
                            },
                            {
                                "id": "13",
                                "label": "任务完成等待上报WMS",
                                "l": "12"
                            },
                            {
                                "id": "14",
                                "label": "任务上报完成",
                                "l": "13"
                            }
                        ]
                    }

                    @apiErrorExample Response-Fail:
                        HTTP 1.1/ 404K
                        {
                            'msg': 'Fail'
                        }
                    """
    def __init__(self):
        self.aprocess = [{'id': '0', 'label': '订单未下发', 'l': '-1'},
                         {'id': '1', 'label': '订单已接收', 'l': '0'},
                         {'id': '2', 'label': '订单已下发', 'l': '1'},
                         {'id': '3', 'label': '订单下发失败正在重发', 'l': '1'},
                         {'id': '4', 'label': '调度已分派车辆', 'l': '2'},
                         {'id': '5', 'label': 'AGV开始执行', 'l': '4'},
                         ]
        self.mprocess = [{'0': '订单未下发', 'l': '-1'},
                         {'1': '订单已接收', 'l': '0'},
                         {'2': '订单已下发', 'l': '1'},
                         {'3': '订单下发失败正在重发', 'l': '1'},
                         {'4': '调度已分派车辆', 'l': '2'},
                         {'5': 'AGV开始执行', 'l': '4'},
                         ]
        self.location = {'load': None, 'check': None, 'unload': None}
        pass

    def initmap(self, taskno, pl_list):
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
        index = {}
        for row in self.mprocess:
            # tmep = None
            for key, value in row.items():
                if key not in index and key != '-1':
                    tmep = Node(key)
                    index[key] = tmep
                    no = key
                if key == 'l' and value != '-1':
                    index[value].add_child(tmep)
                    index[no].set_parent(index[value])
        return index

    def searchlocationsql(self, taskno):
        sql = '''
            select pt.optlist from pl_task as pt 
            left join pl_task_relation as ptr on pt.id = ptr.pl_task_id 
            left join pl_task_report as ptrp on pt.id =  ptrp.pl_task_id
            where task_no = '{}'
        '''.format(taskno)
        return sql

    def searchsql(self, taskno):
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
        when (select ordertask.error_code from ordertask) is not NULL then '999'
        when (select count(*) from agvtask)=0 then '2'
        when (select count(*) from agvcmd)=0 then '4'
        when (select ordertask.status from ordertask) not in ('finish','manually_finish') then '5'
        '''.format(taskno)
        return sql

    def get(self, taskno):

        # print(str(orderlist).lstrip('[').rstrip(']'))

        sql = self.searchsql(taskno)
        location_sql = self.searchlocationsql(taskno)
        cmppro = []

        try:
            from sqlalchemy import select, exists
            session = sched.SessionFactory()
            cursor = session.execute(location_sql)
            location_dict = cursor.fetchall()
            session.commit()

        except (Exception) as e:
            logger.error(str(e))
            return {"error": "数据库查询异常"}, 500
        try:
            location_dict = location_dict[0][0]
            print(location_dict)
            start = 5
            load_time = 1
            unload_time = 1
            check_time = 1
            for i in location_dict['optlist']:
                if i['opt'] == 'load':
                    try:  # 如果去的位置不存在check点的，直接跳过逻辑
                        self.aprocess.append(
                            {'id': str(start + 1), 'label': 'AGV已经生成前往货区{}的任务'.format(i['check_point']),
                             'l': str(start)})
                        self.mprocess.append(
                            {str(start + 1): 'AGV已经生成前往货区{}的任务'.format(i['check_point']), 'l': str(start)})
                        sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = -1 and agvcmd.agv_command_status_id=10)=1 and (select count(*) from agvcmd where parameter_int4_2 = -1)={} then '{}'\n".format(
                            check_time, str(start + 1))
                        start += 1
                        self.aprocess.append(
                            {'id': str(start + 1), 'label': 'AGV正在前往货区{}'.format(i['check_point']), 'l': str(start)})
                        self.mprocess.append({str(start + 1): 'AGV正在前往货区{}'.format(i['check_point']), 'l': str(start)})
                        sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = -1 and agvcmd.agv_command_status_id=11)=1 and (select count(*) from agvcmd where parameter_int4_2 = -1)={} then '{}'\n".format(
                            check_time, str(start + 1))
                        start += 1
                        check_time += 1
                    except:
                        pass
                    self.aprocess.append(
                        {'id': str(start + 1), 'label': 'AGV已经生成前往取货点{}的任务'.format(i['pos']), 'l': str(start)})
                    self.mprocess.append({str(start + 1): 'AGV已经生成前往取货点{}的任务'.format(i['pos']), 'l': str(start)})
                    sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = 2 and agvcmd.agv_command_status_id=10)=1 and (select count(*) from agvcmd where parameter_int4_2 = 2)={} then '{}'\n".format(
                        load_time, str(start + 1))
                    start += 1
                    self.aprocess.append(
                        {'id': str(start + 1), 'label': 'AGV正在前往取货点{}'.format(i['pos']), 'l': str(start)})
                    self.mprocess.append({str(start + 1): 'AGV正在前往取货点{}'.format(i['pos']), 'l': str(start)})
                    sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = 2 and agvcmd.agv_command_status_id=11)=1 and (select count(*) from agvcmd where parameter_int4_2 = 2)={} then '{}'\n".format(
                        load_time, str(start + 1))
                    start += 1
                    load_time += 1
                elif i['opt'] == 'unload':
                    try:  # 如果去的位置不存在check点的，直接跳过逻辑
                        self.aprocess.append(
                            {'id': str(start + 1), 'label': 'AGV已经生成前往货区{}的任务'.format(i['check_point']),
                             'l': str(start)})
                        self.mprocess.append(
                            {str(start + 1): 'AGV已经生成前往货区{}的任务'.format(i['check_point']), 'l': str(start)})
                        sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = -1 and agvcmd.agv_command_status_id=10)=1 and (select count(*) from agvcmd where parameter_int4_2 = -1)={} then '{}'\n".format(
                            check_time, str(start + 1))
                        start += 1
                        self.aprocess.append(
                            {'id': str(start + 1), 'label': 'AGV正在前往货区{}'.format(i['check_point']), 'l': str(start)})
                        self.mprocess.append({str(start + 1): 'AGV正在前往货区{}'.format(i['check_point']), 'l': str(start)})
                        sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = -1 and agvcmd.agv_command_status_id=11)=1 and (select count(*) from agvcmd where parameter_int4_2 = -1)={} then '{}'\n".format(
                            check_time, str(start + 1))
                        start += 1
                        check_time += 1
                    except:
                        pass
                    self.aprocess.append(
                        {'id': str(start + 1), 'label': 'AGV已经生成前往卸货点{}的任务'.format(i['pos']), 'l': str(start)})
                    self.mprocess.append({str(start + 1): 'AGV已经生成前往卸货点{}的任务'.format(i['pos']), 'l': str(start)})
                    sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = 1 and agvcmd.agv_command_status_id=10)=1 and (select count(*) from agvcmd where parameter_int4_2 = 1)={} then '{}'\n".format(
                        unload_time, str(start + 1))
                    start += 1
                    self.aprocess.append(
                        {'id': str(start + 1), 'label': 'AGV正在前往卸货点{}'.format(i['pos']), 'l': str(start)})
                    self.mprocess.append({str(start + 1): 'AGV正在前往卸货点{}'.format(i['pos']), 'l': str(start)})
                    sql = sql + "when (select 1 from agvcmd where parameter_int4_2 = 1 and agvcmd.agv_command_status_id=11)=1 and (select count(*) from agvcmd where parameter_int4_2 = 1)={} then '{}'\n".format(
                        unload_time, str(start + 1))
                    start += 1
                    unload_time += 1
            self.aprocess.append({'id': str(start + 1), 'label': 'AGV执行任务完成等待数据同步', 'l': str(start)})
            self.mprocess.append({str(start + 1): 'AGV执行任务完成等待数据同步', 'l': str(start)})
            sql = sql + "when (select pl.status from pl) != 'completed' then '{}'\n".format(str(start + 1))
            start += 1
            self.aprocess.append({'id': str(start + 1), 'label': '任务完成等待上报WMS', 'l': str(start)})
            self.mprocess.append({str(start + 1): '任务完成等待上报WMS', 'l': str(start)})
            sql = sql + "when (select pl.report_id from pl) is NULL then '{}'\n".format(str(start + 1))
            start += 1
            self.aprocess.append({'id': str(start + 1), 'label': '任务上报完成', 'l': str(start)})
            self.mprocess.append({str(start + 1): '任务上报完成', 'l': str(start)})
            sql = sql + "when (select pl.report_id from pl) is not NULL then '{}'\nelse '-1' end) as process from ordertask".format(
                str(start + 1))
            start += 1
        except:
            logger.error("不存在此任务的optlist!")
            resdata = {"process": [], "info": {}}
            return resdata, 204
        try:
            from sqlalchemy import select, exists
            session = sched.SessionFactory()
            cursor = session.execute(sql)
            orderinfo = cursor.fetchall()
            session.commit()
        except (Exception) as e:
            logger.error(str(e))
            return {"error": "数据库查询异常"}, 500
        promap = self.initmap(taskno, location_dict)
        data = [dict(zip(ininfo.keys(), ininfo)) for ininfo in orderinfo]
        resdata = {"process": [], "info": {}}
        from ..base.errormap import ordererror
        if len(data) == 0:
            return {'error': "未查到信息"}, 404
        for row in data:
            if row["process"] == '999':
                if row["error_code"] in ordererror:
                    row["reason"] = ordererror[str(row["error_code"])]
                else:
                    row["reason"] = 'unknown'
                break
            print(row)
            print(promap)
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
            resdata["map"] = self.aprocess
            break

        return resdata, 200


class tasktraceback(Resource):

    def __init__(self):
        pass

    def get(self):

        offset = request.args.get("offset")
        limit = request.args.get("limit")
        task_no = request.args.get("task_no")
        b_time = request.args.get("b_time")
        e_time = request.args.get("e_time")
        status = request.args.get("status")
        offset = 0 if offset is None else offset
        limit = 100 if limit is None else limit
        b_time = '2020-1-1' if b_time is None or b_time == '' else b_time
        e_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') if e_time is None or e_time == '' else e_time

        try:
            from ..base.models.layer2_pallet_model import PlTask, PlTaskType, PlTaskRelation, PlTaskReport
            from sqlalchemy import select, exists, between

            with sched.SessionFactory() as session:
                statement = select(PlTask.id, PlTask.task_no, PlTask.task_type, PlTask.status, PlTask.priority,
                                   PlTask.ex, PlTaskRelation.relation).outerjoin(PlTaskRelation) \
                    .filter(PlTask.status.in_(['created', 'handle', 'active', 'in_progress', 'completed',
                                               'error']) if status is None or status == '' else PlTask.status == status,
                            True if task_no is None or task_no == '' else PlTask.task_no == task_no,
                            PlTask.created_timestamp.between(b_time, e_time)).order_by(PlTask.id).offset(offset).limit(
                    limit)
                result = session.execute(statement).all()
                session.commit()
        except (Exception) as e:
            logger.error(str(e))
            return {"error": "数据库异常，请联系相关人员"}, 500

        import copy
        orderlist = []
        tasktmp = {"task_no": None, "agv_list": None, "status": None, "cur_dest": None, "cur_omi": "", "c_t": None,
                   "a_t": None, "cel_t": None, "fin_t": None, "reason": None, "err_code": 0}
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

        # 获取活跃任务对应的order
        if len(orderlist) == 0:
            print("empty")
            return rstdata, 200
        # print(str(orderlist).lstrip('[').rstrip(']'))
        sql = 'select * from layer4_1_om.order where order_name in({})'.format(str(orderlist).lstrip('[').rstrip(']'))
        # print(sql)
        with sched.SessionFactory() as session:
            cursor = session.execute(sql)
            orderinfo = cursor.fetchall()
            session.commit()
        # waiting/active/finish/error/waiting_cancel/cancel_finish/waiting_manually_finish/manually_finish

        for row in orderinfo:
            # 处理未发送成功的
            rstdata[row.order_name]["agv_list"] = row.agv_list
            rstdata[row.order_name]["cur_dest"] = row.current_destination
            rstdata[row.order_name]["cur_omi"] = row.current_omi
            rstdata[row.order_name]["c_t"] = row.create_time.strftime(
                '%Y-%m-%d %H:%M:%S') if row.create_time is not None else ''
            rstdata[row.order_name]["a_t"] = row.active_time.strftime(
                '%Y-%m-%d %H:%M:%S') if row.active_time is not None else ''
            rstdata[row.order_name]["cel_t"] = row.cancel_time.strftime(
                '%Y-%m-%d %H:%M:%S') if row.cancel_time is not None else ''
            rstdata[row.order_name]["fin_t"] = row.finished_time.strftime(
                '%Y-%m-%d %H:%M:%S') if row.finished_time is not None else ''
            rstdata[row.order_name]["err_code"] = row.error_code if row.error_code is not None else 0
            if row.status == 'error':
                rstdata[row.order_name]["status"] = row.status
                pass
            elif row.status == 'finish' or row.status == 'manually_finish':
                if rstdata[row.order_name]["status"] != 'completed':
                    rstdata[row.order_name]["reason"] = "数据尚未同步，长期不同步需要检查监控定时任务"
                else:
                    with sched.SessionFactory() as session:
                        statement = select(PlTaskReport.id).filter(
                            ~exists().where(PlTaskReport.pl_task_id == taskdict[row.order_name].id))
                        result = session.execute(statement).all()
                        session.commit()
                    rstdata[row.order_name]["reason"] = "数据未上报给wms"
            else:
                rstdata[row.order_name]["status"] = row.status

        return rstdata, 200
