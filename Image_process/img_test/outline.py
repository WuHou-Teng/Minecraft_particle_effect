import cv2 as cv
import os
from matplotlib import pyplot as plt

image_name = "try3.jpg"
address = "E:\work\Interesting_things\python_test\Mc_Effect\pics"
# img = cv.imread(os.path.join(address, image_name), 0)

# laplacian = cv.Laplacian(img, cv.CV_64F)
# sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=5)
# sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=5)
# plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray')
# plt.title('Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 2), plt.imshow(laplacian, cmap='gray')
# plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 3), plt.imshow(sobelx, cmap='gray')
# plt.title('Sobel_X'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 4), plt.imshow(sobely, cmap='gray')
# plt.title('Sobel_Y'), plt.xticks([]), plt.yticks([])
# plt.show()

# 读取原图
Src = cv.imread(os.path.join(address, image_name))
print(Src.shape)
# 重新定义图片大小
# Src = cv.resize(Src, (600, 500))
# 显示图片， 标题为“Src”
cv.imshow("Src", Src)
# 转为灰度图
dst = cv.cvtColor(Src, cv.COLOR_BGR2GRAY)
# cv.imshow("input", Src)
# 阈值处理(⼆值处理）
# 参数1：src——输⼊图像
# 参数2：thresh——阈值
# 参数3：maxval——由参数4决定
# 参数4：type——阈值处理模式选择
#   阈值处理模式分为一下几种：
#   THRESH_BINARY = 0     大于 thresh 为 max，否则为 0
#   THRESH_BINARY_INV = 1 大于 thresh 为 0，否则为 max
#   THRESH_TRUNC = 2      大于 thresh 为thresh,否则为 0
#   THRESH TOZERO = 3     大于 thresh 不变，否则为 0
#   THRESH_TOZERO_INV = 4 大于 thresh 为 0,否则不变
ret, thresh = cv.threshold(dst, 127, 255, cv.THRESH_BINARY)
# cv.imshow("thresh", thresh)
# 获取轮廓信息
# 画出轮廓——drawContours函数原型：drawContours(image, contours, contourldx, color, thickness)
# 参数1：image：需要画出轮廓的图像
# 参数2：contours：输⼊的所有轮廓（每个轮廓以点集的⽅式存储）
#   cv.RETR_EXTERNAL   表示只检测外轮廓
#   cv.RETR_LIST       检测的轮廓不建立等级关系
#   cv.RETR_CCOMP      建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界。
#   cv.RETR_TREE       建立一个等级数结构的轮廓
# 参数3：contourldx：画第⼏个轮廓，常⽤-1，画出全部轮廓
#   cv.CHAIN_APPROX_NONE   储存所有的轮廓点
#   cv.CHAIN_APPROX_SIMPLE 压缩水平方向，垂直方向， 对角线方向的元素，只保留该方向的终点坐标。
# 参数4：color：画出轮廓线条的颜⾊
# 参数5：thickness：画出轮廓线条的粗细
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

result = cv.drawContours(Src, contours, -1, (0, 0, 255), 2)
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()
