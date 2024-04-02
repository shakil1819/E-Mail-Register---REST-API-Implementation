from db import db


class UserModel(db.Model):
    tablename = "users"

    email = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
    username = db.Column(db.String(80), unique = False, nullable = False)
    password = db.Column(db.String(80), nullable = False)