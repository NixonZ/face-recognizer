import os
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO
import logging
from sys import stdout
import cv2
import numpy as np
import base64


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app,cors_allowed_origins="*")


recognModel = 'nn-models/openface.nn4.small2.v1.t7'
\
netRecogn = cv2.dnn.readNetFromTorch(recognModel)

def detectFace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('venv/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
    faces = face_cascade.detectMultiScale(gray)
    if (len(faces) == 0):
        return None,None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def face2vec(face):
    facebgr = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
    blob = cv2.dnn.blobFromImage(facebgr, 1.0 /255, (96,96))
    netRecogn.setInput(blob)
    vec = netRecogn.forward()
    return vec

def recognize(face1,face2):
    vec1 = face2vec(face1)
    vec2 = face2vec(face2)
    return vec1.dot(vec2.reshape(128,1))

def readb64(uri):
        encoded_data = uri.split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

recognModel = 'nn-models/openface.nn4.small2.v1.t7'

Videoface = None
Uploadface = None

@socketio.on('VideoImage')
def handle_message(dataURL):
    # print(dataURL)
    global Videoface
    img = readb64(dataURL)
    print('---Recieving Video Data---')
    gray , rect = detectFace(img)
    if type(rect) != type(None):
        (x, y, w, h) = rect
        Videoface = img[y:y+w, x:x+h]
        # cv2.imwrite('videoface.jpeg',img[y:y+w, x:x+h])
    else:
        Videoface = None
        print('--- No Faces detected in Video---')

@socketio.on('UploadImage')
def handle_message(dataURL):
    global Uploadface
    img = readb64(dataURL)
    print('---Recieving Uploaded image---')
    gray , rect = detectFace(img)
    if type(rect) != type(None):
        (x, y, w, h) = rect
        Uploadface = img[y:y+w, x:x+h]
        # cv2.imwrite('Uploadface.jpeg',img[y:y+w, x:x+h])
    else:
        Uploadface = None
        print('--- No Faces detected in photo---')
            
@socketio.on('Recognise')
def handle_message(dataURL):    
    if ( type(Videoface) == type(None) or type(Uploadface) == type(None)):
        socketio.emit('output','Face not recognised Try again!')
    else:
        output = recognize(Videoface,Uploadface)
        socketio.emit('output', str(output[0]))

@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")

if __name__ == '__main__':
    socketio.run(app)
