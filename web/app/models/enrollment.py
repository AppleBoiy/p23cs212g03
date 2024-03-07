from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from app import db
from app.models.course import Course
from app.models.user import User, Lecturer

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

    lecturers = db.relationship("Lecturer", secondary="lecturer_enrollments")

    delete_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, course_id, user_id):
        self.course_id = course_id
        self.user_id = user_id

    def set_grade(self, grade):
        self.grade = grade
        db.session.commit()


    def delete(self):
        self.delete_at = datetime.now()
        db.session.commit()

    def add_lecturer(self, lecturer):
        self.lecturers.append(lecturer)
        db.session.commit()

    def remove_lecturer(self, lecturer):
        self.lecturers.remove(lecturer)
        db.session.commit()



class LecturerEnrollments(db.Model):
    __tablename__ = "lecturer_enrollments"
    id = db.Column(db.Integer, primary_key=True)
    lecturer_id = db.Column(db.String(9), db.ForeignKey("lecturers.user_id"), primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"), primary_key=True)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    delete_at = db.Column(db.DateTime, nullable=True)


    def delete(self):
        self.delete_at = datetime.now()
        db.session.commit()

    def __init__(self, lecturer_id, enrollment_id):
        self.lecturer_id = lecturer_id
        self.enrollment_id = enrollment_id