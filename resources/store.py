from logging.config import dictConfig
import uuid
import logging

from flask import Flask,request
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort

from db import stores,items
from resources.item import find_items
from schemas import StoreSchema


blp = Blueprint("stores",__name__,description="Operation on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        res = find_store(store_id)
        if res == -1:
            return f"Could not find store with id: {id}",404
        return res,200

    def delete(self,store_id):
        try:
            del stores[store_id]
            del items[store_id]
            return "Item deleted"
        except KeyError:
            return abort(404,exc="Could not find id")
        
    def put(self,store_id):
        logging.info(f"🔵 update_store")
        request_data=request.get_json()
        logging.info(f"🔵 update_store, request body ={request_data}")
        if 'name' not in request_data.keys():
            return abort(400, "Could not find store name")
        if 'items' not in request_data.keys():
            return abort(400, "Could not find items")

        store_data = request_data['name']
        item_data = request_data['items']
    
        update_store= find_store(store_id)
        if update_store == -1:
            return "Could not find store id",400

        update_items = find_items(store_id)
        if update_items== -1:
            return "Could not find  item keys",400
        try:
            stores[store_id]= store_data
            items[store_id]= item_data
            logging.info(f"🟢 update_store, updated items , store ={update_store} , items={update_items}")
            return { "store": stores[store_id] , "items": items[store_id] },201
        except:
            logging.info(f"🔴 update_store, could not find keys")
            return "Could not update data"


@blp.route("/stores")
class Stores(MethodView):
    def get(self):
        logging.info(f"🔵 get_store")
        return {"stores":stores}

    def post(self):
        request_data=request.get_json()
        new_store = request_data['name']
        new_items = request_data['items']
        if new_store in stores.values():
            return abort(400,message="Duplicated store not allowed")
        if new_items in items.values():
            return abort(400,message="Duplicated item not allowed")
        new_uuid = uuid.uuid4().hex
        stores[new_uuid]=new_store
        items[new_uuid]=new_items
        return {
                'id':new_uuid,
                'created_store':new_store,
                'created_items':new_items
                },201


def find_store(store_id):
    logging.info(f"🔵 find_store id: {store_id}")
    try:
        return stores[store_id]
    except KeyError:
        logging.info(f"🔴 find_store, could not find store with id")
        return -1

