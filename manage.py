import subprocess

import _mssql
import uuid
import decimal
import json
from src.app import create_app
#from celery.schedules import crontab
# from src.corntask.get import sched
from flask_script import Manager
from flask_apidoc.commands import GenerateApiDoc
from flask_apidoc import ApiDoc
import os

from flask import render_template, current_app


def run(model):
    args = 'flask-sqlacodegen --flask --schema {} --outfile ./src/base/models/{}_model.py postgresql://postgres:admin@127.0.0.1:5432/longji0628'.format(
        model, model)
    os.system(args)

if __name__ == '__main__':
    app = create_app()
    
    from src.corntask.sql_manager import *
    from src.settings import Database
    from src.base.dbcon.sqlserver import *

    @app.route('/task')
    def adddemo():
        return render_template('task.html')

    @app.route('/apidoc')
    def apidoc():
        return current_app.send_static_file('index.html')

    from src.settings import server
    app.run(host='0.0.0.0', port=server.PORT, debug=False, threaded=server.THREADED)

