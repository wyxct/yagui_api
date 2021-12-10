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

def test_database_connection(database_connection):
    rows, error_info = execute_commit_sql(database_connection, "select 1;")
    if error_info is not None or rows is None or len(rows) <= 0:
        return False  # connection is bad
    else:
        return True  # connection is good
