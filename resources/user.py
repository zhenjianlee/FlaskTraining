import uuid 
import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt


from db import db
from schemas import PlainUserSchema
from models import UserModel, BlockedAccessTokenModel

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
            abort(404, message=str(e))


    @blp.arguments(PlainUserSchema)
    @blp.response(201,PlainUserSchema)
    def post(cls,user_data):
        user = UserModel(username=user_data.get('username'),password=pbkdf2_sha256.hash(user_data.get('password')))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            return abort(400, message =str(e))
        except SQLAlchemyError as e:
            return abort(500, message=str(e))
        return user
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(cls,user_data):
        user = UserModel.query.filter_by(username=user_data.get('username')).first()
        logging.debug(f"user : {user.id} , {user.username} , {user.password} , user_data: {user_data}")
        if user and pbkdf2_sha256.verify(user_data.get('password'),user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token":access_token}

        return abort(401, message="Invalid login credentials!")
    
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(cls):
        jti=get_jwt().get('jti')
        blocked_token = BlockedAccessTokenModel(jti=jti,token=get_jwt())
        try:
            db.session.add(blocked_token)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404,message=e)
        return {"message":"Successfully logged out"}
