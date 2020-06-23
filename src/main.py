"""Module with main flask logic"""
from flask import Blueprint, render_template, request, make_response, redirect
from flask_login import login_required, current_user
import src.sql_queries as db
import src.camera as camera

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    table_ = db.get_inventory(current_user.household_id)
    return render_template('profile.html', name=current_user.name, table=table_)


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


@main.route('/newRecipe')
def new_recipe():
    return render_template('newRecipe.html')


@main.route('/newRecipeEntry', methods=['POST'])
def new_recipe_entry():
    return str(db.new_recipe(request.form['name'], request.form['instructions'], request.form['dificulty'], request.form['time']))


@main.route('/newIngredient')
def new_ingridient():
    recipes = db.get_all_recipe()
    products = db.get_inventory(current_user.household_id)
    print(products)
    return render_template('newIngredient.html', recipes=recipes, products=products)


@main.route('/newIngredientEntry', methods=['POST'])
def new_ingridient_entry():
    db.new_ingredient(
        request.form['recipe_id'], request.form['product_id'], request.form['amount'])
    return profile()


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


def info(text):
    return render_template('info.html', text=text)
