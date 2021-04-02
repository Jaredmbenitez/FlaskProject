from classes.database import Database
from flask_sqlalchemy import SQLAlchemy
from models.User import db
#  user Class represents user table in MYSQL database 'precious'


class Report(db.Model):
    __tablename__ = 'reports'  # User table in our Database

    # Each column is an attribute of our User Object.
    report_id = db.Column(db.Integer, primary_key=True)
    reported_user_id = db.Column(db.Integer)
    reported_photo_id = db.Column(db.Integer)
    report_description = db.Column(db.String(255))
    report_tags = db.Column(db.String(255))

    # This method is how the object is printed out.

    def __repr__(self):
        return f"User: ('{self.report_id}', '{self.reported_user_id}', '{self.reported_photo_id}', '{self.report_tags}', '{self.report_description}')"


""" Not needed
    # Constructor
    def __init__(self, reported_user_id='', reported_photo_id='', report_description='', report_tags=''):
        self.report_id = report_id
        self.reported_user_id = reported_user_id
        self.reported_photo_id = reported_photo_id
        self.report_description = report_description
        self.report_tags = report_tags

    # Getters
    def get_report_id(self):
        return self.report_id

    def get_reported_user_id(self):
        return self.reported_user_id

    def get_reported_photo_id(self):
        return self.reported_photo_id

    def get_report_description(self):
        return self.report_description
    
    def get_report_tags(self):
        return self.report_tags

    # Setters
    def set_report_id(self):
        self.report_id = report_id

    def set_reported_user_id(self):
        self.reported_user_id = reported_user_id

    def set_reported_photo_id(self):
        self.reported_photo_id = reported_photo_id

    def set_report_description(self):
        self.report_description = report_description
    
    def set_report_tags(self):
        self.report_tags = report_tags

    # Create an object from a row in our Report Table. Returns a Report Object.
    def new_ReportObject(report_id):
        db = Database()
        db.connect()
        sql = "SELECT * from user WHERE report_id = {0}".format(report_id)
        row = db.query(sql)
        row = row[0]
        newReport = Report()
        newReport.set_report_id(row['report_id'])
        newReport.set_reported_user_id(row['reported_user_id'])
        newReport.set_reported_photo_id(row['reported_photo_id'])
        newReport.set_report_description(row['report_description'])
        newReport.set_report_tags(row['report_tags'])
        return newReport
"""