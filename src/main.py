from base64 import b64decode
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import base64
import cv2
from pyzbar.pyzbar import decode


main = Blueprint('main', __name__)

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
        with open('src/static/images/'+barcode, 'wb') as file:
            file.write(img)
        return render_template('newItem.html', barcode=barcode)


@main.route('/newItem')
def new_product():
    return render_template('newItem.html')

@main.route('/newItemEntry', methods=['POST'])
def new_product_entry():
    return str(request.form)


