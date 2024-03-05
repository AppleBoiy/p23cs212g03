import json
import secrets
import string

from flask import jsonify, render_template, request, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager, oauth
from app.models.user import User
from app.models.authuser import AuthUser

from app.models.course import Course

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route("/db")
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "<h1>db works.</h1>"
    except Exception as e:
        return "<h1>db is broken.</h1>" + str(e)


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
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



def gen_avatar_url(email, name):
    # Generate background color based on hashed email
    bgcolor = generate_password_hash(email, method="sha256")[-6:]

    # Calculate text color based on background color
    color = hex(int("0xffffff", 0) - int("0x" + bgcolor, 0)).replace("0x", "")

    # Extract first letters of first and last names
    lname = ""
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]

    # Construct avatar URL
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




@app.route("/facebook/")
def facebook():
    if current_user.is_authenticated:
        return redirect(url_for("pre3_profile"))

    oauth.register(
        name="facebook",
        client_id="932473408460153",
        client_secret="4614a2e713bb506d69e653b9fb30814c",
        authorize_url="https://www.facebook.com/dialog/oauth",
        access_token_url="https://graph.facebook.com/oauth/access_token",
        redirect_uri=url_for("facebook_auth", _external=True),
        client_kwargs={"scope": "email"},
    )

    # Redirect to facebook_auth function
    redirect_uri = url_for("facebook_auth", _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)


@app.route("/facebook/auth/")
def facebook_auth():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    token = oauth.facebook.authorize_access_token()
    userinfo = oauth.facebook.parse_id_token(token)
    email = userinfo["email"]
    user = AuthUser.query.filter_by(email=email).first()

    if not user:
        name = userinfo.get("name", "")
        random_pass_len = 8
        password = "".join(
            secrets.choice(string.ascii_uppercase + string.digits)
            for i in range(random_pass_len)
        )
        new_user = AuthUser(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        user = AuthUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect(url_for("index"))


@app.route("/users")
def is_users():
    list = User.query.all()
    return render_template("view_db.html", lists=list)


@app.route("/x/")
def x_twitter():
    return redirect(url_for(""))
