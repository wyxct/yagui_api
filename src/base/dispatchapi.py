
from ..settings import orderserver


def sendorder(data):
    import requests
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'charset':'utf-8',
    }
    order_json = {
        "order_name": data["task_no"],
        "priority": data["priority"] if "priority" in data  else 0,
        "dead_line": "2020-02-01 16:00:00",
        "ts_name": data["ts_name"],
        "parameters": data["parameters"],
        "uid":hash(data["task_no"])
        }

    try:
        response = requests.request("POST", orderserver.S_URI, json=order_json, headers=headers)
    except (Exception) as e:
        print(e)
        return {"error":str(e)}, 400
    return response.text.encode('latin-1').decode('gbk'),response.status_code

if __name__ == '__main__':
    pass
