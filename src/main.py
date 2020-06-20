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

@main.route('/newProduct')
def new_product():
    return render_template('newProduct.html')

@main.route('/newProductEntry', methods=['POST'])
def new_product_entry():
    return str(request.form)


