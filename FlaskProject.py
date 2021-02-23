# On windows: To start flask server WITH DEBUGGER
# 1) $env:FLASK_APP= "FlaskProject.py"
# 2) $env:FLASK_DEBUG=1
# 3) flask run

# Notes:
# The static folder holds all static files. You can use {{url_for('static','')}} to reference a static file on the file server.
# {{url_for('')}} this can be used to find the path of a given route, based off our routes in our main application 'FlaskProject.py'
### This project serves as an example on how to use and maintain a Project using the Flask MicroFramework. ###
from flask import Flask, render_template, url_for, flash, request, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Fk3yN9vnSECRETdUKlE6'       # Cookie Secret Key


@app.route("/home")
@app.route("/")  # Root Page.
def home():
    return render_template('home.html', title="Home")


@app.route("/about")  # About Page
def about():
    return render_template('about.html', title="About")


@app.route("/account")  # Account Page
def account():
    return render_template('account.html',  title="Account")


@app.route("/shop")  # Shop Page
def shop():
    return render_template('shop.html', title="Shop")


@app.route("/login")  # Login Page
def login():
    loginForm = LoginForm()
    return render_template('login.html', title="Login", form=loginForm)


# Register Page, Accepts POST and GET requests.
@app.route("/register", methods=['GET', 'POST'])
def register():
    registerForm = RegistrationForm()
    if registerForm.validate_on_submit():
        # Flash a message.
        flash(f'Account created for {registerForm.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=registerForm)


if __name__ == '__main__':
    app.run(debug=True)
