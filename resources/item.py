import uuid
import logging

from flask import Flask, Request
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort

from db import items

blp = Blueprint("items",__name__,description="Operation on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self,item_id):
        res = find_items(item_id)
        if res == -1:
            return f"Could not find items with id:{item_id}",404
        return res,200
    

@blp.route("/items")
class Items(MethodView):
    def get(self):
        return items
    

def find_items(item_id):
    try:
        return items[item_id]
    except KeyError:
        logging.info(f"🔴 find_items, could not find item with id")
        return -1