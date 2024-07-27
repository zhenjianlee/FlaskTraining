import uuid
import logging
import models

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from config import DevelopmentConfig
from logging.config import dictConfig
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.user import blp as UserBlueprint
from resources.tag import blp as TagBlueprint
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
    jwt = JWTManager(app)
    api=Api(app)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
