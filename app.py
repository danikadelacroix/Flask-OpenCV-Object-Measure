from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import uuid
from utlis import getContours, warpImg, findDis, reorder
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            # Save uploaded file
            filename = str(uuid.uuid4()) + ".jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process image
            img = cv2.imread(filepath)
            imgContours, conts = getContours(img, minArea=50000, filter=4)

            dimensions = []
            if conts:
                biggest = conts[0][2]
                imgWarp = warpImg(img, biggest, 210 * 3, 297 * 3)

                imgContours2, conts2 = getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=False)
                for obj in conts2:
                    nPoints = reorder(obj[2])
                    nW = round((findDis(nPoints[0][0]//3, nPoints[1][0]//3)/10), 1)
                    nH = round((findDis(nPoints[0][0]//3, nPoints[2][0]//3)/10), 1)
                    dimensions.append({"width": nW, "height": nH})

            return render_template("index.html", dimensions=dimensions, image_name=filename)

    return render_template("index.html", dimensions=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)
