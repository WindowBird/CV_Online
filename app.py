import os
from api.routes import api
from api.image_enhancement import enhancement_api
from flask import Flask, render_template


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists('static/uploads/'):
    os.makedirs('static/uploads/')


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/edge_detection', methods=['GET', 'POST'])
def edge_detection():
    # 这里的代码用于处理边缘检测的逻辑
    return render_template('edge_detection.html')


@app.route('/image_enhancement', methods=['GET', 'POST'])
def image_enhancement():
    return render_template('image_enhancement.html')


app.register_blueprint(api)  # 注册蓝图
app.register_blueprint(enhancement_api)

if __name__ == '__main__':
    app.run(debug=True)
