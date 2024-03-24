import os
import redis
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from rq import Queue
from flask import current_app,jsonify
from sqlalchemy import or_

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema#, UserRegisterSchema
from tasks import send_user_registration_email


blp = Blueprint("Users", "users", description="Operations on users")
connection = redis.from_url(
    os.getenv("REDIS_URL")
)
queue = Queue("emails", connection=connection)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        subject = "Welcome!Your registration was successful"
        message = f"Welcome to our platform, {user.username}!"

        current_app.queue.enqueue(send_user_registration_email,subject, message, user.email)
        return {"message": "User created successfully."}, 201

@blp.route("/user")
class StoreList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

@blp.route("/deleteall")
class DeleteAllUsers(MethodView):
    def delete(self):
        try:
            db.session.query(UserModel).delete()
            db.session.commit()
            return {"message": "All data deleted successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {e}"}, 500