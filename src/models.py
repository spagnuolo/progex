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
    household_id = db.Column(db.Integer, Foreignkey('Household.id')) 


class Household(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime)
    product_id = db.Column(db.Integer, Foreignkey('Product.id'))

class Product_Category(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(1000))

class Recipe(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    instructions = db.Column(db.String(10000))
    dificulty = db.Column(db.Integer)
    time = db.Column(db.Integer)

class RecipeIngredients(db.Model)
    recipe_id = db.Column(db.Integer, ForeginKey('Recipe.id'))
    product_id = db.Column(db.Integer, ForeginKey('Product.id'))
    amount = db.Column(db.Integer)
