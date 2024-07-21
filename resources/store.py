import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import StoreSchema,PlainStoreSchema
from models import StoreModel


blp = Blueprint("Stores", "stores", description="Operations on stores")

stores={}

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        try:
            # You presumably would want to include the store's items here too
            # More on that when we look at databases
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(cls, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return stores.values()

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