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
