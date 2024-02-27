from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash


from app import app, db
from app.models.contact import Contact
from app.models.authuser import AuthUser, PrivateContact
from app.models.blog import BlogEntry


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
