import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt


WHITE = 255
BLACK = 0

# 先将白色以外的像素变成全黑，然后再用sd将内部轮廓勾勒出来。

class OutlineProcess(object):
    """
    用于尝试获取完整的图像轮廓线。
    """
    def __init__(self, image_name, address):
        self.image_name = image_name
        self.address = address
        self.full_img_addr = os.path.join(self.address, self.image_name)
        self.src_img = cv.imread(self.full_img_addr)
        # 提前将matplot的图片显示分辨率拉高。
        plt.rcParams['figure.dpi'] = 300

    def stand_div_rgb(self, r, g, b):
        """
        计算输入的三个通道的标准差。如果标准差大，则代表该粒子的三个通道颜色差距较大。饱和度较高。
        :param r: 红色通道数值 (0~255)
        :param g: 绿色通道数值 (0~255)
        :param b: 蓝色通道数值 (0~255)
        :return:
        """
        average = int(r) + int(g) + int(b)
        sd = ((int(r) - average) ** 2 + (int(g) - average) ** 2 + (int(b) - average) ** 2) ** 0.5
        return sd

    def sd_filter(self, sd_threshold, wb=WHITE):
        """
        标准差滤镜，将颜色均衡度度高于阈值的像素挑出来
        :param sd_threshold:
        :param wb: 目标是，可以是BLACK(0) 或者是WHITE(255)
        :return:
        """
        sd_filtered_img = self.src_img
        for each_rows in sd_filtered_img:
            for pixels in each_rows:
                if self.stand_div_rgb(pixels[0], pixels[1], pixels[2]) > sd_threshold:
                    pixels[0] = wb
                    pixels[1] = wb
                    pixels[2] = wb

    def show_img(self, img):
        """
        将经过处理的图片还原回原来的8位无符号整形，然后通过matplot显示。
        :param img: 经过处理的图片。
        """
        plt.imshow(cv.cvtColor(img.astype(np.uint8), cv.COLOR_BGR2RGB))
        plt.show()

    def add_outline(self, img):
        dst = cv.cvtColor(img.astype(np.uint8), cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(dst, 127, 255, cv.THRESH_BINARY)




