import cv2
import numpy as np


def adjust_gray_levels(image, gray_levels):
    # 计算每个新灰度级的范围大小
    scale_factor = 256 // gray_levels

    # 调整图像的灰度级别
    adjusted_image = (image // scale_factor) * scale_factor

    return adjusted_image


def adjust_resolution(image, resolution):
    height, width = image.shape[:2]
    return cv2.resize(image, (resolution * width // 100, resolution * height // 100))


def detect_edges(image, metric):
    if metric == 'l1':
        return cv2.Canny(image, 100, 200)
    else:
        return cv2.Laplacian(image, cv2.CV_64F)


def process_image(image_path, gray_levels=None, resolution=None, distance_metric=None):
    # 读取原图像
    original_image = cv2.imread(image_path)

    # 创建图像的副本
    resolution_image = original_image.copy()
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    edges_image = original_image.copy()

    # 调整灰度级
    if gray_levels is not None:
        gray_image = adjust_gray_levels(gray_image, gray_levels)

    # 调整分辨率
    if resolution is not None:
        resolution_image = adjust_resolution(original_image, resolution)

    # 绘制轮廓线
    if distance_metric is not None:
        edges_image = detect_edges(original_image, distance_metric)

    return resolution_image, gray_image, edges_image
