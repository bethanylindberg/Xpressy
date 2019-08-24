#################################################
# Imports
#################################################
from flask import Flask, jsonify, render_template, redirect, request
from prediction import processImage
from keras.models import load_model
from datetime import datetime
import os


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

#Credit to github.com/ferrygun for def allowed_file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#################################################
# Flask Setup
#################################################
app = Flask(__name__,static_url_path='/static')

#################################################
# Flask Routes
#################################################
@app.route("/",methods=['GET'])
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/about")
def about():
    """Return the about page."""
    return render_template("about.html")


@app.route("/details")
def details():
    """Return the details page."""
    return render_template("details.html")


@app.route("/home")
def home():
    """Return the homepage."""
    return redirect("/")

@app.route('/predict', methods=['GET','POST'])
def prediction():
    path = datetime.now().strftime('%Y-%m-%d%H:%M:%S')

    if request.method == 'POST':
        image = request.files['file']

        if image and allowed_file(image.filename):
            img = processImage(image,path)
            prediction = model.predict(img)
            model = load_model("emotion_model_trained.h5")
            prediction = model.predict(img)

            pred_dict = {}

            pred_dict["Image_ID"] = f"{path}.jpg"
            # pred_dict["label"] = input_label
            pred_dict["angry_pred"] = round(prediction[0][0]*100,2)
            pred_dict["disgust_pred"] = round(prediction[0][1]*100,2)
            pred_dict["fear_pred"] = round(prediction[0][2]*100,2)
            pred_dict["happy_pred"] = round(prediction[0][3]*100,2)
            pred_dict["neutral_pred"] = round(prediction[0][4]*100,2)
            pred_dict["sad_pred"] = round(prediction[0][5]*100,2)
            pred_dict["surprise_pred"] = round(prediction[0][6]*100,2)

    return render_template('predict.html', pred_dict=pred_dict, imagesource='static/uploads/' + path)
    # return jsonify(pred_dict,image)   

from flask import send_from_directory

if __name__ == "__main__":
    app.run()