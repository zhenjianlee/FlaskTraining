import uuid
import logging
import models

from flask import Flask
from flask_smorest import Api

from config import DevelopmentConfig
from logging.config import dictConfig
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from db import db

def create_app():
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
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api=Api(app)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    return app
