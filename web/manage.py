from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash


from app import app, db

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    app.logger.info("create_db")
    try:
        app.logger.info("db.drop_all()")
        db.drop_all()
    except:
        app.logger.info("db.drop_all() failed")

    db.create_all()
    app.logger.info("db.create_all()")
    db.session.commit()


@cli.command("drop_db")
def drop_db():
    app.logger.info("drop_db")
    db.drop_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        User(
            user_id="650510XXX",
            email="flask@204212",
            name="สมชาย ทรงแบด",
            password=generate_password_hash("1234", method="sha256"),
            role="admin",
        )
    )
    db.session.add(
        User(
            user_id="650510001",
            email="flask@204213",
            name="สมหญิง ทรงแบด",
            password=generate_password_hash("1234", method="sha256"),
            role="user",
        )
    )

    db.session.add(
        User(
            user_id="650510999",
            email="Sompong@jojo.net",
            name="สมปอง ใจร้าย",
            password=generate_password_hash("1234", method="sha256"),
            role="lecturer",
        )
    )

    db.session.add(
        User(
            user_id="000000001",
            email="google@hotmail.com",
            name="กูรู",
            password=generate_password_hash("1234", method="sha256"),
            role="student",
        )
    )

    db.session.add(
        Course(
            course_id="204111",
            abbr="CS111",
            name="Python Programming",
            description="Learn Python Programming",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204112",
            abbr="CS112",
            name="Web Programming",
            description="Learn Web Programming",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.commit()

    db.session.add(
        Enrollment(
            user_id="650510001",
            course_id="204111",
        )
    )

    db.session.commit()


if __name__ == "__main__":
    cli()
