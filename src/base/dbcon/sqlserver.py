import pymssql
import logging
logger = logging.getLogger('flask')
def execute_commit_sql(Database, sql_sentence, sql_type = 'select'):
    rows = []
    error_info = None
    try:
        database_connection = pymssql.connect(Database.HOST, Database.USERNAME, Database.PASSWORD,
                                              Database.DATABASE)
        cur = database_connection.cursor()
        cur.execute(sql_sentence)
        if sql_type == 'select':
            rows = cur.fetchall()
        database_connection.commit()
        cur.close()
        # logger.info('One SQL was successfully executed: \n' + sql_sentence)

    except Exception as e:
        logger.info('One SQL failed to execute: \n' + str(sql_sentence))  # need use str() conversion to avoid sql_sentence is None
        error_info = 'Error: ' + str(repr(e))
        logger.info(error_info)

    return rows, error_info

from ...settings import Database
def run_sql(sql_sentence,sql_type = 'select'):
    rows, error_info = execute_commit_sql(Database.sqlserver, sql_sentence, sql_type)
    if error_info is not None:
        logger.info('run "' +str(sql_sentence) +'" failed! error_info: ' + str(error_info))
        return None
    else:
        logger.info('run "' + str(sql_sentence) + '" success! rows: ' + str(rows))
        return rows

def get_index_dict(cursor):
    index_dict=dict()
    index=0
    for desc in cursor.description:
        index_dict[desc[0]]=index
        index=index+1
    return index_dict

def fetch(Database,sql,dict1):
    conn = pymssql.connect(Database.HOST, Database.USERNAME, Database.PASSWORD,Database.DATABASE)
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

def execute(Database,sql,dict):
    conn = pymssql.connect(Database.HOST, Database.USERNAME, Database.PASSWORD,Database.DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql,dict)
    conn.commit()
    conn.close()

def handle(Database,sql,dict):
    conn = pymssql.connect(Database.HOST, Database.USERNAME, Database.PASSWORD,Database.DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, dict)
    res = cursor.fetchall()
    conn.commit()
    conn.close()
    return res


def handle_select(Database, sql, dict):
    conn = pymssql.connect(Database.HOST, Database.USERNAME, Database.PASSWORD,Database.DATABASE)
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

def test_database_connection(database_connection):
    rows, error_info = execute_commit_sql(database_connection, "select 1;")
    if error_info is not None or rows is None or len(rows) <= 0:
        return False  # connection is bad
    else:
        return True  # connection is good
