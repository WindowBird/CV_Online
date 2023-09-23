from flask import Blueprint, request, render_template, current_app
import os
import cv2
from image_processing.linear_transforms import global_linear  # 假设这些是你的图像处理函数
from image_processing.nonlinear_transforms import log_transform
enhancement_api = Blueprint('enhancement_api', __name__)


@enhancement_api.route('/enhancement', methods=['POST'])
def image_enhancement():
    file = request.files['file']
    if file:
        original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(original_path)

        original_image = cv2.imread(original_path)
        enhancement_type = request.form.get('enhancement_type', 'linear')

        if enhancement_type == 'linear':
            enhanced_img = global_linear(original_image)
        elif enhancement_type == 'log':
            enhanced_img = log_transform(original_image)

        enhanced_filename = 'enhanced_' + file.filename
        enhanced_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], enhanced_filename)
        cv2.imwrite(enhanced_filepath, enhanced_img)

        return render_template('image_enhancement.html',
                               original='uploads/' + file.filename,
                               enhanced='uploads/' + enhanced_filename,
                               enhancement_type=enhancement_type)

