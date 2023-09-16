import cv2
from flask import Blueprint, request, send_from_directory
from image_processing.process_image import process_image
import os

api = Blueprint('api', __name__)

@api.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # 调用图像处理函数
        resized, gray, edges = process_image(file_path)

        # 保存处理后的图像
        cv2.imwrite(os.path.join("processed", "resized_" + file.filename), resized)
        cv2.imwrite(os.path.join("processed", "gray_" + file.filename), gray)
        cv2.imwrite(os.path.join("processed", "edges_" + file.filename), edges)

        return "Image processed and saved", 200

