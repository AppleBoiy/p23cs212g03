import json
import secrets
import string

from flask import (jsonify, render_template,
                request, url_for, flash, redirect)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager, oauth
from app.models.contact import Contact
from app.models.authuser import AuthUser, PrivateContact

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return AuthUser.query.get(int(user_id))

@app.route('/pre3')
def pre3_index():
    return render_template('pre3/index.html')

@app.route('/pre3/profile')
@login_required
def pre3_profile():
    return render_template('pre3/profile.html')

@app.route('/pre3/logout')
@login_required
def pre3_logout():
    logout_user()
    return redirect(url_for('pre3_login'))

@app.route('/pre3/signup', methods=('GET', 'POST'))
def pre3_signup():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password']

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

            # if this returns a user, then the email already exists in database
            user = AuthUser.query.filter_by(email=email).first()
            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash('Email address already exists')
                return redirect(url_for('pre3_signup'))

            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(email, name)  # assuming gen_avatar_url is defined elsewhere
            new_user = AuthUser(email=email, name=name,
                                password=generate_password_hash(password, method='sha256'),
                                avatar_url=avatar_url)
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('pre3_login'))

    return render_template('pre3/signup.html')


@app.route('/pre3/login', methods=('GET', 'POST'))
def pre3_login():
    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        user = AuthUser.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('pre3_login'))

        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('pre3_profile')
        return redirect(next_page)

    return render_template('pre3/login.html')


def gen_avatar_url(email, name):
    # Generate background color based on hashed email
    bgcolor = generate_password_hash(email, method='sha256')[-6:]

    # Calculate text color based on background color
    color = hex(int('0xffffff', 0) - int('0x'+bgcolor, 0)).replace('0x', '')

    # Extract first letters of first and last names
    lname = ''
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]

    # Construct avatar URL
    avatar_url = "https://ui-avatars.com/api/?name=" + \
                 fname + "+" + lname + "&background=" + \
                 bgcolor + "&color=" + color

    return avatar_url



@app.route('/facebook/')
def facebook():
    oauth.register(
        name='facebook',
        client_id='932473408460153',
        client_secret='4614a2e713bb506d69e653b9fb30814c',
        authorize_url='https://www.facebook.com/dialog/oauth',
        access_token_url='https://graph.facebook.com/oauth/access_token',
        redirect_uri=url_for('facebook_auth', _external=True),
        client_kwargs={'scope': 'email'}
    )

    # Redirect to facebook_auth function
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    userinfo = oauth.facebook.parse_id_token(token)
    email = userinfo['email']
    user = AuthUser.query.filter_by(email=email).first()

    if not user:
        name = userinfo.get('name','')
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                          for i in range(random_pass_len))
        new_user = AuthUser(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        user = AuthUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect(url_for('pre3_profile'))

@app.route('/x/')
def x_twitter():
    return redirect(url_for('pre3_profile'))