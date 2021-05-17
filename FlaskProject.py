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
from models.Review import Review
##
from encrypt import *
import secrets
import pymysql
from classes.forms import RegistrationForm, LoginForm, ReportForm, FullAddToCartForm, DigitalAddToCartForm, CopyrightAddToCartForm, PrintAddToCartForm, DigitalAndCopyrightAddToCartForm, DigitalAndPrintAddToCartForm, CopyrightAndPrintAddToCartForm, ContactSellerForm, RequestTransactionLog, CreatePromo, RemovePromo
from flask import Flask, render_template, url_for, flash, request, redirect, session
from werkzeug.utils import secure_filename
from classes.database import Database
from functions import *


app = Flask(__name__)
# Cookie Secret Key
app.config['SECRET_KEY'] = 'Fk3yN9vnSECRETdUKlE6INSBDY80n14SECRETKEY1n1k'
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.conn            # DB Connection
db.init_app(app)    # Connect to database with ORM using SQLAlchemy


@app.route("/home", methods=['GET', 'POST'])
# Root Page.           --------------------------
@app.route("/", methods=['GET', 'POST'])
def home():
    # Check if image was posted
    if request.method == 'POST':
        # Grab form data
        nsfw = 0  # nsfw is false by default
        times_purchased = 0  # Initialize as 0
        print_price = None
        copyright_price = None
        if request.form.get("nsfwCheck"):
            nsfw = 1
        if request.form.get("print-price"):
            print_price = request.form.get("print-price")
        if request.form.get("copyright_price"):
            copyright_price = request.form.get("copyright_price")
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
        newPhoto = Photo(image=url, title=title, tags=tags, price=price, print_price=print_price, copyright_price=copyright_price,
                         nsfw=nsfw, posted_by=posted_by, times_purchased=times_purchased, photo_description=description, num_views=0)
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


# debug for new item page      --------------------------
@app.route("/itemUpdate")
def itemUpdate():
    return render_template('itemUpdate.html', title="itemUpdate")


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
    userReviews = getUserReviews(username)
    FiveStars = getXStarReviews(username, 5)
    OneStar = getXStarReviews(username, 4)
    TwoStars = getXStarReviews(username, 3)
    ThreeStars = getXStarReviews(username, 2)
    FourStars = getXStarReviews(username, 1)
    contactForm = ContactSellerForm()
    reportForm = ReportForm()

    if request.method == "POST":
        if contactForm.validate_on_submit():
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")
            #!!! DATA GOES NOWHERE FOR NOW

            flash('Email Successfully Sent', 'success')
            return redirect(url_for('accountDynamic', username=username))

            #!! User rating variables and validation on submit
        elif "selectUserRating" in request.form:
            flash('Review was sent', 'success')
            reviewInfo = request.form.get("review-content")
            reviewRating = request.form.get("selectUserRating")
            submitUserReview(username, reviewInfo, reviewRating)
            return redirect(url_for('accountDynamic', username=username))

            # Remove item from seller page
        elif "unlistItemButton" in request.form:
            photo_id = request.form.get('unlistItemButton')
            unlistItem(photo_id)
            flash("Item has been removed from your seller page.", "success")
            return redirect(url_for('accountDynamic', username=username))

            # Change Profile Pic
        elif "ChangeProfilePictureButton" in request.form:
            # Process image into binary data
            image = request.files["ChangeProfilePictureInput"]
            updateProfilePicture(image)
            flash("You have updated you profile picture!", "success")
            return redirect(url_for('accountDynamic', username=username))

    if "username" in session:
        user = session["username"]
        return render_template('dynamicaccount.html', title="Account", userObj=userObj, allPhotoObjects=allPhotoObjects, contactForm=contactForm, userReviews=userReviews, FiveStars=FiveStars, FourStars=FourStars, ThreeStars=ThreeStars, TwoStars=TwoStars, OneStar=OneStar, form=ReportForm)

    return render_template('dynamicaccount.html',  title="Account", userObj=userObj, allPhotoObjects=allPhotoObjects, contactForm=contactForm, userReviews=userReviews, FiveStars=FiveStars, FourStars=FourStars, ThreeStars=ThreeStars, TwoStars=TwoStars, OneStar=OneStar, form=ReportForm)


# Dynamic Admin Page  --------------------------
@app.route("/admin", methods=['GET', 'POST'])
def adminDynamic():

    if session:
        userObj = getUserInfoByUsername(session["username"])
        if userObj.role == "Admin":
            requestForm = RequestTransactionLog()
            createPromoForm = CreatePromo()
            removePromoForm = RemovePromo()
            # if request.method == "POST":
            #    if requestForm.validate_on_submit():

            # elif createPromoForm.validate_on_submit():

            # elif removePromoForm.validate_on_submit():
            return render_template('dynamicAdmin.html', title="Admin", userObj=userObj, requestForm=requestForm, createPromoForm=createPromoForm, removePromoForm=removePromoForm)
        else:
            return redirect(url_for("home"))

    else:
        return redirect(url_for("home"))


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
            if reportForm.validate_on_submit():  # Check for form's validity
                reason = request.form.get('reason')  # Store data from the form
                extra_info = request.form.get('extra_info')
                userObject = getUserObjectByPhotoID(id)
                userId = userObject.id

                addReport(reason, extra_info, userId)
                # data = [reason, extra_info] # was used for early stage testing
                # Put the data into a new Report object
                # newReport = Report(report_tags=reason,
                #                    report_description=extra_info,
                #                    reported_user_id=userId)
                # db.session.add(newReport)  # add to the database and commit
                # db.session.commit()
                # tell the user the report was submitted
                flash('Report Submitted', 'success')
                return redirect(url_for('itemDynamic', id=id))

            if not "logged_in" in session:
                # create guest user and log them in, post back to same item page.
                GuestUser = createGuestUser()
                session["username"] = GuestUser.username
                session["email"] = GuestUser.email
                session["logged_in"] = True
                flash('You are now logged in as a guest user', 'success')

                return render_template('itemUpdate.html', title="item", form=reportForm, userObject=getUserObjectByPhotoID(id), photoObject=getDecodedImageObjectByPhotoId(id), contactForm=contactForm, options=options, length=length)
                # Add to cart after
            addItemToCart(id)
            flash(f"You have added this item to your cart!", "success")

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
    return render_template('itemUpdate.html', title="item", form=reportForm, userObject=userObject, photoObject=photoObject, contactForm=contactForm, options=options, length=length)


# Shop Page        --------------------------
@app.route("/shop", methods=["GET", "POST"])
def shop():
    imageList = generateAllExistingPhotoObjects()
    if request.method == "POST":
        searchTag = request.form.get("search")
        return redirect(url_for("shopFiltered", tag=searchTag))
    return render_template('shop.html', title="Shop", imageList=imageList)

# adding stuff to shop branch


# Shop Page        --------------------------
@app.route("/shop/<string:tag>", methods=["GET", "POST"])
def shopFiltered(tag):
    imageList = generateAllExistingPhotoObjects()
    newList = []
    for obj in imageList:
        tagsString = str(obj.tags)
        if str(tag).lower() in tagsString:
            newList.append(obj)

    return render_template('shopFiltered.html', title="Shop", imageList=newList)


@app.route("/shop/<int:price>")  # Shop Page        --------------------------
def shopFilteredPrice(price):
    imageList = generateAllExistingPhotoObjects()
    newList = []
    if price == 10:
        for obj in imageList:
            if obj.price <= price:
                newList.append(obj)
    elif price == 30:
        for obj in imageList:
            if obj.price >= 10 and obj.price <= 30:
                newList.append(obj)
    elif price == 50:
        for obj in imageList:
            if obj.price >= 30 and obj.price <= 50:
                newList.append(obj)
    elif price == 55:
        for obj in imageList:
            if obj.price >= 50:
                newList.append(obj)

    elif price == 0:
        for obj in imageList:
            newList = getPhotoObjectsBySellerRating(0)
    elif price == 1:
        for obj in imageList:
            newList = getPhotoObjectsBySellerRating(1)
    elif price == 2:
        for obj in imageList:
            newList = getPhotoObjectsBySellerRating(2)
    elif price == 3:
        for obj in imageList:
            newList = getPhotoObjectsBySellerRating(3)
    elif price == 4:
        for obj in imageList:
            newList = getPhotoObjectsBySellerRating(4)
    elif price == 5:
        for obj in imageList:
            newList = getPhotoObjectsBySellerRating(5)

    return render_template('shopFiltered.html', title="Shop", imageList=newList)


# cart Page        --------------------------
@app.route("/cart", methods=['GET', 'POST'])
def cart():
    cartItems = getCartDatabyUsername(session["username"])
    itemsList = []
    subTotal = 0
    data_ID = 0
    fees = 0
    ID = 0
    if request.method == "POST":
        if 'remove-ind-item-button' in request.form:
            ID = request.form.get('remove-ind-item-button')
            result = deleteItemFromCart([ID])
            if result == 0:
                flash('Item Removed from cart!', 'success')
                return redirect(url_for('cart'))
            else:
                flash("Error Removing item from cart", 'danger')
                return redirect(url_for('cart'))

        data_ID = request.form.getlist("remove-item")
        result = deleteItemFromCart(data_ID)
        if result == 0:
            flash('Items Removed from cart!', 'success')
            return redirect(url_for('cart'))
        else:
            flash("No items selected. Select items to remove from cart", 'danger')

    fees = 0
    for item in cartItems:
        itemInfo = Photo.query.filter_by(photo_id=item.photo_id).first()
        itemInfo = decodeImageFromObject(itemInfo)
        if(itemInfo.photo_description and len(itemInfo.photo_description) > 100):
            itemInfo.photo_description = itemInfo.photo_description[:100]
            itemInfo.photo_description += "..."
        itemsList.append(itemInfo)
        subTotal = subTotal + itemInfo.price
        fees += itemInfo.price * 0.02

    fees = round(fees, 2)
    tax = (subTotal * 0.075)
    grandTotal = subTotal + fees + tax

    return render_template('cart.html', title="Cart", cartData=itemsList, subTotal=subTotal, tax=tax, fees=fees, grandTotal=grandTotal, ID=ID)
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
                       password=encrypt_password(registerForm.password.data), role="User", email=registerForm.email.data, num_sales=0, num_purchases=0, seller_rating=0)
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


# Shop Page        --------------------------
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cartData = getCartDatabyUsername(session["username"])
    subTotal = 0
    itemsList = []

    for item in cartData:
        itemInfo = Photo.query.filter_by(photo_id=item.photo_id).first()
        itemInfo = decodeImageFromObject(itemInfo)
        itemsList.append(itemInfo)
        subTotal = subTotal + itemInfo.price

    if request.method == "POST":
        sendPurchaseConfirmationEmail(session["email"], itemsList=itemsList)
        val = addToTransactions(itemsList)
        flash(f'Checkout Success! {val}', 'success')
        return redirect(url_for('home'))

    return render_template('checkout.html', title="Checkout", cartData=itemsList, subTotal=subTotal)
# adding stuff to shop branch


@app.route("/test")  # test --------------------------
def test():
    data = session['guest']

    data2 = generateRandomPhotoObject()
    data3 = generateRandomPhotoObject()
    return render_template("test.html",  data=data)


if __name__ == '__main__':
    app.run(debug=True)
