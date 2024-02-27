
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
from app import db




class BlogEntry(db.Model, SerializerMixin):
    __tablename__ = "blog_entries"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    message = db.Column(db.String(280))
    email = db.Column(db.String(50), unique=True)
    

    def __init__(self, email, name, message):
        self.email = email
        self.name = name
        self.message = message
        
    
    def update(self, email, name, message):
        self.email = email
        self.name = name
        self.message = message
        