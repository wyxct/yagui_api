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

task_order = Blueprint('ordertask', __name__, url_prefix='/')
api = Api(task_order, default_mediatype='application/json')

api.add_resource(FinishTask, 'FinishTask/')
api.init_app(task_order)

