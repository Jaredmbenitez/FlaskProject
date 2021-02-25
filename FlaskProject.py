# On windows: To start flask server WITH DEBUGGER
# 1) $env:FLASK_APP= "FlaskProject.py"
# 2) $env:FLASK_DEBUG=1
# 3) flask run

# Notes:
# The static folder holds all static files. You can use {{url_for('static','')}} to reference a static file on the file server.
# {{url_for('')}} this can be used to find the path of a given route, based off our routes in our main application 'FlaskProject.py'
### This project serves as an example on how to use and maintain a Project using the Flask MicroFramework. ###
from flask import Flask, render_template, url_for, flash, request, redirect
from classes.forms import RegistrationForm, LoginForm
import pymysql
import secrets
from flask_sqlalchemy import SQLAlchemy

# Create string to connect to database.
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
    secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fk3yN9vnSECRETdUKlE6'       # Cookie Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)    # Connect to database with ORM using SQLAlchemy

# Class represents user table.


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(100))

    # This method is how the object is printed out.
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}'"
    # Constructor

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


@app.route("/home")
@app.route("/")  # Root Page.
def home():
    return render_template('home.html', title="Home", var=conn)


@app.route("/about")  # About Page
def about():
    return render_template('about.html', title="About")


@app.route("/account")  # Account Page
def account():
    return render_template('account.html',  title="Account")


@app.route("/shop")  # Shop Page
def shop():
    return render_template('shop.html', title="Shop")


@app.route("/login", methods=['GET', 'POST'])  # Login Page
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        if (loginForm.email.data == 'admin@precious.com') and (loginForm.password.data == 'password'):
            # Flash a message.
            flash('You have been logged in!', 'success')
            # Redirect User back to homepage on login.
            return redirect(url_for('home'))
        else:
            ('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=loginForm)


# Register Page, Accepts POST and GET requests.
@ app.route("/register", methods=['GET', 'POST'])
def register():
    registerForm = RegistrationForm()
    if registerForm.validate_on_submit():
        newUser = user(username=registerForm.username.data,
                       password=registerForm.password.data, email=registerForm.email.data)
        db.session.add(newUser)
        db.session.commit()
        # Flash a message.
        flash(f'Account created for {registerForm.username.data}!', 'success')
        # Redirect User back to homepage if validation succeeded.
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=registerForm)


if __name__ == '__main__':
    app.run(debug=True)
