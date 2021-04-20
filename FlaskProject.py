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
# Import Models
from models.Report import Report
from models.Photo import Photo
from models.User import *
from models.Cart import Cart
##
from encrypt import *
import secrets
import pymysql
from classes.forms import RegistrationForm, LoginForm, ReportForm, FullAddToCartForm, DigitalAddToCartForm, CopyrightAddToCartForm, PrintAddToCartForm, DigitalAndCopyrightAddToCartForm, DigitalAndPrintAddToCartForm, CopyrightAndPrintAddToCartForm, ContactSellerForm
from flask import Flask, render_template, url_for, flash, request, redirect, session
from werkzeug.utils import secure_filename
from classes.database import Database
from functions import *


app = Flask(__name__)
# Cookie Secret Key
app.config['SECRET_KEY'] = 'Fk3yN9vnSECRETdUKlE6INSBDY80n14SECRETKEY1n1k'
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.conn            # DB Connection
db.init_app(app)    # Connect to database with ORM using SQLAlchemy


@app.route("/home", methods=['GET', 'POST'],)
# Root Page.           --------------------------
@app.route("/", methods=['GET', 'POST'],)
def home():
    # Check if image was posted
    if request.method == 'POST':
        # Grab form data
        nsfw = 0  # nsfw is false by default
        times_purchased = 0  # Initialize as 0
        if request.form.get("nsfwCheck"):
            nsfw = 1

        tags = str(request.form.get("tags")).lower()
        description = request.form.get("description")
        price = request.form.get("price")
        posted_by = session['username']
        title = request.form.get("title")

        # Process image into binary data
        image = request.files["inputFile"]
        image.save(secure_filename(image.filename))
        url = image.filename
        url = convertToBinaryData(url)

        # Create new photo object and add to database.
        newPhoto = Photo(image=url, title=title, tags=tags, price=price,
                         nsfw=nsfw, posted_by=posted_by, times_purchased=times_purchased, num_views=0)
        # Add and commit to database
        db.session.add(newPhoto)
        db.session.commit()

        # Flash a message.
        flash(f'Image Posted', 'success')

    photos = getAllExistingPhotoObjects()
    return render_template('home.html', title="Home", photos=photos)


@app.route("/about")  # About Page      --------------------------
def about():
    return render_template('about.html', title="About")


@app.route("/account")  # Account Page  --------------------------
def account():
    if "username" in session:
        user = session["username"]
        return render_template('account.html', title="Account", user=user)

    return render_template('account.html',  title="Account")


@app.route("/account/<username>", methods=['GET', 'POST'])
def accountDynamic(username):
    userObj = getUserInfoByUsername(username)
    allPhotoObjects = getPhotoObjectsByUsername(username)

    contactForm = ContactSellerForm()

    if request.method == "POST":
        if contactForm.validate_on_submit():
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")
            #!!! DATA GOES NOWHERE FOR NOW

            flash('Email Successfully Sent', 'success')

    if "username" in session:
        user = session["username"]
        return render_template('dynamicaccount.html', title="Account", userObj=userObj, allPhotoObjects=allPhotoObjects, contactForm=contactForm)

    return render_template('dynamicaccount.html',  title="Account", userObj=userObj, allPhotoObjects=allPhotoObjects, contactForm=contactForm)


# Item Page        --------------------------
@app.route("/item", methods=['GET', 'POST'])
def item():
    reportForm = ReportForm()
    if request.method == "POST":  # When a form gets submitted
        if reportForm.validate_on_submit():  # Check for form's validity
            reason = request.form.get("reason")  # Store data from the form
            extra_info = request.form.get("extra_info")
            userId = getUserIdbyUsername('root')
            # data = [reason, extra_info] # was used for early stage testing
            # Put the data into a new Report object
            newReport = Report(report_tags=reason,
                               report_description=extra_info,
                               reported_user_id=userId)
            db.session.add(newReport)  # add to the database and commit
            db.session.commit()
            # tell the user the report was submitted
            flash('Report Submitted', 'success')
        # return render_template('item.html', title="item", form=reportForm, data=data)
    return render_template('item.html', title="item", form=reportForm)


@app.route("/item/<id>", methods=['GET', 'POST'])
def itemDynamic(id):

    # test info: must be in order that appears below for testing
    options = ['digital', 'copyright', 'print']
    length = len(options)
    incrementView(id)

    if options == ['digital', 'copyright', 'print']:
        cartForm = FullAddToCartForm()
    elif options == ['digital', 'copyright']:
        cartForm = DigitalAndCopyrightAddToCartForm()
    elif options == ['digital', 'print']:
        cartForm = DigitalAndPrintAddToCartForm()
    elif options == ['copyright', 'print']:
        cartForm = CopyrightAndPrintAddToCartForm()
    elif options == ['digital']:
        cartForm = DigitalAddToCartForm()
    elif options == ['copyright']:
        cartForm = CopyrightAddToCartForm()
    elif options == ['print']:
        cartForm = PrintAddToCartForm()

    # if request.method == "POST":  # When a form gets submitted
        # if cartForm.validate_on_submit():  # Check for form's validity
        # cartOption = request.form.get("option")  # Store data from the form
        # data = [reason, extra_info] # was used for early stage testing
        # Put the data into a new Report object
        # newCartItem=newCart(option=cartOption)
        # db.session.add(newCartItem)  # add to the database and commit
        # db.session.commit()
        # tell the user the report was submitted
        # flash('Item Added to Cart', 'success')

    contactForm = ContactSellerForm()

    reportForm = ReportForm()
    if request.method == "POST":  # When a form gets submitted
        if 'submit' in request.form:
            if not "logged_in" in session:
                # create guest user and log them in, post back to same item page.
                GuestUser = createGuestUser()
                session["username"] = GuestUser.username
                session["email"] = GuestUser.email
                session["logged_in"] = True
                flash('You are now logged in as a guest user', 'success')

                return render_template('dynamicitem.html', title="item", form=reportForm, cartForm=cartForm, userObject=getUserObjectByPhotoID(id), photoObject=getDecodedImageObjectByPhotoId(id), contactForm=contactForm, options=options, length=length)
                # Add to cart after
            addItemToCart(id)
            flash(f"You have added this item to your cart!", "success")

        if reportForm.validate_on_submit():  # Check for form's validity
            reason = request.form.get('reason')  # Store data from the form
            extra_info = request.form.get('extra_info')
            userId = getUserIdbyUsername('root')
            # data = [reason, extra_info] # was used for early stage testing
            # Put the data into a new Report object
            newReport = Report(report_tags=reason,
                               report_description=extra_info,
                               reported_user_id=userId)
            db.session.add(newReport)  # add to the database and commit
            db.session.commit()
            # tell the user the report was submitted
            flash('Report Submitted', 'success')

        elif contactForm.validate_on_submit():
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")
            #!!! DATA GOES NOWHERE FOR NOW

            flash('Email Successfully Sent', 'success')

    # IMPORTANT must go just before return statement or else db.session.commit breaks the page
    photoObject = getDecodedImageObjectByPhotoId(id)
    userObject = getUserInfoByUsername(photoObject.posted_by)

    # return render_template('item.html', title="item", form=reportForm, data=data)
    return render_template('dynamicitem.html', title="item", form=reportForm, cartForm=cartForm, userObject=userObject, photoObject=photoObject, contactForm=contactForm, options=options, length=length)


@app.route("/shop")  # Shop Page        --------------------------
def shop():
    imageList = generateAllExistingPhotoObjects()
    return render_template('shop.html', title="Shop", imageList=imageList)
# adding stuff to shop branch


@app.route("/shop/<tag>")  # Shop Page        --------------------------
def shopFiltered(tag):
    imageList = generateAllExistingPhotoObjects()
    newList = []
    for obj in imageList:
        tagsString = str(obj.tags)
        if tag in tagsString:
            newList.append(obj)

    return render_template('shopFiltered.html', title="Shop", imageList=newList)
# adding stuff to shop branch


@app.route("/cart")  # cart Page        --------------------------
def cart():
    cartItems = getCartDatabyUsername(session["username"])
    itemsList = []
    subTotal = 0
    for item in cartItems:
        itemInfo = Photo.query.filter_by(photo_id=item.photo_id).first()
        itemInfo = decodeImageFromObject(itemInfo)
        itemsList.append(itemInfo)
        subTotal = subTotal + itemInfo.price

    return render_template('cart.html', title="Cart", cartData=itemsList, subTotal=subTotal)
# adding stuff to cart branch=

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
                flash('Login Unsuccessful. Please check username and password', 'danger')
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
                       password=encrypt_password(registerForm.password.data), email=registerForm.email.data, num_sales=0, num_purchases=0)
        # Add and commit the object to our database

        db.session.add(newUser)
        db.session.commit()
        # Flash a message.
        loggedInUser = User.find_user_by_username(
            registerForm.username.data)
        session["username"] = loggedInUser.username
        session["email"] = loggedInUser.email
        session["logged_in"] = True
        flash(
            f'Account created for {registerForm.username.data}! You are now logged in.', 'success')

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


@app.route("/test")  # test --------------------------
def test():
    data = session['guest']

    data2 = generateRandomPhotoObject()
    data3 = generateRandomPhotoObject()
    return render_template("test.html",  data=data)


if __name__ == '__main__':
    app.run(debug=True)
