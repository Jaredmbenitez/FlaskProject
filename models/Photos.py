from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
from User import db
#  user Class represents user table in MYSQL database 'precious'


class Photo(db.Model):
    __tablename__ = 'photos'  # User table in our Database

    # Each column is an attribute of our User Object.
    photo_id = db.Column(db.Integer, primary_key=True)
    times_purchased = db.Column(db.Integer)
    image = db.Column(db.Column(db.BLOB))
    price = db.Column(db.Column(db.Float))
    tags = db.Column(db.Column(db.String(255)))
    nsfw = db.Column(db.Column(db.String(255)))
    posted_by = db.Column(db.Column(db.Integer))
