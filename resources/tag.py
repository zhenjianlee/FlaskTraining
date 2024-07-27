import uuid
import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError 

from db import db
from schemas import TagSchema ,PlainTagSchema
from models import TagModel,StoreModel

blp = Blueprint("Tags","tags",description="Operation on Tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(cls,store_id):
        store= StoreModel.query.get_or_404(store_id)
        logging.debug(f"TagsInStore.get : store = {store}")
        return store.tags

    

    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(cls,tag_data,store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, 
                          TagModel.name == tag_data.get('name')).first():
            abort(400, message="A tag with that name already exists in that store")
        new_tag=TagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort (500, message=str(e))
        return new_tag
    

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(cls,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag


@blp.route("/tag")
class TagList(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(cls):
        tags= TagModel.query.all()
        return tags
    
