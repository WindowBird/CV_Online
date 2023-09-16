import cv2
import numpy as np

def process_image(image_path, resize_dim=(500, 500), canny_low=100, canny_high=200):
    img = cv2.imread(image_path)

    # 改变分辨率
    img_resized = cv2.resize(img, resize_dim)

    # 灰度处理
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # 轮廓检测
    edges = cv2.Canny(img_gray, canny_low, canny_high)

    return img_resized, img_gray, edges
