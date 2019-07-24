#################################################
# Imports
#################################################
from flask import Flask, jsonify, render_template
from datetime import datetime
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route('/image', methods=['POST'])
def prediction(image):
    path = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
    #converting image to gray scale and save it
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, gray)

    #detect face in image, crop it then resize it then save it
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    path = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
    for (x,y,w,h) in faces:
        face_clip = img[y:y+h, x:x+w]
        cv2.imwrite(f"{path}.jpg", cv2.resize(face_clip, (48,48)))

    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('messigray.png',img)
        cv2.destroyAllWindows()    
        model = load_model("emotion_model_trained4.h5")
    
    img = load_img(f"{path}.jpg",target_size = (48,48),color_mode='grayscale')
    img = img_to_array(img)
    img = np.asarray(img)
    img /= 255
    img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])

    model = load_model("emotion_model_trained4.h5")
    prediction = model.predict(img)

    pred_dict = {}

    pred_dict["Image_ID"] = f"{row.ids}.jpg"
    # pred_dict["label"] = input_label
    pred_dict["angry_pred"] = round(prediction[0][0]*100,2)
    pred_dict["disgust_pred"] = round(prediction[0][1]*100,2)
    pred_dict["fear_pred"] = round(prediction[0][2]*100,2)
    pred_dict["happy_pred"] = round(prediction[0][3]*100,2)
    pred_dict["neutral_pred"] = round(prediction[0][4]*100,2)
    pred_dict["sad_pred"] = round(prediction[0][5]*100,2)
    pred_dict["surprise_pred"] = round(prediction[0][6]*100,2)

    return jsonify(pred_dict)
    
if __name__ == "__main__":
    app.run()