define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./docs/api/main.js",
    "group": "D:\\work\\python\\flask\\flask-scheduler\\docs\\api\\main.js",
    "groupTitle": "D:\\work\\python\\flask\\flask-scheduler\\docs\\api\\main.js",
    "name": ""
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./src/docs/api/main.js",
    "group": "D:\\work\\python\\flask\\flask-scheduler\\src\\docs\\api\\main.js",
    "groupTitle": "D:\\work\\python\\flask\\flask-scheduler\\src\\docs\\api\\main.js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/api/v1/pltasks/",
    "title": "创建",
    "version": "0.0.0",
    "name": "create_pltasks",
    "group": "pltasks",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "task_no",
            "description": "<p>(必须)    唯一任务号</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "task_type",
            "description": "<p>(必须)    任务类型</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "from_pos",
            "description": "<p>(必须)    开始位置</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "to_pos",
            "description": "<p>(必须)    目标位置</p>"
          },
          {
            "group": "Parameter",
            "type": "Array",
            "optional": false,
            "field": "pos_list",
            "description": "<p>目标位置序列</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "plan_date",
            "description": "<p>计划开始时间</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "status",
            "description": "<p>状态</p>"
          },
          {
            "group": "Parameter",
            "type": "Float",
            "optional": false,
            "field": "priority",
            "description": "<p>优先级</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>(必须)       容器</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid_attribute",
            "description": "<p>(必须)  容器属性</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "custom_parm1",
            "description": "<p>自定义参数1</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "custom_parm2",
            "description": "<p>自定义参数2</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "memo",
            "description": "<p>备注</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Request-Example:",
          "content": "{\n    task_no:\"tk00001\",\n    task_type :\"p2p\",\n    from_pos:\"RA-1-1-1\",\n    to_pos:\"RA-1-1-1\",\n    pos_list:[\"RA-1-1-1\",\"RA-1-1-2\"],\n    plan_date:\"2020-8-18 11:22:11\",  \n    status:\"create\",\n    priority:1.00,\n    cid:\"c001\",\n    cid_attribute:\"empty\", \n    custom_parm1:\"\",\n    custom_parm2:\"\",\n    memo:\"\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "回参": [
          {
            "group": "回参",
            "type": "String",
            "optional": false,
            "field": "task_no",
            "description": ""
          },
          {
            "group": "回参",
            "type": "String",
            "optional": false,
            "field": "create_time",
            "description": "<p>创建时间</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"errno\":0,\n    \"errmsg\":\"创建成功！\",\n    \"data\": {\n        \"task_no\": 1,\n        \"create_time\": \"2010-1-1 12:12:12\"\n\n    }\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "{\n    \"errno\":400,\n    \"errmsg\":\"格式错误\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./src/pltask/views.py",
    "groupTitle": "pltasks"
  }
] });
