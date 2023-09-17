from flask import Flask, render_template
import os
from api.routes import api

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
