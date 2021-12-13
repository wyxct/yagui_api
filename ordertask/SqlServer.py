import pymssql
from ..settings import Database

def get_index_dict(cursor):
    index_dict=dict()
    index=0
    for desc in cursor.description:
        index_dict[desc[0]]=index
        index=index+1
    return index_dict

def fetch(sql,dict1):
    conn = pymssql.connect(Database.sqlserver.HOST, Database.sqlserver.USERNAME, Database.sqlserver.PASSWORD,
                           Database.sqlserver.DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql,dict1)
    rows = cursor.fetchall()
    index_dict = get_index_dict(cursor)
    res = []
    for datai in rows:
            resi = dict()
            for indexi in index_dict:
                    resi[indexi] = datai[index_dict[indexi]]
            res.append(resi)
    conn.close()
    return res

def execute(sql,dict):
    conn = pymssql.connect(Database.sqlserver.HOST, Database.sqlserver.USERNAME, Database.sqlserver.PASSWORD,
                           Database.sqlserver.DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql,dict)
    conn.commit()
    conn.close()

def handle(sql,dict):
    conn = pymssql.connect(Database.sqlserver.HOST, Database.sqlserver.USERNAME, Database.sqlserver.PASSWORD,
                           Database.sqlserver.DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, dict)
    res = cursor.fetchall()
    conn.commit()
    conn.close()
    return res


def handle_select(sql, dict):
    conn = pymssql.connect(Database.sqlserver.HOST, Database.sqlserver.USERNAME, Database.sqlserver.PASSWORD,
                           Database.sqlserver.DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, dict)
    try:
        res = cursor.fetchall()
        if res[0][0] == 1:
            conn.commit()
        else:
            conn.rollback()
    except:
        print("this bill is exist")
        return 0
    conn.close()
    return res




