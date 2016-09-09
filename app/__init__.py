#!flask/bin/env python
# (c) R. D. Scanlon 2016

r"""
Microblog Web App Initialization

Initialization of the Microblog Web Application.

Refer to blog.miguelgrinberg.com for a detailed description of this code.
"""

# Imports:
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, \
    MAIL_PASSWORD

# Create the flask instance for the current web app.  Apply the configuration
# from the configuration file, config.py.
app = Flask(__name__)
app.config.from_object('config')


# Create the database instance for the web app.
db = SQLAlchemy(app)

# Create the LoginManager instance and point to the login view.
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))


# Setup Logging for when app is not in debugging mode.
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler

    # Setup Email Logging
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, \
                               ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Setup File Logging
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from app import views, models
