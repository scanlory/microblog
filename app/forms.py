#!usr/bin/env python
# (c) R. D. Scanlon 2016

r"""
microblog Forms

Login form constructor for the microblog web app.
"""


# Imports:
from flask_wtf.form import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import User

# Functions/Classes/etc.:
class LoginForm(Form):
    """
    Generates login form for authentication of users.
    """
    user_id = StringField('user_id', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(Form):
    """
    Generates a form for editing user information.
    """
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        """
        Validates the user entered nickname to ensure that there are no collisions
        in the database.
        :return:
        """
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is in use.  CHOOSE ANOTHER.')
            return False
        return True
