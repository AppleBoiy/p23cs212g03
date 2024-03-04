from datetime import datetime, timezone

from app import db, app
from sqlalchemy_serializer import SerializerMixin


def get_server_time_utc():
    server_time = datetime.now()
    server_time = server_time.astimezone(timezone.utc)
    return server_time


class BlogEntry(db.Model, SerializerMixin):
    __tablename__ = "blog_entries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(280), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=get_server_time_utc)
    date_updated = db.Column(
        db.DateTime,
        nullable=False,
        default=get_server_time_utc,
    )
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, message, email):
        self.name = name
        self.message = message
        self.email = email
        self.date_created = get_server_time_utc()

    def update(self, message):
        app.logger.debug(f"Updating message: {message}")
        self.message = message
        self.date_updated = get_server_time_utc()

    def delete(self):
        self.is_deleted = True
        self.date_updated = get_server_time_utc()
        db.session.commit()
