from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash


from app import app, db

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User, Student


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
            role="student",
        )
    )

    db.session.add(
        Student(
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
        User(
            user_id="000000002",
            email="student@mail.com",
            name="Student 1",
            password=generate_password_hash("1234", method="sha256"),
            role="student",
        )
    )

    db.session.add(
        User(
            user_id="000000003",
            email="lecturer@mail.com",
            name="Lecturer 1",
            password=generate_password_hash("1234", method="sha256"),
            role="lecturer",
        )
    )

    db.session.add(
        User(
            user_id="000000004",
            email="admin@admin",
            name="Admin 1",
            password=generate_password_hash("1234", method="sha256"),
            role="admin",
        )
    )

    db.session.commit()

@cli.command("seed_courses")
def seed_course():
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

    db.session.add(
        Course(
            course_id="204113",
            abbr="CS113",
            name="Data Structure",
            description="Learn Data Structure",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204114",
            abbr="CS114",
            name="Database",
            description="Learn Database",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204115",
            abbr="CS115",
            name="Computer Network",
            description="Learn Computer Network",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204116",
            abbr="CS116",
            name="Operating System",
            description="Learn Operating System",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204117",
            abbr="CS117",
            name="Software Engineering",
            description="Learn Software Engineering",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204118",
            abbr="CS118",
            name="Computer Security",
            description="Learn Computer Security",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204119",
            abbr="CS119",
            name="Artificial Intelligence",
            description="Learn Artificial Intelligence",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204120",
            abbr="CS120",
            name="Machine Learning",
            description="Learn Machine Learning",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.add(
        Course(
            course_id="204121",
            abbr="CS121",
            name="Big Data",
            description="Learn Big Data",
            department="CS",
            credits=3,
            year=1,
        )
    )

    db.session.commit()

@cli.command("seed_enrollments")
def seed_enrollments():
    e = []
    for i in range(1, 10):
        tmp = Enrollment(user_id="650510001", course_id=f"20411{i}")
        tmp.set_grade(4.0)
        e.append(tmp)

    tmp = Enrollment(user_id="650510001", course_id="204120")
    tmp.set_grade(3.0)
    e.append(tmp)

    db.session.add_all(e)
    db.session.commit()



if __name__ == "__main__":
    cli()
