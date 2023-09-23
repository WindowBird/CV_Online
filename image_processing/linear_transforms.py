import cv2
import numpy as np


def validate_image(image):
    if image is None or not isinstance(image, (np.ndarray,)):
        raise ValueError("Invalid input image")


# 修改后的 global_linear 函数
def global_linear(image, scale_factor=2):
    validate_image(image)
    # 应用全局线性变换
    enhanced_img = cv2.convertScaleAbs(image * scale_factor)
    return enhanced_img

