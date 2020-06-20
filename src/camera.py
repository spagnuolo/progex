'''camera.py'''

import io
import base64
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

# cam = cv2.VideoCapture(0)
# cam.set(3,640)
# cam.set(4,480)

def __base64ToImage(base64_string):
    imgdata = base64.b64decode(str(base64_string[22:]))
    image = Image.open(io.BytesIO(imgdata))
    #nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def barcode_locater(image_data):
    """
    Gets the Picture and tries to find a barcode.
    If yes then return the barcode and the manipulated picture
    else try again
    """

    img = __base64ToImage(image_data)
    my_data = b"None"

    for barcode in decode(img):
        my_data = barcode.data.decode("utf-8")

        #transform image to numpy array
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))

        #add rectangles
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        fontweight = 1
        color = (255, 0, 255)
        font_scale = 0.9
        cv2.putText(img, my_data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, fontweight, cv2.LINE_AA)

    imgencode, buffer = cv2.imencode(".jpg", img)
    image = base64.b64encode(buffer.tostring()).decode('ascii')

    try:
        barcode = my_data.decode("ascii")
    except:
        barcode = my_data

    return image, barcode
