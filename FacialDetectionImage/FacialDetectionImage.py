
import numpy as np
import cv2,glob
import wget
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re



def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

def get_images(url):
    soup = make_soup(url)

    images = [img for img in soup.findAll('img')]
    print (str(len(images)) + "images found.")
    print ('Downloading images to current working directory.')

    image_links = [each.get('src') for each in images]
    cpt =0
    for each in image_links:
        filename=each.split('/')[-1]
        extension = filename.split('.')[-1]
        header = each.split(':')[0]
        if(extension =='jpg' or extension =='png'):
            if(header == 'https'):
                urllib.request.urlretrieve(each, filename)
            elif (each.startswith('//')):
                urllib.request.urlretrieve('https:'+each, filename)
            else:
                print("nothing to show !")
def detectface(file):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    img = cv2.imread(file, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    print("showing faces !! ")
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detectFaces(url):
    get_images(url)
    exts = ['*.png', '*.jpeg', '*.jpg']
    listOfImages = [f for ext in exts for f in glob.glob(ext)]
    for img in listOfImages:
        detectface(img)


detectFaces('https://fr.wikipedia.org/wiki/Friends')