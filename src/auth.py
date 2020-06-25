from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db, sql_queries

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """Returns the template for the login Page.

    Returns:
        [render_template]: [login.html]
    """
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """
    Login controller. Checks if Email and Password are in the database 
    and returns the profile view if successfull. 
    """
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please Check your login Details')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    """
    Controller for the signup Process.
    Returns the Signup Viev
    """
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    Registration Controller Function. Checks if 
    Email Adress exists. If it doesn`t it adds
    a new user to the database.
    Returns view for the login

    """
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    hname = '{0}|{1}'.format(name, email)
    hid = sql_queries.new_household(hname)
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.login'))

    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'), household_id=hid)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    """
    Logout Controller. Returns Index view
    """
    logout_user()
    return redirect(url_for('main.index'))
