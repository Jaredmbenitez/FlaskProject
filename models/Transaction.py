from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
from User import db
#  user Class represents user table in MYSQL database 'precious'


class Transaction(db.Model):
    __tablename__ = 'transactions'  # User table in our Database

    # Each column is an attribute of our User Object.
    transaction_id = db.Column(db.Integer, primary_key=True)
    sold_by = db.Column(db.String(255))
    bought_by = db.Column(db.String(255))
    photo_id = db.Column(db.String(255))
    time_of_transaction = db.Column(db.String(255))
