--TXJ01QLS21111200010550
--TSJ11111211021000101026
with "taskinfo" as
(
	select 'TXJ01QLS21111200010550'::character varying as taskno
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

