from flask_login import UserMixin
from sqlalchemy import ForeignKey
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

class Household(db.Model):
    __tablename__ = 'Household'
    id = db.Column(db.Integer, primary_key=True)

class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    product_category = db.Column(db.Integer, ForeignKey('Product_Category.id'))
class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime)
    product_id = db.Column(db.Integer, ForeignKey('Product.id'))

class Product_Category(db.Model):
    __tablename__ = 'Product_Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(1000))

class Recipe(db.Model):
    __tablename__ = 'Recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    instructions = db.Column(db.String(10000))
    dificulty = db.Column(db.Integer)
    time = db.Column(db.Integer)

class RecipeIngredients(db.Model):
    __tablename__ = 'RecipeIngredients'
    recipe_id = db.Column(db.Integer, ForeignKey('Recipe.id'), primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('Product.id'), primary_key=True)
    amount = db.Column(db.Integer)

class ScannCodes(db.Model):
    __tablename__ = 'ScannCodes'
    code = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('Product.id'))
