from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(session_options={"autoflush": False})
#  user Class represents user table in MYSQL database 'precious'


class User(db.Model):
    __tablename__ = 'user'  # User table in our Database

    # Each column is an attribute of our User Object.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    bio = db.Column(db.String(255))
    num_sales = db.Column(db.Integer)
    num_purchases = db.Column(db.Integer)
    profile_picture = db.Column(db.LargeBinary)
    role = db.Column(db.String(255))

    # This method is how the object is printed out.

    def __repr__(self):
        return f"User: ('{self.id}', '{self.username}', '{self.email}')"

    # Constructor
    def __init__(self, username='', password='', email=''):
        self.username = username
        self.password = password
        self.email = email

    # Getters
    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

    # Setters
    def set_id(self, id):
        self.id = id

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_email(self, email):
        self.email = email

    # Create an object from a row in our User Table. Returns a User Object.
    def new_UserObject(id):
        db = Database()
        db.connect()
        sql = "SELECT * from user WHERE id = {0}".format(id)
        row = db.query(sql)
        row = row[0]
        newUser = User()
        newUser.set_id(row['id'])
        newUser.set_username(row['username'])
        newUser.set_password(row['password'])
        newUser.set_email(row['email'])
        return newUser

    def find_user_by_username(username):        # Returns a User Object.
        db = Database()
        db.connect()
        sql = "SELECT * from user where username = '{0}'".format(username)
        row = db.query(sql)
        row = row[0]
        newUser = User()
        newUser.set_id(row['id'])
        newUser.set_username(row['username'])
        newUser.set_password(row['password'])
        newUser.set_email(row['email'])
        return newUser
