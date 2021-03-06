#!flask/bin/python
# (c) R. D. Scanlon 2016

r"""
Microblog Models

Handles the data class definitions for the SQLALCHEMY configuration.
"""


from app import db, lm
from flask_login import UserMixin
from hashlib import md5


class User(db.Model):
    """
    Microblog User class definition.
    """
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), index=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    # todo: Add follower functionality.

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2

        # If nickname is not unique, add a number to the end, and continually
        # increment until a unique nickname is found.
        while True:
            new_nickname = nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def get_id(self):
        return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.nickname

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' \
               % (md5(self.email.encode('utf-8')).hexdigest(), size)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
