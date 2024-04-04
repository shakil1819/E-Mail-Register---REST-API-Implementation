import os
import redis
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_migrate import Migrate
from rq import Queue
from flask import current_app,jsonify
from sqlalchemy import or_
from redis import Redis
from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema#, UserRegisterSchema
from tasks import send_user_registration_email
from validate_email import validate_email
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()

blp = Blueprint("Users", "users", description="Operations on users")
# connection = redis.from_url((host)
#     os.getenv("REDIS_URL")
# )
connection=Redis(host='redis',port=6379)
# connection=Redis(host='rq_worker',port=6379)
queue = Queue("emails", connection=connection)

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that username or email already exists.")

        is_valid = validate_email(user_data["email"])
        if not is_valid:
            abort(400, message="Invalid email address.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": f"Database error occurred: {str(e)}"}, 500

        subject = "Welcome!Your registration was successful"
        message = f"Welcome to our platform, {user.username}!"

        for i in range(3):
            delay=timedelta(minutes=30 * (i + 1))
            current_app.queue.enqueue_in(send_user_registration_email,subject, message, user.email, retry=i)

        # Store the email in Redis
        # connection.set(user.email, 'pending')

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