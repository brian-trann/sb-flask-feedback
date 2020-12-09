from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional, Email, Length
from wtforms.fields.html5 import EmailField
import email_validator

class CreateUserForm(FlaskForm):
    '''CreateUserForm. Includes validation and messages '''
    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Password can't be blank")])
    email = EmailField("Email", validators=[InputRequired(message="Email can't be blank"), Email()])
    first_name = StringField("First Name", validators=[InputRequired(message="First name can't be blank")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Last name can't be blank")])

class LogInForm(FlaskForm):
    '''LogInForm '''
    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Password can't be blank")])


class FeedbackForm(FlaskForm):
    '''Feedback Form'''
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])