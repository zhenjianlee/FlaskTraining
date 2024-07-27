import uuid 
import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from schemas import PlainUserSchema
from models import UserModel

blp=Blueprint("Users","users",description="Operation on users")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,PlainUserSchema)
    def get(cls,user_id):
        user=UserModel.query.get_or_404(user_id)
        return user

    @blp.response(201)
    def delete(cls,user_id):
        user=UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message=e)
        return {"code":201,"message":f"User {user} succesfully deleted!"}

    
@blp.route("/user")
class UserList(MethodView):
    @blp.response(200,PlainUserSchema(many=True))
    def get(cls):
        try:
            return UserModel.query.all()
        except SQLAlchemyError as e:
            abort(404, message=e)


    @blp.arguments(PlainUserSchema)
    @blp.response(201,PlainUserSchema)
    def post(cls,user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            return abort(400, message =e)
        except SQLAlchemyError as e:
            return abort(500, message=e)
        return user