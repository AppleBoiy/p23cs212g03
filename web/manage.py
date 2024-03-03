from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash


from app import app, db
from app.models.contact import Contact
from app.models.authuser import AuthUser, PrivateContact
from app.models.blog import BlogEntry

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

@cli.command("seed_db")
def seed_db():
    db.session.add(
        User(
            user_id="650510XXX",
            email="flask@204212",
            name="สมชาย ทรงแบด",
            password=generate_password_hash("1234", method="sha256"),
            avatar_url="https://ui-avatars.com/api/?name=\
สมชาย+ทรงแบด&background=83ee03&color=fff",
            role="admin",
        )
    )
    db.session.add(
        User(
            user_id="650510001",
            email="flask@204213",
            name="สมหญิง ทรงแบด",
            password=generate_password_hash("1234", method="sha256"),
            avatar_url="https://ui-avatars.com/api/?name=\
สมหญิง+ทรงแบด&background=83ee03&color=fff",
            role="user",
        )
    )

    db.session.add(
        User(
            user_id="650510999",
            email="Sompong@jojo.net",
            name="สมปอง ใจร้าย",
            password=generate_password_hash("1234", method="sha256"),
            avatar_url="https://ui-avatars.com/api/?name=\
สมชาย+ทรงแบด&background=83ee03&color=fff",
            role="teacher",
        )
    )

    db.session.add(
        User(
            user_id="000000001",
            email="google@hotmail.com",
            name="กูรู",
            password=generate_password_hash("1234", method="sha256"),
            avatar_url="https://ui-avatars.com/api/?name=\
สมชาย+ทรงแบด&background=83ee03&color=fff",
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


@cli.command("seed_sample_db")
def seed_sample_db():
    db.session.add(
        AuthUser(
            email="flask@204212",
            name="สมชาย ทรงแบด",
            password=generate_password_hash("1234", method="sha256"),
            avatar_url="https://ui-avatars.com/api/?name=\
สมชาย+ทรงแบด&background=83ee03&color=fff",
        )
    )

    db.session.add(
        BlogEntry(
            name="สมชาย ทรงแบด",
            message="hello welcome to my blog",
            email="flask@204212",
        )
    )

    db.session.add(Contact(firstname="สมชาย", lastname="ทรงแบด", phone="081-111-1111"))
    db.session.add(
        PrivateContact(
            firstname="สมชาย",
            lastname="ทรงแบด",
            phone="081-111-1111",
            owner_id=1,
        )
    )
    db.session.commit()



if __name__ == "__main__":
    cli()
