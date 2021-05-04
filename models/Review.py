from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
from models.User import db
#  user Class represents user table in MYSQL database 'precious'


class Review(db.Model):
    __tablename__ = 'user_reviews'  # User table in our Database

    # Each column is an attribute of our User Object.
    review_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    review_value = db.Column((db.Integer))
    review_content = db.Column((db.String(255)))
   
