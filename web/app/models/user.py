from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from app import db
from werkzeug.security import generate_password_hash


def gen_avatar_url(email, name):
    bgcolor = generate_password_hash(email, method="sha256")[-6:]
    color = hex(int("0xffffff", 0) - int("0x" + bgcolor, 0)).replace("0x", "")
    lname = ""
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]

    avatar_url = (
        "https://ui-avatars.com/api/?name="
        + fname
        + "+"
        + lname
        + "&background="
        + bgcolor
        + "&color="
        + color
    )
    return avatar_url


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

    def __init__(self, user_id, email, name, password, role):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.role = role
        self.avatar_url = gen_avatar_url(email, name)
