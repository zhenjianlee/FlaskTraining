from logging.config import dictConfig
import uuid
import logging

from flask import Flask,request
from flask_smorest import Api, Blueprint, abort

from db import stores,items

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

@app.get('/stores')
def get_stores():
    logging.info(f"🔵 get_store")
    return {"stores":stores}

@app.post('/store')
def post_store():
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


@app.get('/store/<id>')
def get_store(id):
    res = find_store(id)
    if res == -1:
        return f"Could not find store with id: {id}",404
    return res,200


@app.delete('/store/<id>')
def delete_store(id):
    try:
        del stores[id]
        del items[id]
        return "Item deleted"
    except KeyError:
       return abort(404,exc="Could not find id")
    

@app.put('/store/<id_data>')
def update_store(id_data):
    logging.info(f"🔵 update_store")
    request_data=request.get_json()
    logging.info(f"🔵 update_store, request body ={request_data}")
    if 'name' not in request_data.keys():
        return abort(400, "Could not find store name")
    if 'items' not in request_data.keys():
        return abort(400, "Could not find items")
    # if 'id' not in request_data.keys():
    #     return abort(400, "Could not find store id")
    store_data = request_data['name']
    item_data = request_data['items']
    # id_data=request_data['id']
  
    update_store= find_store(id_data)
    if update_store == -1:
        return "Could not find store id",400

    update_items = find_items(id_data)
    if update_items== -1:
        return "Could not find  item keys",400
    try:
        stores[id_data]= store_data
        items[id_data]= item_data
        logging.info(f"🟢 update_store, updated items , store ={update_store} , items={update_items}")
        return { "store": stores[id_data] , "items": items[id_data] },201
    except:
        logging.info(f"🔴 update_store, could not find keys")
        return "Could not update data"
    
    
@app.get('/items')
def get_items():
    return items

@app.get('/item/<id>')
def get_item(id):
    res = find_items(id)
    if res == -1:
        return f"Could not find items with id:{id}",404
    return res,200

def find_store(id):
    try:
        return stores[id]
    except KeyError:
        logging.info(f"🔴 find_store, could not find store with id")
        return -1

def find_items(id):
    try:
        return items[id]
    except KeyError:
        logging.info(f"🔴 find_store, could not find item with id")
        return -1