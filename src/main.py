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
def new_product(barcode=''):
    categories =  db.get_all_product_categories()
    return render_template('newProduct.html', categories=categories, barcode=barcode)


@main.route('/newProductEntry', methods=['POST'])
def new_product_entry():
    product_id = db.new_product(request.form['name'], request.form['group'], request.form['discription'])
    db.link_code_product(request.form['barcode'], product_id)
    return make_response(new_item())


@main.route('/newItem', methods=['POST'])
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
def new_item_entry():
    db.new_item(request.form['hid'], request.form['pid'], request.form['date'])
    return profile()


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
    db.delete_scancode(42141112)
    return db.all_tables()


def info(text):
    return render_template('info.html', text=text)
