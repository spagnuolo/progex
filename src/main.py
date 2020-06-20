from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import base64

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

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
        with open('test.png', 'wb') as file:
            file.write(base64.b64decode(request.form['photo'][22:]))

    return render_template('newItem.html', barcode="12345")
