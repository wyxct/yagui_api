from ts_template.ts_template import CancelException
from ts_template.ts_template import StopException
import sys
import random
import asyncio
import pdb
from pathlib import Path
from datetime import datetime
import time
import json
desc = 'multi_point_task'
# agv_type:{4:ants;1:picking}
para_template = {'multi_point_task': {'optlist': 'dict'}}
operator_list = []

async def run(self):
    status = 0
    try:
        task_id = None
        optlist = sorted (self.optlist)
        order_info = await self.get_order_info()
        order_id = json.loads(order_info).get('order_name')
        for idx in optlist:
            current_point = self.optlist[idx]
            check_point = current_point.get('check_point',0)
            i_flag = current_point.get('i_flag', True) # 自动完成
            pos = current_point['pos']
            opt = current_point['opt']
            # todo:opt需要确认

            if opt == 'go':
                opt_id = -1
            elif opt == 'load':
                opt_id = 2
            elif opt == 'unload':
                opt_id = 1
            else:
                continue

            if check_point != 0:
                # 有check点任务
                check_task = await self.goto_location(check_point, -1, True, [8], None, task_id)
                if opt == 'load':
                    (i_status, result) = await self.insert_interaction_and_wait_finish2(order_id, 1, json.dumps({"pos":pos}))
                elif opt == 'unload':
                    if check_point == 'LC-01-01-01':
                        # 传送带前的check点定制写死
                        (i_status, result) = await self.insert_interaction_and_wait_finish2(order_id, 5,json.dumps({"pos": pos}))
                    else:
                        (i_status, result) = await self.insert_interaction_and_wait_finish2(order_id, 4,json.dumps({"pos": pos}))
                else:
                    continue

                if i_status == 'invalid':
                    check_apply_result = result
                else:
                    # todo:失败怎么处理？？
                    check_apply_result = pos
            else:
                check_task = task_id
                check_apply_result = pos

            if not i_flag:
                # 有交互任务（不自动完成）
                goto_task = await self.goto_location(check_apply_result, -1, True, [8], None, check_task)
                i_status = await self.insert_interaction_and_wait_finish2(order_id, 2, json.dumps({"pos":check_apply_result}))
                if i_status == 'invalid':
                    task_id = await self.opt(check_apply_result, opt_id, True, [8], None, goto_task)

                    # 维护库位状态
                    if opt == 'load':
                        await self.insert_interaction(order_id, 3, json.dumps({"pos": check_apply_result}))
                    elif opt == 'unload':
                        await self.insert_interaction(order_id, 6, json.dumps({"pos": check_apply_result}))

                else:
                    # todo:失败怎么处理？？
                    task_id = goto_task
                    pass
            else:
                task_id = await self.goto_location(check_apply_result, opt_id, True, [8], None, check_task)
                # 维护库位状态
                if opt == 'load':
                    await self.insert_interaction(order_id, 3, json.dumps({"pos": check_apply_result}))
                elif opt == 'unload':
                    await self.insert_interaction(order_id, 6, json.dumps({"pos": check_apply_result}))


    except CancelException as e:
        self.logger.info('Order:{} When run file \"{}\", get cancel command'.format(self.order.order_id, Path(__file__).name))
        status = 1
        await self.cancel()
        return status
    except StopException as e:
        self.logger.info('Order:{} When run file \"{}\", get stop ts command'.format(self.order.order_id, Path(__file__).name))
        return 2
    except Exception as e:
        self.logger.error('Order({}) When run file \"{}\", get exception：{}'.format(self.order.order_id, Path(__file__).name, e))
        return 504
    self.logger.info('Order:{} Run file \"{}\", finished!'.format(self.order.order_id, Path(__file__).name))
    self.logger.debug(
        '============================== Order:{} Done==============================\n'.format(self.order.order_id))
    return status


async def cancel(self):
    self.logger.info('Order:{} When run file {}, run cancel operation'.format(self.order.order_id, Path(__file__).name))
    self.logger.debug(
        '============================== Order:{} Done==============================\n'.format(self.order.order_id))
    return
