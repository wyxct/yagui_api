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

task_bp = Blueprint('pltask', __name__, url_prefix='/api/')
api = Api(task_bp, default_mediatype='application/json')

api.add_resource(p2ptasks, 'p2ptasks/')
api.add_resource(p2ptasksInteractio, 'p2ptasks/interaction/')
api.add_resource(p2ptasksgoon, 'p2ptasks/goon/')
api.add_resource(accessiblelocation, 'p2ptasks/accessibleloc/')
api.add_resource(tasktraceback, 'p2ptasks/tasktraceback/')
api.add_resource(tasktracebackdetail, 'p2ptasks/tasktraceback/<string:taskno>')
api.init_app(task_bp)

