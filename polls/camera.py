import cv2,os,urllib.request
import numpy as np
from django.conf import settings

face_cascade = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'haarcascade_frontalface_default.xml'))
video = cv2.VideoCapture(0)
class VideoCamera1(object):
    def __init__(self):
        self.video = video
    def __del__(self):
        self.video.release()
    def get_frame(self):
        _, img = self.video.read()
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255 , 0, 0), 2)
        flip = cv2.flip(img,1)
        ret , jpeg = cv2.imencode('.jpg',flip)
        return jpeg.tobytes()

class VideoCamera2(object):
    def __init__(self):
        self.video = video
    def __del__(self):
        self.video.release()
    def get_frame(self):
        _, img = self.video.read()
        image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image,(7,7),0)
        image = cv2.Canny(image,14,62)
        ret,image = cv2.threshold(image,50,255,cv2.THRESH_BINARY_INV)
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        img = image
        flip = cv2.flip(img,1)
        ret , jpeg = cv2.imencode('.jpg',flip)
        return jpeg.tobytes()