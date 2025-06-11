# 📏 Object Measurement Web App

A Python + OpenCV + Flask web application to measure the real-world dimensions of rectangular objects (like cards, packages, etc.) using an A4 sheet as reference.

## Tech Stack:
- Python, OpenCV, NumPy
- Flask (web framework)
- HTML, CSS (for frontend)

## How to Run:

### 1. Install dependencies
```bash
pip install -r requirements.txt
### 2. Run the project
```
### 2. Run the project
```bash
python app.py
```
Open your browser and go to: http://127.0.0.1:5000
Upload an image containing the object placed on an A4 sheet.
The app will return the same image with overlaid dimensions in centimeters.

## Features:
-Image-based object measurement using A4 sheet as scale
-Upload & measure multiple objects per image
-Visual dimension annotations on processed image
-Clean, responsive frontend (HTML + CSS)

---

## Sample Input/Output:
- Sample image: ![Sample Input](sample_input.png)
- Output: ![Sample Output](outputIMG.png)
