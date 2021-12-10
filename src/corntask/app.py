# coding:utf-8
import logging.config
from .views import *
import uuid
from datetime import date, datetime
from flask import Flask as _Flask
from flask import request, render_template, Blueprint
from flask.json import JSONEncoder as _JSONEncoder
from flask_restful import Api
from flask_restful.reqparse import text_type


asyntask_bp = Blueprint('asyntask', __name__, url_prefix='/api/')
api = Api(asyntask_bp, default_mediatype='application/json')

'''
@asyntask_bp.route('index', methods=['GET'])
def demo():
    return render_template('index.html')
'''

api.add_resource(tasks, 'tasks/')
api.add_resource(onetask, 'tasks/<string:taskid>/')
api.add_resource(resumetask, 'tasks/<string:taskid>/resume/')
api.add_resource(pausetask, 'tasks/<string:taskid>/pause/')
api.add_resource(reloadtask, 'tasks/reload/')
api.add_resource(starttask, 'tasks/<string:taskid>/start/')
#api.add_resource(stoptask, 'tasks/<string:taskid>/stop/')
api.add_resource(resultstask, 'tasks/<string:taskid>/results/')
api.init_app(asyntask_bp)
