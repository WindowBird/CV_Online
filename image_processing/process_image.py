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


def binarize_image(image):
    # 确保图像是灰度图像
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    threshold = 127
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary_image


# 4连通
def four_connected(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


# 8连通
def eight_connected(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
            (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1)]


def detect_edges(image, metric):
    if metric == 'l1':
        return cv2.Canny(image, 100, 200)
    elif metric == 'l2':
        return cv2.Laplacian(image, cv2.CV_64F)
    elif metric in ['内部点8连通，轮廓点4连通', '内部点4连通，轮廓点8连通']:
        binary_image = binarize_image(image)
        zero_count = np.sum(binary_image == 0)
        non_zero_count = np.sum(binary_image == 255)

        edge_value = 255 if zero_count > non_zero_count else 0
        inner_value = 0 if edge_value == 255 else 255

        edges = np.zeros_like(binary_image)
        height, width = binary_image.shape[:2]

        for x in range(1, height - 1):
            for y in range(1, width - 1):
                if binary_image[x, y] == inner_value:
                    continue

                edge_neighbors = four_connected(x, y) if metric == 'l3' else eight_connected(x, y)
                is_edge = any(binary_image[i, j] == edge_value for i, j in edge_neighbors)

                if is_edge:
                    edges[x, y] = edge_value

        return edges


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
