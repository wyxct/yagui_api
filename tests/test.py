#coding:utf-8

general_result = dict()
def pick_count(sku):
    if sku in general_result:
        general_result[sku] += 1
    else:
        general_result[sku] = 1
    return general_result

def get_top_k_sku(k):
    sorted_count = sorted(general_result.items(),key=lambda x:x[1])
    return sorted_count[:k]

# 每次拣货调一下pick_count(sku)
# get_top_k_sku(k)函数获取频率前k的品类


# 1.定时任务分为General和项目的文件夹，然后通用的放General，项目专用放项目文件夹
# 2.setting里面加项目和自启动定时任务
# 3.server下面project改成PROJECT_NO
# 4.每个定时任务的py文件路径都得改，包括库引用的路径
# 5.通过每个定时任务里面的配置，过滤掉不是同项目的定时任务
# 6.通过selfboot配置自动加载指定定时任务

# 1.查看是否能够读取到src下面的tasks下面的子文件，并插入到g_task_table，d_task_table表中
# 2.测试是否能读取到setting.json下面的配置文件并在内存写入到setting.py里
# 3.测试是否能自启动SELF_BOOT里面的定时任务
# 4.测试是否只启动了general和PROJECT_NO里的项目的定时任务
# 5.测试是否关闭了之前的不是自启动或者不是本项目的定时任务
# 6.测试改动之后原本定时任务是否正常运行
# 7.测试接口是否能返回正确的文件夹下面的所有任务和他属于的项目