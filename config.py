#!flask/bin/python
# (c) R. D. Scanlon 2016

r"""
Microblog Configuration

Main config for the microblog web application.
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# WTForms Configuration Parameters
WTF_CSRF_ENABLED = True
SECRET_KEY = 'WTF_KEY'

# SQLALCHEMY Configuration Parameters
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True


# Google OAuth Client Configuration
_GOOGLE_CLIENT_ID = '935847580353-hq73q3okd8tkbmt3t0bh658f2hvu49ea.apps.googleusercontent.com'
_GOOGLE_SECRET_KEY = '1GVr9GEPLgK-guajJrbG-pB5'

_FACEBOOK_CLIENT_ID = '1214891375217418'
_FACEBOOK_SECRET_KEY = '1b321ae7a763325345cc11bcd4391b10'

OAUTH_CREDENTIALS = {
    'google': {
        'id': _GOOGLE_CLIENT_ID,
        'secret': _GOOGLE_SECRET_KEY
    },
    'facebook': {
        'id': _FACEBOOK_CLIENT_ID,
        'secret': _FACEBOOK_SECRET_KEY
    }
}


# Email Server Settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None


# Administrator List
ADMINS = ['scanlory@gmail.com']