from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from app import db



class User(db.Model, UserMixin):
    __tablename__ = "users"
    # primary keys are required by SQLAlchemy

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(9), unique=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    avatar_url = db.Column(db.String(100))
    role = db.Column(db.String(100))

    def __init__(self, user_id, email, name, password, avatar_url, role):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.avatar_url = avatar_url
        self.role = role

    