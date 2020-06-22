"""Module with main flask logic"""
from flask import Blueprint, render_template, request, make_response
from flask_login import login_required, current_user
import src.sql_queries as sql
import src.camera as camera

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    table_ = sql.get_inventory(current_user.household_id)
    return render_template('profile.html', name=current_user.name, table=table_)

@main.route('/newItem', methods=['POST'])
def newItem():
    if request.method == 'POST':
        code = request.form['barcode']

        if sql.is_scancode(code):
            return render_template('newItem.html', barcode=code)

        return render_template('newProduct.html', barcode=code)

    return render_template('newItem.html')


@main.route('/newItem')
def new_product():
    return render_template('newItem.html')

@main.route('/newItemEntry', methods=['POST'])
def new_product_entry():
    return str(request.form)

@main.route('/scanner')
def scanner():
    return render_template('scanner.html')

@main.route('/scan', methods=['POST'])
def scan():
    if request.method == 'POST':
        image, scancode = camera.barcode_locater(request.form['photo'])

    return make_response(render_template('scanner.html', pic=image, barcode=scancode))

