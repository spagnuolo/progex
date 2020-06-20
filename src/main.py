from base64 import b64decode
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import base64
import cv2
import random
from pyzbar.pyzbar import decode
import random
import string
import src.sql_queries as sql

main = Blueprint('main', __name__)
################################################################
# Helper Functions
################################################################
def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/newItem', methods=['POST'])
def newItem():
    if request.method == 'POST':
        barcode = request.form['barcode']
        img = base64.b64decode(request.form['photo'][22:])
        filename = random_string_generator(12,string.ascii_letters)
        if barcode != "None":
            filename = barcode
        with open(f'src/static/images/{filename}.jpg', 'wb') as file:
            file.write(img)
        return render_template('newItem.html', barcode=barcode)


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
        # with open('test.png', 'wb') as file:
        #     file.write(img)

        scancode = img_recognition(img)

        if sql.is_scancode(scancode):
            return render_template('newItem.html', barcode=scancode)

    return render_template('newProduct.html')

def img_recognition(image):
    return "12345"
