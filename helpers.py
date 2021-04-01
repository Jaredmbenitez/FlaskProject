
from base64 import b64encode
import random


def generateRandomImage():
    obj = Photos.query.all()
    image = b64encode(obj[1].image).decode("utf-8")
    return obj
