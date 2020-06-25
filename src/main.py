"""Module with main flask logic"""
from flask import Blueprint, render_template, request, make_response, redirect, current_app, flash, json
from flask_login import login_required, current_user
import src.sql_queries as db
import src.camera as camera
import datetime
from . import sio
import base64
main = Blueprint('main', __name__)


@sio.on('videostream')
def checkbarcode(data):
    with open('test3.png', 'wb') as file:
        file.write(base64.b64decode(data[22:]))
    image, scancode = camera.barcode_locater(data)
    if scancode != "None":
        response = {"image": image, "code": scancode}
        id = db.is_scancode(scancode)
        if id:
            pid = db.get_product_id(scancode)
            pname = db.get_product_name(pid)
            response["message"] = pname
        sio.emit('response_back', response)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    table_ = db.get_inventory(current_user.household_id)
    expired = []
    for item in table_:
        name = item[1]
        due_date__string = item[2]
        due_date = datetime.datetime.strptime(due_date__string, "%Y-%M-%d")
        today = datetime.datetime.today()

        if due_date <= today:
            expired.append((name, due_date__string))

    return render_template('profile.html', name=current_user.name, table=table_, expired=expired)


@main.route('/newProduct')
@login_required
def new_product(barcode=''):
    categories = db.get_all_product_categories()
    return render_template('newProduct.html', categories=categories, barcode=barcode)


@main.route('/newProductEntry', methods=['POST'])
@login_required
def new_product_entry():
    product_id = db.new_product(request.form['name'], db.get_product_category_id_byname(
        request.form['group']), request.form['discription'])
    db.link_code_product(request.form['barcode'], product_id)
    return make_response(new_item())


@main.route('/newItem', methods=['POST'])
@login_required
def new_item():
    if request.method == 'POST':
        code = request.form['barcode']

        if db.is_scancode(code):
            pid = db.get_product_id(code)
            pname = db.get_product_name(pid)
            return render_template('newItem.html', pname=pname, pid=pid, hid=current_user.household_id)

        return new_product(barcode=request.form['barcode'])

    return redirect(new_product())


@main.route('/newItemEntry', methods=['POST'])
@login_required
def new_item_entry():
    db.new_item(request.form['hid'], request.form['pid'], request.form['date'])
    return profile()


@main.route('/deleteItem/<item_id>')
@login_required
def delete_item(item_id):
    print(item_id)
    db.delete_item(item_id)
    inventory = db.get_inventory_by_product(current_user.household_id)
    return render_template('tableviews/allProducts.html', inventory=inventory)
####################################
# Reciepes
####################################


@main.route('/allRecipes')
def all_recipes():
    recipes = db.get_all_recipe()
    return render_template('tableViews/allRecipes.html', recipes=recipes)


@main.route('/recipeDetails/<recipe_id>', methods=['POST', 'GET'])
def recipe_details(recipe_id):
    details = db.get_recipe_details(recipe_id)
    inventory = db.get_invetory_for_Recipe(
        current_user.household_id, recipe_id)
    print(details)
    return render_template('recipeDetails.html', details=details, inventory=inventory)


@main.route('/newRecipe')
@login_required
def new_recipe():
    return render_template('newRecipe.html')


@main.route('/newRecipeEntry', methods=['POST'])
@login_required
def new_recipe_entry():
    db.new_recipe(request.form['name'], request.form['instructions'],
                  request.form['dificulty'], request.form['time'])
    return new_ingridient()


@main.route('/newIngredient')
@login_required
def new_ingridient():
    recipes = db.get_all_recipe()
    products = db.get_inventory(current_user.household_id)
    print(products)
    return render_template('newIngredient.html', recipes=recipes, products=products)


@main.route('/newIngredientEntry', methods=['POST'])
@login_required
def new_ingridient_entry():
    db.new_ingredient(
        request.form['recipe_id'], request.form['product_id'], request.form['amount'])
    return new_ingridient()


@main.route('/scanner')
@login_required
def scanner():
    return render_template('scanner.html')


@main.route('/scan', methods=['POST'])
@login_required
def scan():
    if request.method == 'POST':
        image, scancode = camera.barcode_locater(request.form['photo'])

    return make_response(render_template('scanner.html', pic=image, barcode=scancode))


@main.route('/dbraw')
@login_required
def dbraw():
    db.delete_scancode(42141112)
    return db.all_tables()


####################################
# Products
####################################
@main.route('/allProducts')
@login_required
def allProducts():
    inventory = db.get_inventory_by_product(current_user.household_id)
    print(inventory)
    return render_template('tableviews/allProducts.html', inventory=inventory)


@main.route('/productDetails/<product_id>')
@login_required
def product_details(product_id):
    details = db.get_inventory_details(current_user.household_id, product_id)
    name = details[0][1]
    print(details)
    return render_template('productDetails.html', details=details, name=name)

####################################
# Settings
####################################


@main.route("/settings")
@login_required
def settings():
    categories = db.get_all_product_categories()

    return render_template('settings/settings.html', categories=categories)


@main.route("/settings/newCategory", methods=['POST', 'GET'])
def newCategory():
    if request.method == 'POST':
        category = db.new_product_category(request.form['category'])
        flash("Category added successfully")
        return render_template('settings/settings.html')
    categories = db.get_all_product_categories()
    return render_template('settings/newCategory.html', categories=categories)


def info(text):
    return render_template('info.html', text=text)
