from flask import Flask, request, render_template, send_from_directory
import cv2
import os
from api.routes import api
from image_processing.process_image import process_image
from api.routes import upload_file

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('static/uploads/'):
    os.makedirs('static/uploads/')





@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


app.register_blueprint(api)  # 注册蓝图

if __name__ == '__main__':
    app.run(debug=True)
