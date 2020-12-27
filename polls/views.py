from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden
from .models import Upload
from .forms import UploadForm
from pollsapp import settings
import base64 
import cv2,os
import numpy as np
# Create your views here.
face_cascade = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'haarcascade_frontalface_default.xml'))
"""
def upload_pic(request):
    img = request.FILES['image'].read()
    encoded = b64encode(img).decode('ascii')
    mime = "image/jpg"
    mime = mime + ";" if mime else ";"
    input_image = "data:%sbase64,%s" % (mime, encoded)    
    '''
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            m=Upload(image=image)
            m.save()
            query = Upload.objects.all()
            
    '''
    return render(request,'image.html',{'image':input_image})
#    return HttpResponseForbidden('allowed only via POST')
"""
def detect_face(image):
    img =  image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255 , 0, 0), 2)
    flip = cv2.flip(img,1)
    return flip
def pencil(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(7,7),0)
    can = cv2.Canny(blur,14,62)
    ret,img = cv2.threshold(can,50,255,cv2.THRESH_BINARY_INV)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    flip1 = cv2.flip(img,1)
    return flip1
def upload_pic(request):
    if request.method == 'POST':
        img = request.FILES['image']
        image = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        
        detect_image1 = pencil(image)
        image_content1 = cv2.imencode('.jpg', detect_image1)[1].tostring()
        encoded_image1 = base64.encodestring(image_content1)
        to_send1 = 'data:image/jpg;base64, ' + str(encoded_image1, 'utf-8')
        
        detect_image = detect_face(image)
        image_content = cv2.imencode('.jpg', detect_image)[1].tostring()
        encoded_image = base64.encodestring(image_content)
        to_send = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')
        return render(request,'image.html',{'image1':to_send,'image2':to_send1})
    return render(request,'index.html')
