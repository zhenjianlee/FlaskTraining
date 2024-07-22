import uuid
import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import StoreSchema,PlainStoreSchema
from models import StoreModel,ItemModel


blp = Blueprint("Stores", "stores", description="Operations on stores")

stores={}

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store

    @blp.response(200)
    def delete(cls, store_id):
        try:
            store = StoreModel.query.filter_by(id=store_id).first()
            items = ItemModel.query.filter_by(store_id=store_id).all()
            logging.debug(f"Store -> delete : Found store: {store}")
            db.session.delete(items)
            db.session.commit()
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(404, message="Could not delete store!")
        return {"code":201,"message":f"Succesfully deleted the store {store}"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        try:
            return StoreModel.query.all()
        except SQLAlchemyError:
            abort(404, message="Store not found.")

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            return abort(400,message="Store already exists. Cannot contain duplicate values!")
        except SQLAlchemyError:
            return abort(500, message="Unable to insert store data into DB")
        return store