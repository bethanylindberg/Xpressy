from flask import Flask, jsonify, render_template, redirect, request
from prediction import processImage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from datetime import datetime
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
import numpy as np

def processImage(image,path):

    #detect face in image, crop it then resize it then save it
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        face_clip = img[y:y+h, x:x+w]
        cv2.imwrite(f"static/uploads/{path}.jpg", cv2.resize(face_clip, (48,48)))

    img = load_img(f"static/uploads/{path}.jpg",target_size = (48,48),color_mode='grayscale')
    img = img_to_array(img)
    img = np.asarray(img)
    img /= 255
    img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])

    return img