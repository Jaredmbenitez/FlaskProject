from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
from models.User import db
#  user Class represents user table in MYSQL database 'precious'


class Photo(db.Model):
    __tablename__ = 'photos'  # User table in our Database

    # Each column is an attribute of our User Object.
    photo_id = db.Column(db.Integer, primary_key=True)
    times_purchased = db.Column(db.Integer)
    image = db.Column((db.LargeBinary))
    price = db.Column(db.Float)
    tags = db.Column((db.String(255)))
    nsfw = db.Column((db.Boolean))
    posted_by = db.Column(db.Integer)

   