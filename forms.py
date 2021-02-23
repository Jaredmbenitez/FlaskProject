from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import email_validator

# This python file will generate a form in HTML based on the given attributes/ validators written in python.


# Registration Form class. Each attribute represents an input field. Validation included.
class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[
        DataRequired(),             # Required
        Length(min=2, max=20)       # Between 2 and 20 Characters
    ])

    email = StringField('Email', validators=[
        DataRequired(),             # Required
        Email()                     # Email Validator
    ])

    password = PasswordField('Password', validators=[
        DataRequired()              # Required
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(),             # Required
        EqualTo('password')
    ])
    submit = SubmitField('Sign Up!')

    # Creates username field as a string input


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[
        DataRequired(),             # Required
        Email()                     # Email Validator
    ])

    password = PasswordField('Password', validators=[
        DataRequired()              # Required
    ])

    # Remember me field for sync with Secret Cookies.
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
