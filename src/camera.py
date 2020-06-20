from flask import Blueprint, render_template, url_for, redirect, request, flash,Response,send_file,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
import numpy as np
from . import db
import cv2
from pyzbar.pyzbar import decode
import base64
from PIL import Image
import io

camera = Blueprint('camera', __name__)

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

def __base64ToImage(base64_string):
    imgdata = base64.b64decode(str(base64_string[22:]))
    image = Image.open(io.BytesIO(imgdata))
    #nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    return cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)




@camera.route('/scanner')
def scanner():
    return render_template('scanner.html')
    
@camera.route('/takePic', methods=['POST'])
def takePic():
    """
    Gets the Picture and tries to find a barcode. 
    If yes then return the barcode and the manupulated picture
    else try again
    """
    
    if request.method == 'POST':
        data_uri = request.form['photo']
        
        img = __base64ToImage(data_uri)
        myData = b"None"
        for barcode in decode(img):
            myData = barcode.data.decode("utf-8")
            #transform image to numpy array
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            #add rectangles
            cv2.polylines(img,[pts],True,(255,0,255),5)
            pts2 = barcode.rect
            fontweight = 1
            color = (255,0,255)
            fontScale = 0.9
            cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,fontScale,color,fontweight,cv2.LINE_AA)
        imgencode, buffer = cv2.imencode(".jpg",img)
        image = base64.b64encode(buffer.tostring()).decode('ascii')
        try:
            barcode = myData.decode("ascii")
        except:
            barcode = myData
        response = make_response(render_template('scanner.html',pic=image,barcode=barcode))
    
    return response