from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
from models.User import db
#  user Class represents user table in MYSQL database 'precious'


class Cart(db.Model):
    __tablename__ = 'cart'  # Cart table in our Database\
    __table_args__ = {'extend_existing': True}
    pk = db.Column(db.Integer,  primary_key=True)
    posted_by_username = db.Column(db.String(255))
    photo_id = db.Column(db.Integer)
    equipment_id = db.Column(db.Integer)
    cart_id = db.Column(db.Integer)


