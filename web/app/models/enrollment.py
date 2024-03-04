from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from app import db


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = "enrollments"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(6), db.ForeignKey("courses.course_id"))
    user_id = db.Column(db.String(9), db.ForeignKey("users.user_id"))

    def __init__(self, course_id, user_id):
        self.course_id = course_id
        self.user_id = user_id
