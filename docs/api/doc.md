<a name="top"></a>
#  v0.0.0



# Table of contents

- [pltasks](#pltasks)
  - [创建](#创建)

___


# <a name='pltasks'></a> pltasks

## <a name='创建'></a> 创建
[Back to top](#top)

```
POST /api/v1/pltasks/
```

### Parameters - `Parameter`

| Name     | Type       | Description                           |
|----------|------------|---------------------------------------|
| task_no | `String` | <p>(必须)    唯一任务号</p> |
| task_type | `String` | <p>(必须)    任务类型</p> |
| from_pos | `String` | <p>(必须)    开始位置</p> |
| to_pos | `String` | <p>(必须)    目标位置</p> |
| pos_list | `String` | <p>目标位置序列</p> |
| plan_date | `String` | <p>计划开始时间</p> |
| status | `String` | <p>状态</p> |
| priority | `String` | <p>优先级</p> |
| cid | `String` | <p>(必须)       容器</p> |
| cid_attribute | `String` | <p>(必须)  容器属性</p> |
| custom_parm1 | `String` | <p>自定义参数1</p> |
| custom_parm2 | `String` | <p>自定义参数2</p> |
| memo | `String` | <p>备注</p> |

### Parameters examples
`json` - Request-Example:

```json
{
    task_no:"tk00001",
    task_type :"",
    from_pos:"",
    to_pos:"",
    pos_list:"",
    plan_date:"",  
    status:"",
    priority:"",
    cid:"",
    cid_attribute:"", 
    custom_parm1:"",
    custom_parm2:"",
    memo:""
}
```

### Success response

#### Success response - `回参`

| Name     | Type       | Description                           |
|----------|------------|---------------------------------------|
| task_no | `String` |  |
| create_time | `String` | <p>创建时间</p> |

### Success response example

#### Success response example - `Success-Response:`

```json
{
    "errno":0,
    "errmsg":"注册成功！",
    "data": {
        "task_no": 1,
        "create_time": "2010-1-1 12:12:12"

    }
}
```

### Error response example

#### Error response example - `Error-Response:`

```json
{
    "errno":400,
    "errmsg":"数据库查询错误！"
}
```

