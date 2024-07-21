from logging.config import dictConfig
import uuid
import logging

from flask import Flask,request
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort

from config import DevelopmentConfig
from db import stores,items
from exampleDB import storesExample,itemsExample
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.exampleStore import blp as ExampleStoreBlueprint
from resources.exampleItem import blp as ExampleItemBlueprint

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
api=Api(app)
# api.register_blueprint(StoreBlueprint)
# api.register_blueprint(ItemBlueprint)
api.register_blueprint(ExampleStoreBlueprint)
api.register_blueprint(ExampleItemBlueprint)