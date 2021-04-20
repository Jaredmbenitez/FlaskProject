from base64 import b64encode
# Import Models
from models.Report import Report
from models.Photo import Photo
from models.User import *
from models.Cart import Cart
##
from FlaskProject import session

import random
import secrets
from encrypt import *


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
    GuestUser = User(username=username,
                     password=encrypt_password(password), email=email)
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
        tempImage = obj.image
        tempImage = b64encode(tempImage).decode("utf-8")
        obj.image = tempImage
    return queryObjects

# Cart page - Matthew


def getCartDatabyUsername(username):
    queryObjects = Cart.query.filter_by(posted_by_username=username).all()
    return queryObjects


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
