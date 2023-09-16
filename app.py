from flask import Flask, request, render_template, send_from_directory
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('static/uploads/'):
    os.makedirs('static/uploads/')


def process_image(image_path):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (500, 500))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 100, 200)
    return img_resized, img_gray, edges


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(original_path)

        resized, gray, edges = process_image(original_path)

        resized_path = os.path.join(app.config['UPLOAD_FOLDER'], "resized_" + file.filename)
        gray_path = os.path.join(app.config['UPLOAD_FOLDER'], "gray_" + file.filename)
        edges_path = os.path.join(app.config['UPLOAD_FOLDER'], "edges_" + file.filename)

        cv2.imwrite(resized_path, resized)
        cv2.imwrite(gray_path, gray)
        cv2.imwrite(edges_path, edges)

        return render_template("index.html",
                               original='uploads/' + file.filename,
                               resized='uploads/' + "resized_" + file.filename,
                               gray='uploads/' + "gray_" + file.filename,
                               edges='uploads/' + "edges_" + file.filename)


if __name__ == '__main__':
    app.run(debug=True)
