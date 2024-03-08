import json
import secrets
import string

# import sleep
from time import sleep

from flask import jsonify, render_template, request, url_for, flash, redirect, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import app, db, login_manager, oauth
from app.models.authuser import AuthUser
from app.models.user import User, Student, ROLE
from app.models.course import Course
from app.models.enrollment import Enrollment



# from app import oauth

def dummy_sleep():
    sleep(1)

@app.route("/test/sleep")
def test_sleep():
    try:
        dummy_sleep()
        raise TimeoutError
    except TimeoutError as e:
        app.logger.error(e)
        return redirect(url_for("pre3_504"))


@app.errorhandler(404)
def error_404(e):
    return redirect(url_for("pre3_404"))


@app.route("/error/404")
def pre3_404():
    return render_template("err/404.html")


@app.errorhandler(401)
def error_401(e):
    return redirect(url_for("pre3_401"))


@app.route("/error/401")
def pre3_401():
    return render_template("err/401.html")


@app.errorhandler(500)
def error_500(e):
    return redirect(url_for("pre3_500"))


@app.route("/error/500")
def pre3_500():
    return render_template("err/500.html")


@app.errorhandler(504)
def error_504(e):
    return redirect(url_for("pre3_504"))


@app.route("/error/504")
def pre3_504():
    return render_template("err/504.html")


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


@app.route("/pre3/teacher/assign")
@login_required
def teacher_assign():
    # if current_user.role != "teacher":
    # abort(403)
    users = User.query.all()
    course = Course.query.all()

    return render_template("pre3/assign.html", users=users, course=course)


@app.route("/pre3/admin_dashboard")
@login_required
def pre3_admin_dashboard():
    try:
        if current_user.role != "admin":
            abort(401)
        return render_template(
            "pre3/admin_dashboard.html", users=User.query.all(), courses=Course.query.all()
        )
    except SQLAlchemyError as e:
        app.logger.error(e)
        return redirect(url_for("pre3_500"))


@app.route("/pre3/tree")
def tree():
    return render_template("pre3/tree.html")


@app.route("/contact")
def pre3_contact():
    return render_template("contact.html")


def catch_all(path):
    return redirect(url_for("index"))


@app.route("/")
def index():
    try:
        return render_template("index.html")
    except SQLAlchemyError as e:
        app.logger.error(e)
        return redirect(url_for("pre3_500"))


@app.route("/pre3")
def pre3_index():
    return render_template("pre3/index.html")


@app.route("/pre3/profile")
@login_required
def pre3_profile():
    return render_template("pre3/profile.html")


@app.route("/pre3/logout")
@login_required
def pre3_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/pre3/home/student")
@login_required
def pre3_student():
    return render_template("pre3/home_student.html")

@app.route("/pre3/student/dashboard")
@login_required
def pre3_student_dashboard():
    student_id = current_user.user_id
    enrollments = Enrollment.query.filter_by(user_id=current_user.user_id).all()
    c = []
    all_credit = 0
    all_grade = 0
    # create course dictionary
    for e in enrollments:
        tmp = Course.query.filter_by(course_id=e.course_id).first().to_dict()
        all_credit += tmp["credits"]
        if e.grade:
            all_grade += e.grade * tmp["credits"]
        tmp["grade"] = e.grade
        c.append(tmp)
    if all_credit:
        gpa = all_grade / all_credit
    else:
        gpa = 0

    app.logger.debug(str(c))
    return render_template("pre3/student/index.html", courses=Course.query.all(), enrollments=c, gpa=gpa)

@app.route("/pre3/admin/create_user", methods=("GET", "POST"))
@login_required
def pre3_created_user():
    if current_user.role != "admin":
        abort(401)
    if request.method == "POST":
        result = request.form.to_dict()
        app.logger.debug(str(result))

        validated = True
        validated_dict = {}
        valid_keys = ["email", "name", "password", "role", "user_id"]

        # validate the input
        for key in result:
            app.logger.debug(str(key) + ": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == "undefined":
                validated = False
                break
            validated_dict[key] = value
            # code to validate and add user to database goes here

        app.logger.debug("validation done")
        if validated:
            app.logger.debug("validated dict: " + str(validated_dict))
            email = validated_dict["email"]
            name = validated_dict["name"]
            password = validated_dict["password"]
            role = validated_dict["role"]
            user_id = validated_dict["user_id"]

            check_list = ["email", "name", "user_id"]
            # if this returns a user, then the email already exists in database
            for key in check_list:
                user = User.query.filter_by(email=validated_dict[key]).first()
                app.logger.debug("checking " + key)
                if user:
                    # if a user is found, we want to redirect back to signup
                    # page so user can try again
                    app.logger.debug("email exists")
                    # return redirect(url_for("pre3_created_user"))
                    try:
                        return render_template(
                            "pre3/created_user.html", roles=ROLE.ALL_ROLE
                        )
                    except SQLAlchemyError as e:
                        app.logger.error(e)
                        return redirect(url_for("pre3_500"))

            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(email, name)
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method="sha256"),
                role=role,
                user_id=user_id,
            )
            if role == "student":
                new_student = Student(
                    email=email,
                    name=name,
                    password=generate_password_hash(password, method="sha256"),
                    role=role,
                    user_id=user_id,
                )
                db.session.add(new_student)
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("pre3_admin"))
    return render_template("pre3/created_user.html", roles=ROLE.ALL_ROLE)


@app.route("/pre3/home/admin", methods=["GET", "POST"])
@login_required
def pre3_admin():
    users = User.query.all()

    if request.method == "POST":

        # prevent unauthorized access
        if current_user.role != "admin":
            abort(401)

        user_id = request.form.get("user_id")
        new_role = request.form.get("new_role")
        action = request.form.get("action")

        if action == "delete":
            user = User.query.get(user_id)
            if user:
                User.query.filter_by(user_id=user_id).delete()
                db.session.commit()
                return redirect(url_for("pre3_admin"))

        if action == "change_role":
            user = User.query.get(user_id)
            if user:
                user.role = new_role
                db.session.commit()
                return redirect(url_for("pre3_admin"))

    return render_template("pre3/home_admin.html", users=users)


@app.route("/pre3/signup", methods=("GET", "POST"))
def pre3_signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        result = request.form.to_dict()
        app.logger.debug(str(result))
        validated = True
        validated_dict = {}
        valid_keys = ["email", "name", "password"]

        # validate the input
        for key in result:
            app.logger.debug(str(key) + ": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue
            value = result[key].strip()
            if not value or value == "undefined":
                validated = False
                break
            validated_dict[key] = value

        if result["user_role"] == "student":
            validated_dict["user_id"] = result["student_id"]
        else:
            #generate lecturer id
            validated_dict["user_id"] = "L" + result["email"].split("@")[0][:5]

        # code to validate and add user to database goes here
        app.logger.debug("validation done")
        if validated:
            app.logger.debug("validated dict: " + str(validated_dict))
            email = validated_dict["email"]
            name = validated_dict["name"]
            password = validated_dict["password"]
            user_id = validated_dict["user_id"]

            # if this returns a user, then the email already exists in database
            user = User.query.filter_by(email=email).first()
            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash("Email address already exists")
                app.logger.debug("email exists")
                return render_template("pre3/signup.html")

            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(
                email, name
            )
            if result["user_role"] == "student":
                new_student = Student(
                    email=email,
                    name=name,
                    password=generate_password_hash(password, method="sha256"),
                    role="student",
                    user_id=user_id,
                )
                db.session.add(new_student)
                db.session.commit()
                return redirect(url_for("pre3_login"))
            new_lecturer = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method="sha256"),
                role="lecturer",
                user_id=user_id,
            )
            # add the new user to the database

            db.session.add(new_lecturer)
            db.session.commit()
            return redirect(url_for("pre3_signup_success"))

    return render_template("pre3/signup.html")

@app.route("/pre3/signup/success", methods=("GET", "POST"))
def pre3_signup_success():
    if request.referrer != url_for("pre3_signup"):
        abort(401)
    return render_template("pre3/signup_success.html")

@app.route("/pre3/login", methods=("GET", "POST"))
def pre3_login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        if request.method == "POST":
            # login code goes here
            email = request.form.get("email")
            password = request.form.get("password")
            remember = bool(request.form.get("remember"))
            user = User.query.filter_by(email=email).first()

            # check if the user actually exists
            # take the user-supplied password, hash it, and compare it to the
            # hashed password in the database

            if not user or not check_password_hash(user.password, password):
                flash("Please check your login details and try again.")
                # if the user doesn't exist or password is wrong, reload the page
                return redirect(url_for("pre3_login"))

            # if the above check passes, then we know the user has the right
            # credentials
            login_user(user, remember=remember)
            next_page = request.args.get("next")
            if user.role == "admin":
                return redirect(url_for("pre3_admin_dashboard"))
            if user.role == "lecturer":
                return redirect(url_for("pre3_teacher"))
            if user.role == "student":
                return redirect(url_for("pre3_student"))
            return redirect(next_page)

        return render_template("pre3/login.html")
    except SQLAlchemyError as e:
        app.logger.error(e)
        return redirect(url_for("pre3_500"))

    except AttributeError as e:
        app.logger.error(e)
        return redirect(url_for("pre3_500"))

@app.route("/pre3/teacher")
@login_required
def pre3_teacher():
    return render_template("pre3/teacher.html")


@app.route("/pre3/create_course", methods=("GET", "POST"))
@login_required
def pre3_created_course():
    if request.method == "POST":
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get("id", "")
        validated = True
        validated_dict = dict()
        valid_keys = [
            "course_id",
            "abbr",
            "name",
            "year",
            "description",
            "credits",
            "department",
        ]

        # validate the input
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == "undefined":
                validated = False
                break
            validated_dict[key] = value

        if validated:
            app.logger.debug(f"validated dict: {validated_dict}")

            entry = Course(**validated_dict)
            app.logger.debug(str(entry))
            db.session.add(entry)
            # if there is an id_ already: update contact

            db.session.commit()

        return redirect(url_for("pre3_courses"))
    return render_template("pre3/created_course.html")



@app.route("/pre3/courses")
@login_required
def pre3_courses():
    db_course = Course.query.all()

    courses = list(map(lambda x: x.to_dict(), db_course))

    app.logger.debug(str(courses))

    return render_template("pre3/courses.html", courses=courses)
