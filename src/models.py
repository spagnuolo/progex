from flask_login import UserMixin
from . import db

"""
Definitions of Models for the Database (Tables),
After you added new Models do:

from src import db, create_app
db.create_all(app=create_app())

need to be on the Root of the Document
"""


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
