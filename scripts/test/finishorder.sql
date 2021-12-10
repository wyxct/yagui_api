--手工正常完成order脚本
with no as (
	select 'TXJ21800121101500010043'::character varying as no
)
update layer4_1_om.order set status = 'finish',
current_destination = (
with arr as(
select ARRAY(select (jsonb_array_elements(optlist->'optlist')->>'pos') from pl_task where task_no = (select no.no from no)) as t
)
select arr.t[array_length(arr.t,1)] from arr)||'(1)'
where order_name = (select no.no from no)
