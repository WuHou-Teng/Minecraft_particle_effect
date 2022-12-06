import cv2 as cv
import numpy as np


class cvtool(object):
    """
    该函数来源于网上，回头自己要重新制作一份自己习惯的包装。
    """

    def __init__(self):
        pass

    def showImage(self, img, name="img", waitkeyMode=1, destroyMode=0, windowSizeMode=0):
        if img is None:
            print("In function showImage: the input image is None!")
            return
        cv.namedWindow(name, windowSizeMode)
        cv.imshow(name, img)
        cv.waitKey(waitkeyMode)
        if windowSizeMode != 0:
            cv.destroyWindow(name)

    def bgr2gray(self, colorImage):
        if colorImage.shape[-1] != 3:
            print("In function bgr2gray(): the input image's shape is:{}".format(colorImage.shape))
            return None
        grayImage = cv.cvtColor(colorImage, cv.COLOR_BGR2GRAY)
        return grayImage

    def canny(self, img, th1=80, th2=180):
        canny = cv.Canny(img, th1, th2)
        return canny

    def sobelx(self, img, ksize=3):
        sobelx = cv.Sobel(img, cv.CV_16SC1, 1, 0, ksize=ksize)
        return cv.convertScaleAbs(sobelx)

    def sobely(self, img, ksize=3):
        sobely = cv.Sobel(img, cv.CV_16SC1, 0, 1, ksize=ksize)
        return cv.convertScaleAbs(sobely)

    def sobelxy(self, img, ksize=3):
        sobelx = self.sobelx(img, ksize)
        sobely = self.sobely(img, ksize)
        return cv.addWeighted(sobelx, 0.5, sobely, 0.5, 1)

    def gaussianBlur(self, img, ksize=3, sigmax=1, sigmay=1):
        return cv.GaussianBlur(img, (ksize, ksize), sigmax, sigmay)

    def medianBlur(self, img, ksize=3):
        return cv.medianBlur(img, ksize)

    def averageBlur(self, img, ksize=3):
        return cv.blur(img, (ksize, ksize))

    # enum
    # cv::MorphShapes
    # {
    #     cv:: MORPH_RECT = 0,
    #     cv::MORPH_CROSS = 1,
    #     cv::MORPH_ELLIPSE = 2
    # }
    def erode(self, img, ksize=3, morphShape=2):
        return cv.erode(img, (ksize, ksize), 2)

    def dilate(self, img, ksize=3, morphShape=2):
        return cv.dilate(img, (ksize, ksize), 2)

    # enum
    # cv::MorphTypes
    # {
    #     cv::MORPH_ERODE = 0,
    #     cv::MORPH_DILATE = 1,
    #     cv::MORPH_OPEN = 2,
    #     cv::MORPH_CLOSE = 3,
    #     cv::MORPH_GRADIENT = 4,
    #     cv::MORPH_TOPHAT = 5,
    #     cv::MORPH_BLACKHAT = 6,
    #     cv::MORPH_HITMISS = 7
    # }
    def open(self, img, ksize=3, morphType=2, morphShape=2):
        return cv.morphologyEx(img, morphType, (ksize, ksize))

    def close(self, img, ksize=3, morphType=3, morphShape=2):
        return cv.morphologyEx(img, morphType, (ksize, ksize), morphShape)

    def gradient(self, img, ksize=3, morphShape=2):
        return cv.morphologyEx(img, cv.MORPH_GRADIENT, (ksize, ksize), morphShape)

    # enum
    # cv::ThresholdTypes
    # {
    #     cv:: THRESH_BINARY = 0,
    #     cv::THRESH_BINARY_INV = 1,
    #     cv::THRESH_TRUNC = 2,
    #     cv::THRESH_TOZERO = 3,
    #     cv::THRESH_TOZERO_INV = 4,
    #     cv::THRESH_MASK = 7,
    #     cv::THRESH_OTSU = 8,
    #     cv::THRESH_TRIANGLE = 16
    # }
    def threshold(self, img, th=120, maxVal=255, thresholdType=3):
        _, threshold = cv.threshold(img, th, 255, thresholdType)
        return threshold

    def otsu(self, img, thresholdType=cv.THRESH_TOZERO):
        if img.shape[-1] != 1:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, otsu = cv.threshold(img, 0, 255, thresholdType + cv.THRESH_OTSU)
        return otsu

    # enum cv::AdaptiveThresholdTypes
    # {
    #     cv:: ADAPTIVE_THRESH_MEAN_C = 0,
    #     cv::ADAPTIVE_THRESH_GAUSSIAN_C = 1
    # }
    def adaptiveThreshold(self, img, adaptiveThresholdType=cv.ADAPTIVE_THRESH_MEAN_C,
                          thresholdType=0, ksize=11, diff=5):
        if img.shape[-1] != 1:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        if ksize % 2 == 0:
            ksize += 1
        return cv.adaptiveThreshold(img, 255, adaptiveThresholdType, thresholdType, ksize, diff)

    def gamma(self, img, gamma=0.8):
        if img is None:
            print("in gamma: the image is None!")
            return img
        table = []
        for i in range(256):
            table.append(((i / 255.0) ** gamma) * 255)
        table = np.array(table).astype("uint8")
        dst = cv.LUT(img, table)
        return dst


if __name__ == "__main__":
    imgPath = "K:\\Ameng.png"
    img = cv.imread(imgPath)

    pro = cvtool()
    pro.showImage(img, "img", 0)

    gray = pro.bgr2gray(img)
    pro.showImage(gray, "gray", 0)

    canny = pro.canny(img)
    pro.showImage(canny, "canny", 0)

    sobelx = pro.sobelx(img)
    pro.showImage(sobelx, "sobelx", 0)

    sobely = pro.sobely(img)
    pro.showImage(sobely, "sobely", 0)

    sobelxy = pro.sobelxy(img)
    pro.showImage(sobelxy, "sobelxy", 0)

    gauss = pro.gaussianBlur(img, 9)
    pro.showImage(gauss, " gauss", 0)

    median = pro.medianBlur(img, 5)
    pro.showImage(median, "median")

    average = pro.averageBlur(img, 7)
    pro.showImage(average, "average", 0)

    erode = pro.erode(img, 9)
    pro.showImage(erode, "erode", 0)

    dilate = pro.dilate(img, 9)
    pro.showImage(dilate, "dilate", 0)

    open = pro.open(img, 11)
    pro.showImage(open, "open", 0)

    close = pro.close(img, 11)
    pro.showImage(close, "close", 0)

    gradient = pro.gradient(img, 5)
    pro.showImage(gradient, "gradient", 0)

    threshold = pro.threshold(img, 200)
    pro.showImage(threshold, "threshold", 0)

    otsu = pro.otsu(img)
    pro.showImage(otsu, "otsu", 0)

    adaptiveThreshold = pro.adaptiveThreshold(img, 0, 0)
    pro.showImage(adaptiveThreshold, "adaptiveThreshold", 0)

    gamma = pro.gamma(img, 1.5)
    pro.showImage(gamma, "gamma", 0)
