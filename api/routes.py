import cv2
from flask import Blueprint, request, send_from_directory, render_template,current_app
from image_processing.process_image import process_image
import os

api = Blueprint('api', __name__)

@api.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(original_path)

        # 插入步骤二的代码来获取前端参数
        gray_levels = int(request.form.get('gray_levels', 0))  # 默认值为0，表示不更改
        resolution = int(request.form.get('resolution', 100))  # 默认值为100，表示不更改
        distance_metric = request.form.get('distance_metric', 'l1')  # 默认值为'l1'
        resolution_rata = resolution

        # 修改这一行来传递新参数
        resolution, gray, edges = process_image(original_path, gray_levels, resolution, distance_metric)

        resolution_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "resolution_" + file.filename)
        gray_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "gray_" + file.filename)
        edges_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "edges_" + file.filename)

        cv2.imwrite(resolution_path, resolution)
        cv2.imwrite(gray_path, gray)
        cv2.imwrite(edges_path, edges)

        return render_template("index.html",
                               original='uploads/' + file.filename,
                               resolution='uploads/' + "resolution_" + file.filename,
                               gray='uploads/' + "gray_" + file.filename,
                               edges='uploads/' + "edges_" + file.filename,
                               gray_levels=gray_levels,  # 添加新的模板变量
                               resolution_percent=resolution_rata,  # 添加新的模板变量
                               distance_metric=distance_metric)  # 添加新的模板变量

