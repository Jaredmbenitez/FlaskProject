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
##
from encrypt import *
from base64 import b64encode
import random
import secrets
import pymysql
from classes.forms import RegistrationForm, LoginForm, ReportForm, FullAddToCartForm, DigitalAddToCartForm, CopyrightAddToCartForm, PrintAddToCartForm, DigitalAndCopyrightAddToCartForm, DigitalAndPrintAddToCartForm, CopyrightAndPrintAddToCartForm 
from flask import Flask, render_template, url_for, flash, request, redirect, session
from werkzeug.utils import secure_filename
from models.Report import Report
from classes.database import Database


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


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

        tags = request.form.get("tags")
        description = request.form.get("description")
        price = request.form.get("price")
        posted_by = session['username']

        # Process image into binary data
        image = request.files["inputFile"]
        image.save(secure_filename(image.filename))
        url = image.filename
        url = convertToBinaryData(url)

        # Create new photo object and add to database.
        newPhoto = Photo(image=url, tags=tags, price=price,
                         nsfw=nsfw, posted_by=posted_by, times_purchased=times_purchased)
        # Add and commit to database
        db.session.add(newPhoto)
        db.session.commit()

        # Flash a message.
        flash(f'Image Posted', 'success')

    photos = generateXRandomPhotoObjects(9)
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


@app.route("/account/<username>")
def accountDynamic(username):
    userObj = getUserInfoByUsername(username)
    allPhotoObjects = getPhotoObjectsByUsername(username)

    if "username" in session:
        user = session["username"]
        return render_template('dynamicaccount.html', title="Account", userObj=userObj, allPhotoObjects=allPhotoObjects)

    return render_template('dynamicaccount.html',  title="Account", userObj=userObj, allPhotoObjects=allPhotoObjects)


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


@app.route("/item/<id>")
def itemDynamic(id):

    options=['print'] #test info
    length=len(options)

    photoObject = getPhotoObjectByPhotoID(id)
    incrementView(id)
    userObject = getUserInfoByUsername(photoObject.posted_by)

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

    
    #if request.method == "POST":  # When a form gets submitted
        #if cartForm.validate_on_submit():  # Check for form's validity
            #cartOption = request.form.get("option")  # Store data from the form
            # data = [reason, extra_info] # was used for early stage testing
            # Put the data into a new Report object
            #newCartItem=newCart(option=cartOption)
            #db.session.add(newCartItem)  # add to the database and commit
            #db.session.commit()
            # tell the user the report was submitted
            #flash('Item Added to Cart', 'success')
    

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
    return render_template('dynamicitem.html', title="item", form=reportForm, cartForm=cartForm, userObject=userObject, photoObject=photoObject, options=options, length=length)


@app.route("/shop")  # Shop Page        --------------------------
def shop():
    imageList = generateXRandomPhotoObjects(3)
    return render_template('shop.html', title="Shop", imageList=imageList)
# adding stuff to shop branch


@app.route("/cart")  # cart Page        --------------------------
def cart():
    return render_template('cart.html', title="Cart")
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


@app.route("/test")  # test --------------------------
def test():
    data = generateRandomPhotoObject()
    data2 = generateRandomPhotoObject()
    data3 = generateRandomPhotoObject()
    return render_template("test.html",  data=data)


if __name__ == '__main__':
    app.run(debug=True)


##### Extra Functions ######
# Returns a random photo decoded ready to be caught.
def generateRandomImage():
    # Query photo table for all entries
    obj = Photo.query.all()
    if len(obj) == 0:
        return 0
    # Choose a random entry from the table
    randomNumber = random.randint(0, len(obj) - 1)
    # Decode the image
    randomImage = b64encode(obj[randomNumber].image).decode("utf-8")
    # image can be caught in html pages by the following:
    # <img src="data:;base64,{{ image }}"/>
    return randomImage

# Returns a random Photo Object. Image has been decoded.


def generateRandomPhotoObject():

    # Query photo table for all entries
    obj = Photo.query.all()
    if len(obj) == 0:
        return
    # Choose a random entry from the table
    randomNumber = random.randint(0, len(obj) - 1)
    randomPhotoObject = obj[randomNumber]
    if type(randomPhotoObject.image) == str:
        tempImage = bytes(randomPhotoObject.image, encoding='utf-8')
    else:
        tempImage = b64encode(randomPhotoObject.image)
    tempImage = tempImage.decode("utf-8")
    randomPhotoObject.image = tempImage
    return randomPhotoObject


# Generate a number of random Photo Object
def generateXRandomPhotoObjects(x):
    objectsList = []
    for key in range(x):
        tempObj = generateRandomPhotoObject()
        # Somehow we need to check here for duplicates
        objectsList.append(tempObj)
    return objectsList


# FINISHED
def getUserIdbyUsername(user):
    # Query to find user ID
    queryObject = User.query.filter_by(username=user).first()
    return queryObject.id

# Item Page Wyatt


def getPhotoIdBy_____():
    return 0

# Account page - Alec


def getPhotoObjectsByUsername(user):
    queryObjects = Photo.query.filter_by(posted_by=user).all()
    for obj in queryObjects:
        tempImage = obj.image
        tempImage = b64encode(tempImage).decode("utf-8")
        obj.image = tempImage
    return queryObjects

# Cart page - Matthew


def getCartDatabyUserID():
    return 0


def getPhotoObjectByPhotoID(id):
    queryObject = Photo.query.filter_by(photo_id=id).first()
    tempImage = queryObject.image
    tempImage = b64encode(tempImage).decode("utf-8")
    queryObject.image = tempImage
    return queryObject


def getUserInfoByPhotoID():
    return 0

# Returns a User object given the username


def getUserInfoByUsername(user):
    userObject = User.query.filter_by(username=user).first()
    return userObject


def incrementView(id):

    db = Database()
    photoObject = Photo.query.filter_by(photo_id=id).first()
    newVal = str(photoObject.num_views + 1)
    sql = ("UPDATE photos SET num_views = " +
           newVal + " WHERE `photo_id`= " + str(id))
    db.execute(sql)
