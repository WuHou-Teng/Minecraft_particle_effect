import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

address = "C:\\Wuhou\\study\\python_test\\Mc_Effect\\pics"

INPUT_IMAGE = "yooomeng.jpg"
OUTPUT_IMAGE = "yooomeng_outling.png"
SCALE = 1
LIMITER = 240


def show_img(img):
    """
    将经过处理的图片还原回原来的8位无符号整形，然后通过matplot显示。
    :param img: 经过处理的图片。
    """
    plt.imshow(cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB))
    plt.show()


def function_2():
    image = cv2.imread(os.path.join(address, INPUT_IMAGE))
    image = cv2.resize(image, fx=SCALE, fy=SCALE, dsize=None, dst=None)
    image = cv2.GaussianBlur(image, (3, 3), 1)

    output = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2)
    show_img(output)


def main():
    image = cv2.imread(os.path.join(address, INPUT_IMAGE))

    image = cv2.resize(image, fx=SCALE, fy=SCALE, dsize=None, dst=None)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # 灰度转化

    h, w = gray.shape[:2]  # 获取灰度图的长宽
    m = np.reshape(gray, [1, w * h])    # 将图片长宽替换？
    mean = m.sum() / (w * h)  # 图像平均灰度值

    # 将图片高斯模糊
    blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0, sigmaY=0)
    show_img(blur)

    # 让原灰度图和模糊化的灰度图相除，图片轮廓会因为模糊化有较大的改变，而大色块则维持原样。因此，相除后数值较大的区域为轮廓。
    output = cv2.divide(gray, blur, scale=255)
    show_img(output)

    # 二值过滤
    for pixel in output:
        for i in range(0, pixel.size):
            if mean < pixel[i] < LIMITER:
                pixel[i] = 0
            else:
                pixel[i] = 255

    show_img(output)
    # cv2.imwrite(os.path.join(address, OUTPUT_IMAGE), output)


if __name__ == "__main__":
    # main()
    function_2()
