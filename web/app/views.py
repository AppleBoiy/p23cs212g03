import json
import secrets
import string

from flask import jsonify, render_template, request, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager, oauth
from app.models.user import User
from app.models.course import Course

# from app import oauth


@app.route("/pre3/tree")
def tree():
    return render_template("pre3/tree.html")

@app.route("/<path:path>")
def catch_all(path):
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html")

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
    return redirect(url_for("pre3_login"))


@app.route("/pre3/home/student")
@login_required
def pre3_student():
    return render_template("pre3/home_student.html")

@app.route('/pre3/home/admin/create_user', methods=('GET', 'POST') )
@login_required
def pre3_created_user():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))

        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password', 'role', 'user_id']


        # validate the input
        for key in result:
            app.logger.debug(str(key)+": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
            # code to validate and add user to database goes here


        app.logger.debug("validation done")
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']
            role = validated_dict['role']
            user_id = validated_dict['user_id']
            # if this returns a user, then the email already exists in database
            user = User.query.filter_by(email=email).first()


            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash('Email address already exists')
                return redirect(url_for('pre3_admin'))


            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(email, name)
            new_user = User(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256'),
                                avatar_url=avatar_url, role=role, user_id=user_id)
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()


        return redirect(url_for('pre3_admin'))
    return render_template('pre3/created_user.html')


@app.route("/pre3/home/admin", methods=["GET", "POST"])
@login_required
def pre3_admin():
    users = User.query.all()

    if request.method == "POST":
        user_id = request.form.get("user_id")
        new_role = request.form.get("new_role")
        action = request.form.get("action")

        if action == "delete":
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
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
        return redirect(url_for("pre3_profile"))

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

        # code to validate and add user to database goes here
        app.logger.debug("validation done")
        if validated:
            app.logger.debug("validated dict: " + str(validated_dict))
            email = validated_dict["email"]
            name = validated_dict["name"]
            password = validated_dict["password"]

            # if this returns a user, then the email already exists in database
            user = AuthUser.query.filter_by(email=email).first()
            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash("Email address already exists")
                return redirect(url_for("pre3_signup"))

            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(
                email, name
            )  # assuming gen_avatar_url is defined elsewhere
            new_user = AuthUser(
                email=email,
                name=name,
                password=generate_password_hash(password, method="sha256"),
                avatar_url=avatar_url,
            )
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("pre3_login"))

    return render_template("pre3/signup.html")


@app.route("/pre3/login", methods=("GET", "POST"))
def pre3_login():
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
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("pre3/login.html")


@app.route("/pre3/teacher")
@login_required
def pre3_teacher():
    return render_template("pre3/teacher.html")

@app.route('/pre3/create_course', methods=('GET', 'POST') )
@login_required
def pre3_created_course():
   if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['course_id', 'abbr', 'name', 'year', 'description', 'credits', 'department']


        # validate the input
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value


        if validated:
            app.logger.debug(f'validated dict: {validated_dict}')


            entry = Course(**validated_dict)
            app.logger.debug(str(entry))
            db.session.add(entry)
            # if there is an id_ already: update contact



            db.session.commit()


        return pre3_db_contest()
   return render_template('pre3/created_course.html')


@app.route("/pre3/courses")
@login_required
def pre3_courses():
    db_course = Course.query.all()

    courses = list(map(lambda x: x.to_dict(), db_course))

    app.logger.debug(str(courses))

    return render_template("pre3/courses.html", courses=courses)