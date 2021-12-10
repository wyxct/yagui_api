# coding:utf-8
import logging.config
from .views import *
import uuid
from datetime import date, datetime
from flask import Flask as _Flask
from flask import Blueprint
from flask.json import JSONEncoder as _JSONEncoder
from flask_restful import Api

mt_bp = Blueprint('mt', __name__, url_prefix='/ts/api/')
api = Api(mt_bp, default_mediatype='application/json')

api.add_resource(addropt, 'addropt/')
api.add_resource(functest, 'functest/')

api.add_resource(p2ptasksgoon, 'p2ptasks/goon/')
api.add_resource(accessiblelocation, 'p2ptasks/accessibleloc/')
api.add_resource(tasktraceback, 'p2ptasks/tasktraceback/')
api.add_resource(tasktracebackdetail, 'p2ptasks/tasktraceback/<string:taskno>')
api.init_app(mt_bp)

