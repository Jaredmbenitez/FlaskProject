# On windows: To start flask server WITH DEBUGGER
# 1) $env:FLASK_APP="FlaskProject.py"
# 2) $env:FLASK_DEBUG=1
# 3) flask run
# FOR MAC USERS
# 1) set FLASK_APP="FlaskProject.py"
# 2) export FLASK_APP="FlaskProject.py"
# 3) set FLASK_DEBUG=1
# 4) export FLASK_DEBUG=1
#   git fetch
#   git pull origin dev:dev
#
# 5) flask run

# Notes:
### This project serves as an example on how to use and maintain a Project using the Flask MicroFramework. ###

# The static folder holds all static files. You can use {{url_for('static','')}} to reference a static file on the file server.
# {{url_for('')}} this can be used to find the path of a given route, based off our routes in our main application 'FlaskProject.py'

# Tools used for the creation:
# Python (Flask, SQLAlchemy, Pymysql,Flask-wtf, Email_Validators )
# html
# css
# SQL


from flask import Flask, render_template, url_for, flash, request, redirect, session
from classes.forms import RegistrationForm, LoginForm
import pymysql
import secrets
from models.User import *
from encrypt import *


app = Flask(__name__)
# Cookie Secret Key
app.config['SECRET_KEY'] = 'Fk3yN9vnSECRETdUKlE6INSBDY80n14SECRETKEY1n1k'
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.conn            # DB Connection
db.init_app(app)    # Connect to database with ORM using SQLAlchemy


@app.route("/home")
@app.route("/")  # Root Page.           --------------------------
def home():

    return render_template('home.html', title="home",)


@app.route("/about")  # About Page      --------------------------
def about():
    return render_template('about.html', title="About")


@app.route("/account")  # Account Page  --------------------------
def account():
    if "username" in session:
        user = session["username"]
        return render_template('account.html', title="Account", user=user)

    return render_template('account.html',  title="Account")


@app.route("/shop")  # Shop Page        --------------------------
def shop():
    return render_template('shop.html', title="Shop")
# adding stuff to shop branch


# Login Page, Accepts POST and GET requests --------------------------
@app.route("/login", methods=['GET', 'POST'])
def login():

    # Create new Form from LoginForm Class
    loginForm = LoginForm()
    # Check for validation errors.
    if loginForm.validate_on_submit():
        # Check request method
        if request.method == "POST":

            givenPass = loginForm.password.data
            givenUser = loginForm.username.data
            DBUserObject = User.find_user_by_username(givenUser)

            # Check given password against Database Password
            if check_encrypted_password(givenPass, DBUserObject.password):
                # Declare Session Variables
                loggedInUser = User.find_user_by_username(
                    loginForm.username.data)
                session["username"] = loggedInUser.username
                session["email"] = loggedInUser.email
                session["logged_in"] = True
                # Flash a success message.
                flash('You have been logged in!', 'success')
                # Redirect User back to homepage on login.
                return redirect(url_for('home'))
            else:
                ('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=loginForm)


# Register Page, Accepts POST and GET requests. --------------------------
@ app.route("/register", methods=['GET', 'POST'])
def register():
    # Create new Form from RegistrationForm Class
    registerForm = RegistrationForm()
    # Check if any validation errors occured.
    if registerForm.validate_on_submit():
        # Create new user object from form information
        newUser = User(username=registerForm.username.data,
                       password=encrypt_password(registerForm.password.data), email=registerForm.email.data)
        # Add and commit the object to our database
        db.session.add(newUser)
        db.session.commit()
        # Flash a message.
        flash(f'Account created for {registerForm.username.data}!', 'success')
        # Redirect User back to homepage if validation succeeded.
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=registerForm)


@app.route("/logout")  # Logout --------------------------
def logout():
    # End the current session.
    session.clear()
    # Flash a message.
    flash(f'You have been logged out!', 'success')
    # Redirect to login page
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
