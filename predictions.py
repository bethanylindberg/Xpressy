
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import glob
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
#download this xml file from link: https://github.com/opencv/opencv/tree/master/data/haarcascades.

# Load the images
file_paths = []
labels = []
targets = []

emotions = ['ANGRY','DISGUST','FEAR','HAPPY','NEUTRAL','SAD','SURPRISE']
e=0
for emotion in emotions:

    for filename in glob.glob(f"Stock_Images/{emotion}/*.jpg"):
        path = filename.split('\\')[0]+'/'+filename.split("\\")[1]
        file_paths.append(path)
        labels.append(e)
        targets.append(emotion)
    e+=1


def imageProcess(img_path,image_size):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(cv2.UMat(np.float32(img)), cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        face_clip = img[y:y+h, x:x+w]  #cropping the face in image
        img = cv2.resize(face_clip, (48,48))  #resizing image then saving it
    return img

image_size = (48,48)
images = []
for path in file_paths:
    img = imageProcess(path,image_size)
    img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
    img  = img /255.0 
    images.append(img)


model = load_model("emotion_model_trained.h5")

predictions = []
for img in images:
    prediction = model.predict(img)
    prediction = prediction.reshape(1, prediction.shape[1]*prediction.shape[2]*prediction.shape[3])
    predictions.append(prediction)

print(predictions)    

