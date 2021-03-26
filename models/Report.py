from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
from User import db
#  user Class represents user table in MYSQL database 'precious'


class Report(db.Model):
    __tablename__ = 'reports'  # User table in our Database

    # Each column is an attribute of our User Object.
    report_id = db.Column(db.Integer, primary_key=True)
    reported_user_id = db.Column(db.Integer)
    reproted_photo_id = db.Column(db.Integer)
    report_description = db.Column(db.String(255))
    report_tags = db.Column(db.String(255))
