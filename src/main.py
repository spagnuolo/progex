from base64 import b64decode
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user


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
        img = b64decode(request.form['photo'][22:])

        # Test: Write data to file.
        with open('test.png', 'wb') as file:
            file.write(img)

        scancode = img_recognition(img)

        if is_scancode(scancode):
            return render_template('newItem.html', barcode=scancode)

    return render_template('newProduct.html')

def img_recognition(image):
    return "12345"

def is_scancode(code):
    return True
