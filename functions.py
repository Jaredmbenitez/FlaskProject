from base64 import b64encode
import os
# Import Models
from models.Report import Report
from models.Photo import Photo
from models.User import *
from models.Cart import Cart
##
from FlaskProject import session

import secrets
import pymysql

import random
import secrets
from encrypt import *
from classes.database import Database
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, url_for, flash, request, redirect, session
from werkzeug.utils import secure_filename


def decodeImageFromObject(photoObject):

    if type(photoObject.image) == str:
        tempImage = bytes(photoObject.image, encoding='utf-8')
    else:
        tempImage = b64encode(photoObject.image)
    tempImage = tempImage.decode("utf-8")
    photoObject.image = tempImage
    return photoObject


def getDecodedImageObjectByPhotoId(id):
    queryObject = Photo.query.filter_by(photo_id=id).first()

    if type(queryObject.image) == str:
        tempImage = bytes(queryObject.image, encoding='utf-8')
    else:
        tempImage = b64encode(queryObject.image)
    tempImage = tempImage.decode("utf-8")
    queryObject.image = tempImage
    return queryObject


def addItemToCart(id):

    username = getUserObjectByPhotoID(id).username
    photoObject = getDecodedImageObjectByPhotoId(id)

    photo_id = photoObject.photo_id
    price = photoObject.price
    cart_id = getUserInfoByUsername(session["username"]).id

    cartItem = Cart(posted_by_username=username, photo_id=photo_id)

    newDB = Database()
    sql = f"INSERT INTO cart (`posted_by_username`, `photo_id`, `cart_id`) VALUES('" + \
        username + "'," + "'" + str(photo_id) + \
        "'," + "'" + str(cart_id) + "')"
    newDB.execute(sql)

    return 1


def getUserObjectByPhotoID(id):
    PhotoObject = Photo.query.filter_by(photo_id=id).first()
    UserObject = User.query.filter_by(username=PhotoObject.posted_by).first()
    return UserObject


def getUserInfoByUsername(user):
    userObject = User.query.filter_by(username=user).first()
    return userObject


def createGuestUser():
    username = "Guest" + str(random.randint(99, 1000))
    password = "asdfasdf"
    email = username + " @yahoo.com"
    role = "GuestUser"
    rating = 0
    GuestUser = User(username=username,
                     password=encrypt_password(password), email=email, role=role, num_sales=0, seller_rating=0, num_purchases=0)
    db.session.add(GuestUser)
    db.session.commit()
    return GuestUser


def getAllExistingPhotoObjects():
    queryObjects = Photo.query.all()
    for obj in queryObjects:
        tempImage = obj.image
        tempImage = b64encode(tempImage).decode("utf-8")
        obj.image = tempImage
    return queryObjects


def incrementView(id):

    db = Database()
    photoObject = Photo.query.filter_by(photo_id=id).first()
    newVal = str(photoObject.num_views + 1)
    sql = ("UPDATE photos SET num_views = " +
           newVal + " WHERE `photo_id`= " + str(id))
    db.execute(sql)


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
        decodeImageFromObject(obj)
    return queryObjects

# Cart page - Matthew


def getPhotoObjectByPhotoID(id):
    queryObject = Photo.query.filter_by(photo_id=id).first()
    tempImage = queryObject.image
    tempImage = b64encode(tempImage).decode("utf-8")
    queryObject.image = tempImage  # db.session.commit breaks the page after this line
    return queryObject


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def getPhotoObjectsByTag(tag):
    queryObjects = Photo.query.filter_by(tags=tag)  # NOT CORRECT CURRENTLY
    for obj in queryObjects:
        obj = decodeImageFromObject(obj)
    return queryObjects


def generateAllExistingPhotoObjects():
    queryObjects = Photo.query.all()
    for obj in queryObjects:
        obj = decodeImageFromObject(obj)
    return queryObjects


def getCartDatabyUsername(username):
    userObject = getUserInfoByUsername(username)
    queryObjects = Cart.query.filter_by(cart_id=userObject.id).all()
    return queryObjects


def deleteItemFromCart(data_id):
    db = Database()
    for id in data_id:
        sql = "DELETE FROM cart WHERE photo_id = '" + id + "'"
        result = db.delete(sql)
        if not result:
            return 0
    return 1


def addReport(reason, extra_info, userId):
    db = Database()
    sql = "INSERT INTO `reports` (reported_user_id,report_description,report_tags) VALUES ('" + \
        str(userId) + "', '" + str(extra_info) + "', '" + str(reason) + "')"
    result = db.execute(sql)
    return result


def sendPurchaseConfirmationEmail(toAddress, itemsList):

    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("preciousemailer@yahoo.com", "uzwnfwabytncppng")
    subject = "Transaction is being processed"

    body = "Your order has been accepted, and is now being processed by our systems.\n\n Please check back for a confirmation email once item is shipped. \n\n  Thank you! \n\n"
    i = 1
    for item in itemsList:
        body += str(i) + "\n" + "Seller: " + item.posted_by + "\n" + "Item: " + item.title + "\n" + \
            "Item Price: " + str(item.price) + "\n\n"
        i = i + 1

    msg = f'Subject: {subject} \n\n{body}'

    server.sendmail("preciousemailer@yahoo.com",
                    toAddress, msg)

    server.quit()


def getPhotoObjectsBySellerRating(seller_rating):
    userObjects = User.query.filter_by(seller_rating=seller_rating).all()
    newList = []
    for obj in userObjects:
        photoObjects = getPhotoObjectsByUsername(obj.username)
        for obj2 in photoObjects:
            newList.append(obj2)

    return newList


def submitUserReview(username, reviewInfo, reviewRating):
    db = Database()
    loggedInUser = session['username']
    sql = f"INSERT into `user_reviews` (user_name, review_value, review_content, review_posted_by) VALUES('{username}', '{reviewRating}', '{reviewInfo}', '{loggedInUser}')"
    result = db.insert(sql)
    if result:
        return 1
    return 0


def unlistItem(photo_id):
    db = Database()
    sql = f"DELETE FROM photos WHERE photo_id = '{photo_id}'"

    result = db.delete(sql)

    if result:
        return 1
    return 0


def updateProfilePicture(image):
    # Process image into binary data
    loggedInUser = session["username"]
    filename = secure_filename(image.filename)
    fullPath = (os.getcwd() + "/static/images/profile_pictures/" + filename)
    image.save(fullPath)
    db = Database()
    sql = f"UPDATE user SET profile_picture = '{filename}' WHERE username = '{loggedInUser}'"
    result = db.update(sql)
    return result


def getUserReviews(username):
    db = Database()
    sql = f"SELECT * FROM `user_reviews` WHERE user_name = '{username}'"
    userReviews = db.query(sql)
    for review in userReviews:
        var = User.query.filter_by(username=review["review_posted_by"]).first()
        review["profile_picture"] = var.profile_picture
    return userReviews


def getXStarReviews(username, starVal):
    db = Database()
    sql = f"SELECT * FROM `user_reviews` WHERE user_name = '{username}' AND review_value = '{starVal}' "
    return db.query(sql)


def addToTransactions(itemsList):
    username = session['username']
    db = Database()
    for item in itemsList:
        sql = f"INSERT INTO transactions (sold_by,bought_by,photo_id) VALUES ('{item.posted_by}','{username}', '{item.photo_id}')"
        result = db.insert(sql)
    return result
