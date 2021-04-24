from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import email_validator

# These classes will generate a form in HTML based on the given attributes/ validators written in python.


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

    # Apply for admin privellages
    adminPrivellages = BooleanField('Apply for Admin Privellages')

    # Creates username field as a string input


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[
        DataRequired(),             # Required
        Length(min=2, max=20)       # Between 2 and 20 Characters
    ])

    password = PasswordField('Password', validators=[
        DataRequired()              # Required
    ])

    # Remember me field for sync with Secret Cookies.
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class ReportForm(FlaskForm):

    reason = SelectField(u'Reason', choices=[('wrongTags', 'Wrong Tags'), (
        'nsfw', 'NSFW (not labeled)'), ('copyright', 'Copyright'), ('other', 'Other')])

    extra_info = TextAreaField(
        'Additional Information (max characters:255)', validators=[Length(min=1, max=255)])

    submit = SubmitField('Submit')


class FullAddToCartForm(FlaskForm):

    option = RadioField('Options:', choices=[('digital', 'Digital: '), (
        'copyright', 'Digital & Copyright: '), ('print', 'Print: ')], default='digital')

    submit = SubmitField('Add To Cart')


class DigitalAddToCartForm(FlaskForm):

    option = RadioField('Options:', choices=[
                        ('digital', 'Digital: ')], default='digital')

    submit = SubmitField('Add To Cart')


class CopyrightAddToCartForm(FlaskForm):

    option = RadioField('Options:', choices=[
                        ('copyright', 'Digital & Copyright')], default='digital')

    submit = SubmitField('Add To Cart')


class PrintAddToCartForm(FlaskForm):

    option = RadioField('Options:', choices=[
                        ('print', 'Print')], default='digital')

    submit = SubmitField('Add To Cart')


class DigitalAndCopyrightAddToCartForm(FlaskForm):

    option = RadioField('Options:', choices=[(
        'digital', 'Digital: '), ('copyright', 'Digital & Copyright: ')], default='digital')

    submit = SubmitField('Add To Cart')


class DigitalAndPrintAddToCartForm(FlaskForm):

    option = RadioField('Options:', choices=[
                        ('digital', 'Digital: '), ('print', 'Print: ')], default='digital')

    submit = SubmitField('Add To Cart')


class CopyrightAndPrintAddToCartForm(FlaskForm):

    option = RadioField('Options:', choices=[(
        'copyright', 'Digital & Copyright: '), ('print', 'Print: ')], default='digital')

    submit = SubmitField('Add To Cart')


class ContactSellerForm(FlaskForm):

    email = StringField('Email', validators=[
        DataRequired(),             # Required
        Email()                     # Email Validator
    ])

    subject = TextAreaField('Subject (max characters:32)',
                            validators=[Length(min=1, max=32)])

    message = TextAreaField('Type your message to the seller here: ', validators=[
                            Length(min=1, max=512)])

    submit = SubmitField('Send Message')
