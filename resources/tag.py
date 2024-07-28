import uuid
import logging
import json

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError 

from db import db
from schemas import TagSchema , ItemAndTagSchema
from models import TagModel,StoreModel,ItemModel

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
    
    @blp.response(201,TagSchema)
    @blp.alt_response(202,
                  description="Deletes a tag if no item is tagged with it",
                    example={"message":"Tag Deleted"})
    @blp.alt_response(404,description="Tag not found")
    @blp.alt_response(400,description="Tag is not deleted")
    def delete(cls,tag_id):
        tag= TagModel.query.get_or_404(tag_id)
        logging.debug(f"Tag - delete : {tag}")
        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,message=str(e))

        return {"code": 201, "message":f"Tag {tag} succesfully deleted"}


@blp.route("/tag")
class TagList(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(cls):
        tags= TagModel.query.all()
        return tags
    

# Linking and Unlinking Tags to Items
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinksTagsToItems(MethodView):
    @blp.response(201,TagSchema)
    def post(cls,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            #db.session.add(item) # not necessary to add!! it is ald in session!
            db.session.commit()
        except SQLAlchemyError as e:
            abort (500,message=str(e))
        return tag
    

    @blp.response(200,ItemAndTagSchema)
    def delete(cls,item_id,tag_id):
        item =ItemModel.query.get_or_404(item_id)
        tag= TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))

        return {"message":"Item removed from tag","item": item ,"tag":tag}

    


