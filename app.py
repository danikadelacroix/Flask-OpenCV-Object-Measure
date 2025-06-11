from flask import Flask, render_template, request, send_from_directory
import cv2
import os
import uuid
from utlis import getContours, warpImg, findDis, reorder

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
PROCESSED_FOLDER = "static/processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file.filename == "":
            return render_template("index.html", error="No file selected.")

        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(img_path)

        img = cv2.imread(img_path)
        scale = 3
        wP, hP = 210 * scale, 297 * scale
        imgContours, conts = getContours(img, minArea=50000, filter=4)

        if len(conts) != 0:
            biggest = conts[0][2]
            imgWarp = warpImg(img, biggest, wP, hP)

            imgContours2, conts2 = getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=False)
            measurements = []

            if len(conts2) != 0:
                for obj in conts2:
                    nPoints = reorder(obj[2])
                    nW = round(findDis(nPoints[0][0] // scale, nPoints[1][0] // scale) / 10, 1)
                    nH = round(findDis(nPoints[0][0] // scale, nPoints[2][0] // scale) / 10, 1)

                    x, y, w, h = obj[3]
                    cv2.arrowedLine(imgWarp, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[1][0][0], nPoints[1][0][1]), (255, 0, 255), 2, 8, 0, 0.05)
                    cv2.arrowedLine(imgWarp, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[2][0][0], nPoints[2][0][1]), (255, 0, 255), 2, 8, 0, 0.05)
                    cv2.putText(imgWarp, f"{nW}cm", (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2,
                                (255, 0, 255), 2)
                    cv2.putText(imgWarp, f"{nH}cm", (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2,
                                (255, 0, 255), 2)
                    measurements.append((nW, nH))

            output_filename = f"{uuid.uuid4().hex}.jpg"
            output_path = os.path.join(PROCESSED_FOLDER, output_filename)
            cv2.imwrite(output_path, imgWarp)

            return render_template("index.html",
                                   image_path=output_path,
                                   measurements=measurements)

        else:
            return render_template("index.html", error="No A4 paper detected.")

    return render_template("index.html")

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    app.run(debug=True)
