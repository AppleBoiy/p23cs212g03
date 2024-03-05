from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from app import db


class Course(db.Model, UserMixin):
    __tablename__ = "courses"
    # primary keys are required by SQLAlchemy
    course_id = db.Column(db.String(6), primary_key=True)
    abbr = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(1000))
    year = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    credits = db.Column(db.Integer)
    department = db.Column(db.String(100))

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, course_id, abbr, name, year, description, credits, department):
        self.course_id = course_id
        self.abbr = abbr
        self.name = name
        self.year = year
        self.description = description
        self.credits = credits
        self.department = department

        self.created = db.func.current_timestamp()
        self.updated = db.func.current_timestamp()

    def update(self, name, description, credits, department):
        self.name = name
        self.description = description
        self.credits = credits
        self.department = department

        self.updated = db.func.current_timestamp()


    # to_dict() and from_dict() methods are required by the SerializerMixin
    def to_dict(self):
        return {
            "course_id": self.course_id,
            "abbr": self.abbr,
            "name": self.name,
            "year": self.year,
            "description": self.description,
            "credits": self.credits,
            "department": self.department,
        }

    @staticmethod
    def from_dict(course_dict):
        return Course(
            course_dict["course_id"],
            course_dict["abbr"],
            course_dict["name"],
            course_dict["year"],
            course_dict["description"],
            course_dict["credits"],
            course_dict["department"],
        )