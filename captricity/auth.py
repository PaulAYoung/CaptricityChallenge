#!/usr/bin/env python

from passlib.context import CryptContext
from flask.ext.login import LoginManager, login_user, logout_user
from flask import Blueprint, current_app, render_template, request, send_from_directory, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from captricity.models import User, db_session

################################################
# setup login manager and hash function
###############################################

login_manager = LoginManager()

hasher = CryptContext(schemes=['sha512_crypt'])


@login_manager.user_loader
def load_user(userid):
    "Load a user by id"
    return User.query.get(userid)


################################################
# auth views
################################################

auth_views = Blueprint('auth', __name__, static_folder= "static", template_folder= "templates")

@auth_views.route('/login', methods=["GET", "POST"])
def login():
    """Login view"""

    if request.method == "GET":
        return render_template('login.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = db_session.query(User).\
            filter(User.username==username).\
            first()

        if user and hasher.verify(password, user.password):
            login_user(user)
            return redirect(url_for('base_views.index'))
        else:
            print "unverified"
            flash("Invalid username or password", 'error')
            return render_template('login.html')


@auth_views.route('/newuser', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash("Passwords don't match", "error")
            return render_template('newuser.html')
        else:
            hashword = hasher.encrypt(password)
            user = User(username=username, password=hashword)
            try:
                db_session.add(user)
                db_session.commit()
                login_user(user)
                flash("User created")
                return redirect(url_for('base_views.index'))
            except IntegrityError:
                flash("Username already exists", "error")
                return render_template('newuser.html')
    else:
        return render_template('newuser.html')


@auth_views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("base_views.index"))

