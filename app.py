# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 12:38:27 2023

@author: Admin
"""

import os
from uuid import uuid4

from flask import Flask, request, render_template, send_from_directory
from tensorflow.keras.preprocessing import image
import numpy as np
from keras.models import load_model

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
classes = ['acerolas','apples','Apricot','apricots','Avacado','avacados','bananas','blueberries','cantaloupes','cherries','Cherry2','coconuts','figs','grapefruits','grapes','guava','Hazelnut','Huckleberry','kiwifruit','lemons','Lychee','Mandarine','Mango','Mango Red','mangos','olives','Orange','oranges','Papaya','Passion Fruit','passionfruit','Peach','peaches','pears','pineapples','Plum','plums','pomegranates','Rambutan','raspberries','Raspberry','Redcurrant','Salak','strawberries','Strawberry','watermelons']
new_model = load_model('model.h5')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

        ttt=r'\ '
        ttt.strip()
        test_image = image.load_img(os.path.join(APP_ROOT, f"images/{filename}"), target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = new_model.predict(test_image)
        result1 = result[0]
        for i in range(6):
    
            if result1[i] == 1.:
                break;
        prediction = classes[i]

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("template.html",image_name=filename, text=prediction)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=False)
