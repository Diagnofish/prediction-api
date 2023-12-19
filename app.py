import os

import numpy as np
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow_hub import KerasLayer
from PIL import Image


custom_objects = {'KerasLayer': KerasLayer}
app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = set({'png', "jpg", "jpeg"})
app.config["UPLOAD_FOLDER"] = "static/uploads/"
app.config["MODEL_FILE"] = "fish_disease_model.h5"
app.config["LABELS_FILE"] = "labels.txt"


def allowed_file(filename):
  return "." in filename and filename.rsplit(".", 1)[1] in app.config["ALLOWED_EXTENSIONS"]


model = load_model(app.config["MODEL_FILE"], custom_objects=custom_objects, compile=False)
with open(app.config["LABELS_FILE"], "r") as file:
  labels = file.read().splitlines()


def predict_fish_disease(image):
  # Pre-processing input image
  img = Image.open(image).convert("RGB")
  img = img.resize((224, 224))
  img_array = np.asarray(img)
  img_array = np.expand_dims(img_array, axis=0)
  normalized_image_array = img_array.astype(np.float32) / 255
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
  data[0] = normalized_image_array

  # Predicting the image
  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = labels[index]
  confidence_score = prediction[0][index]
  return class_name[2:], confidence_score


@app.route("/")
def index():
  return jsonify({
    "Hello world",
  }), 200


@app.route("/detection", methods=["POST"])
def prediction_route():
  if request.method == "POST":
    image = request.files["image"]
    if image and allowed_file(image.filename):
      # Save imput image
      filename = secure_filename(image.filename)
      image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
      image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

      class_name, confidence_score = predict_fish_disease(image_path)
      os.remove(image_path)
      
      return jsonify({
        "is_success": True,
        "confidence_score":   float(confidence_score),
        "result":     class_name,
      }), 200
    else:
      return jsonify({
        "error": "only image files (jpg, jpeg, png) are allowed",
      }), 400
  else:
    return jsonify({
      "error": "method not allowed",
    }), 405


if __name__ == "__main__":
  app.run(debug=True,
          host="0.0.0.0",
          port=int(os.environ.get("PORT", 8080)))
