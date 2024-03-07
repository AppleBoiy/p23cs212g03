from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from app import db
from app.models.course import Course

class Enrollment(db.Model, SerializerMixin):
    __tablename__ = "enrollments"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(6), db.ForeignKey("courses.course_id"))
    user_id = db.Column(db.String(9), db.ForeignKey("users.user_id"))
    course_info = db.relationship("Course")
    grade = db.Column(db.Float, nullable=True)
    # many to many relationship between users and courses
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())



    def __init__(self, course_id, user_id):
        self.course_id = course_id
        self.user_id = user_id

    def set_grade(self, grade):
        self.grade = grade
        db.session.commit()