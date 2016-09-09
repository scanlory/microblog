#!flask/bin/python
# (c) R. D. Scanlon 2016

r"""
Microblog Views

Handlers that respond to requests from web browsers or other clients.
"""

# Imports:
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, EditForm
from .models import User
from app.oauth import OAuthSignIn
from datetime import datetime


# Create the mappings from URLs / and /index.
@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    Defines the view parameters for the index page.
    :return:
    """
    user = g.user
    posts = [  # Temporary list of posts
        {
            'author': {'nickname': 'Ryan'},
            'body': 'Beautiful day in the Burgh!'
        },
        {
            'author': {'nickname': 'Laurin'},
            'body': 'Sausage review!'
        },
        {
            'author': {'nickname': 'Laurin'},
            'body': 'A great day at the meat market!'
        }
    ]

    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """
    Handles the validation of the login form and redirects to the index page
    upon successful validation of the form.
    :return:
    """

    # Check for user authentication.  If user is already authenticated, we
    # don't want to create a second login instance.

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    # Create LoginForm class instance from models.py:
    form = LoginForm()

    # Upon successful validation of the form, redirect back to the index page.
    if form.validate_on_submit():
        print('Form Validated')
        session['remember_me'] = form.remember_me.data

        return oid.try_login(form.user_id.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form)


# OAuth Authorization (facebook, google, etc.)
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


# OAuth Callback
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


# Generic Logout View
@app.route('/logout')
def logout():
    """
    Logout the current OpenID session.
    :return:
    """
    logout_user()
    return redirect(url_for('index'))


# Generate user profile page.
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User {} not found.'.format(nickname))
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)


# Generate the edit form handler.
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """
    View handler for the edit from.
    :return:
    """
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        # Obtain user information from the EditForm.
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data

        # Add and commit changes to the database.
        db.session.add(g.user)
        db.session.commit()
        flash("Your changes have been saved.")

        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


# Query DB for user information.
@lm.user_loader
def load_user(id):
    """
    Queries the application SQLALCHEMY database for a user id.
    :param id:
    :return:
    """
    return User.query.get(int(id))


@app.before_request
def before_request():
    """
    Populates the flask g variable with the current user information.
    :return:
    """
    g.user = current_user

    # Update the last seen time if the user is already authenticated.
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@oid.after_login
def after_login(resp):
    """
    Populates the login instance with user data.  If the user does not
    currently exist in the database, the user is added.

    :param resp:
    :return: 'next' or 'index', depending on the page that called the login request.
    """
    print("You've made it to the after_login function!")
    if resp.email is None or resp.email == "":
        flash('Invalid login.  Please try again.')
        return redirect(url_for('login'))

    # Query the server to see if the user currently exists in the database.
    # If the user does not exist in the database, create the entry by parsing
    # the email address added and returning the nickname.
    user = User.query.filter_by(email=resp.email).first()
    print(user)
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nikname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)

        # Add the new user and commit to the database.
        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    # Call the login_user function to register user as a valid login.
    login_user(user, remember=remember_me)

    # The 'next' redirect will return to the page that the user was trying to
    # access, but was unable to due to the lack of a current login.
    return redirect(request.args.get('next') or url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
