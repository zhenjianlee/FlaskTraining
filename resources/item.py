import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError 

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item= ItemModel.query.get_or_404(item_id)
        return item

    @blp.response(200)
    def delete(self, item_id):
        try:
            item=ItemModel.query.filter_by(id=item_id).first()
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            return abort(500, message="Could not delete item!")
        return {'code': 200 ,"message":f"Succesfully deleted the item {item}"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item= ItemModel.query.get(item_id)
        if item:
            item.name = item_data['name']
            item.price =item_data['price']
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return ItemModel.query.all()
        except SQLAlchemyError:
            return abort(404,message="Could not retrieve Item data")

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occured with DB insertion")
        return item