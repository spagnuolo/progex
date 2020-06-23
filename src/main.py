"""Module with main flask logic"""
from flask import Blueprint, render_template, request, make_response
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
def new_product():
    categories =  db.get_all_product_categories()
    return render_template('newProduct.html', categories=categories)

@main.route('/newProductEntry', methods=['POST'])
def new_product_entry():
    product_id = db.new_product(request.form['name'], request.form['group'], request.form['discription'])
    db.link_code_product(request.form['barcode'], product_id)
    return make_response(new_item(product_id))

@main.route('/newItem', methods=['POST'])
def new_item(product_id):
    code = request.form['barcode']

    if db.is_scancode(code):
        return render_template('newItem.html', pname=request.form['name'], pid=product_id, hid=current_user.household_id)

    categories =  db.get_all_product_categories()
    return render_template('newProduct.html', categories=categories)


@main.route('/newItemEntry', methods=['POST'])
def new_item_entry():
    db.new_item(request.form['hid'], request.form['pid'], request.form['date'])
    return str(request.form)+' added to Databse.'

@main.route('/scanner')
def scanner():
    return render_template('scanner.html')

@main.route('/scan', methods=['POST'])
def scan():
    if request.method == 'POST':
        image, scancode = camera.barcode_locater(request.form['photo'])

    return make_response(render_template('scanner.html', pic=image, barcode=scancode))

@main.route('/dbraw')
def dbraw():
    return db.all_tables()
