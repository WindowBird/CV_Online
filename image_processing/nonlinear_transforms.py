import cv2
import numpy as np


def log_transform(image):
    # 检查输入图像的通道数
    channels = cv2.split(image)

    # 对每个通道进行 log 变换
    enhanced_channels = []
    for channel in channels:
        if channel.dtype != 'float32':
            channel = channel.astype('float32')
        c = 255 / np.log(1 + np.max(channel))
        enhanced_channel = c * (np.log(channel + 1))
        enhanced_channel = enhanced_channel.astype('uint8')
        enhanced_channels.append(cv2.convertScaleAbs(enhanced_channel))

    # 合并通道
    enhanced_img = cv2.merge(enhanced_channels)

    return enhanced_img

