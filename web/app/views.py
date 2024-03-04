import json
import secrets
import string

from flask import jsonify, render_template, request, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager, oauth
from app.models.contact import Contact
from app.models.authuser import AuthUser, PrivateContact
from app.models.user import User

# from app import oauth


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return AuthUser.query.get(int(user_id))


@app.route("/crash")
def crash():
    return 1 / 0


@app.route("/db")
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "<h1>db works.</h1>"
    except Exception as e:
        return "<h1>db is broken.</h1>" + str(e)


@app.route("/lab04")
def lab04_bootstrap():
    return app.send_static_file("lab04_bootstrap.html")


@app.route("/", methods=("GET", "POST"))
@login_required
def lab10_phonebook():
    if request.method == "POST":
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get("id", "")
        validated = True
        validated_dict = dict()
        valid_keys = ["firstname", "lastname", "phone"]

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
            app.logger.debug("validated dict: {validated_dict}")
            # if there is no id: create a new contact entry
            if not id_:
                validated_dict["owner_id"] = current_user.id
                # entry = Contact(**validated_dict)
                entry = PrivateContact(**validated_dict)
                app.logger.debug(str(entry))
                db.session.add(entry)
            # if there is an id already: update the contact entry
            else:
                # contact = Contact.query.get(id_)
                contact = PrivateContact.query.get(id_)
                if contact.owner_id == current_user.id:
                    contact.update(**validated_dict)

            db.session.commit()

        return lab10_db_contacts()
    return render_template("lab10_phonebook.html")


@app.route("/lab10/contacts")
@login_required
def lab10_db_contacts():
    # db_contacts = Contact.query.all()
    db_contacts = PrivateContact.query.filter(
        PrivateContact.owner_id == current_user.id
    )
    contacts = list(map(lambda x: x.to_dict(), db_contacts))
    app.logger.debug(f"DB Contacts: {contacts}")

    return jsonify(contacts)


@app.route("/lab10/remove_contact", methods=("GET", "POST"))
@login_required
def lab10_remove_contacts():
    app.logger.debug("LAB10 - REMOVE")
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get("id", "")
        try:
            # contact = Contact.query.get(id_)
            contact = PrivateContact.query.get(id_)
            if contact.owner_id == current_user.id:
                db.session.delete(contact)
                db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing contact with id {id_}: {ex}")
            raise
    return lab10_db_contacts()


@app.route("/lab11")
@login_required
def lab11_index():
    return render_template("lab11/index.html")


@app.route("/lab11/profile")
@login_required
def lab11_profile():
    return render_template("lab11/profile.html")


@app.route("/lab11/login", methods=("GET", "POST"))
def lab11_login():
    if request.method == "POST":
        # login code goes here
        email = request.form.get("email")
        password = request.form.get("password")
        remember = bool(request.form.get("remember"))

        user = AuthUser.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for("lab11_login"))

        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("lab11_profile")
        return redirect(next_page)

    return render_template("lab11/login.html")


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


@app.route("/lab11/signup", methods=("GET", "POST"))
def lab11_signup():

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
                return redirect(url_for("lab11_signup"))

            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(email, name)
            new_user = AuthUser(
                email=email,
                name=name,
                password=generate_password_hash(password, method="sha256"),
                avatar_url=avatar_url,
            )
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("lab11_login"))
    return render_template("lab11/signup.html")


@app.route("/lab11/logout")
@login_required
def lab11_logout():
    logout_user()
    return redirect(url_for("lab11_index"))


@app.route("/google/")
def google():
    if current_user.is_authenticated:
        return redirect(url_for("pre3_profile"))

    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url=app.config["GOOGLE_DISCOVERY_URL"],
        client_kwargs={"scope": "openid email profile"},
    )

    # Redirect to google_auth function
    redirect_uri = url_for("google_auth", _external=True)
    app.logger.debug("Redirect URI: " + redirect_uri)

    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/google/auth")
def google_auth():
    if current_user.is_authenticated:
        return redirect(url_for("pre3_profile"))

    token = oauth.google.authorize_access_token()
    app.logger.debug(str(token))

    userinfo = token["userinfo"]
    app.logger.debug(" Google User " + str(userinfo))
    email = userinfo["email"]
    user = AuthUser.query.filter_by(email=email).first()

    if not user:
        name = userinfo.get("given_name", "") + " " + userinfo.get("family_name", "")
        random_pass_len = 8
        password = "".join(
            secrets.choice(string.ascii_uppercase + string.digits)
            for i in range(random_pass_len)
        )
        picture = userinfo["picture"]
        new_user = AuthUser(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256"),
            avatar_url=picture,
        )
        db.session.add(new_user)
        db.session.commit()
        user = AuthUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect(url_for("pre3_profile"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("pre3_profile"))
