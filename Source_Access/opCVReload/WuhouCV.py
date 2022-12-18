import cv2 as cv

# import imutils


class WuHouCV(object):
    """
    对于部分常用函数和常用常熟的二次包装
    """

    def __init__(self):
        pass

    # read image
    IMREAD_UNCHANGED = -1  # 返回加载的图像原样(带alpha通道，否则它会被裁剪)。忽略EXIF定向。
    IMREAD_GRAYSCALE = 0  # 始终将图像转换为单通道灰度图像(编解码器内部转换)。
    IMREAD_COLOR = 1  # 总是将图像转换为3通道BGR彩色图像。
    IMREAD_ANYDEPTH = 2  # 当输入有相应深度时返回16位/32位图像，否则将其转换为8位图像。
    IMREAD_ANYCOLOR = 4  # 则以任何可能的颜色格式读取图像。
    IMREAD_LOAD_GDAL = 8  # 使用gdal驱动程序加载图像。
    IMREAD_REDUCED_GRAYSCALE_2 = 16  # 总是将图像转换为单通道灰度图像，图像大小减小1/2。
    IMREAD_REDUCED_COLOR_2 = 17  # 总是将图像转换为3通道BGR彩色图像，图像大小减小1/2。
    IMREAD_REDUCED_GRAYSCALE_4 = 32  # 始终将图像转换为单通道灰度图像，图像大小减小1/4。
    IMREAD_REDUCED_COLOR_4 = 33  # 总是将图像转换为3通道BGR彩色图像，图像大小减小1/4。
    IMREAD_REDUCED_GRAYSCALE_8 = 64  # 总是将图像转换为单通道灰度图像，图像大小减小1/8。
    IMREAD_REDUCED_COLOR_8 = 65  # 总是将图像转换为3通道BGR彩色图像，图像大小减小1/8。
    IMREAD_IGNORE_ORIENTATION = 128  # 不要根据EXIF的方向标志旋转图像。

    def imread(self, file_name, flag=IMREAD_UNCHANGED):
        """
        【读取图片】
        课接受的文件类型：
            .jpeg .jpg .jpe .jp2
            .png
            .bmp .dib
            .pbm .ppm .pgm .pxm .pnm
            .tiff .tif
        :param file_name:图片名称/地址
        :param flag:读取方式，默认为 BGR，且带有 alpha 通道
        :return:
        """
        cv.imread(file_name, flag)

    # 阈值
    THRESH_BINARY = 0  # 大于 thresh 为 max，否则为 0
    THRESH_BINARY_INV = 1  # 大于 thresh 为 0，否则为 max
    THRESH_TRUNC = 2  # 大于 thresh 为thresh,否则为 0
    THRESH_TOZERO = 3  # 大于 thresh 不变，否则为 0
    THRESH_TOZERO_INV = 4  # 大于 thresh 为 0,否则不变

    THRESH_MASK = 7
    THRESH_OTSU = 8  # flag, use Otsu algorithm to choose the optimal threshold value
    THRESH_TRIANGLE = 16  # flag, use Triangle algorithm to choose the optimal threshold value

    ADAPTIVE_THRESH_MEAN_C = 0  # 阈值是每个像素邻域区域的均值减去常量C
    ADAPTIVE_THRESH_GAUSSIAN_C = 1  # 阈值是每个像素相邻域区域的高斯加权和减去常量C

    #
    # void cv::adaptiveThreshold ( InputArray src,      # Source 8-bit single-channel image.
    #                              OutputArray 	dst,    # Destination image of the same size and the same type as src.
    #                              double 	maxValue,   # Non-zero value assigned to the pixels for which the
    #                                                     condition is satisfied
    #                              int 	adaptiveMethod, # Adaptive thresholding algorithm to use,
    #                                                     see AdaptiveThresholdTypes.
    #                                                     The BORDER_REPLICATE | BORDER_ISOLATED is used to
    #                                                     process boundaries.
    #                              int 	thresholdType,  # Thresholding type that must be either
    #                                                     THRESH_BINARY or THRESH_BINARY_INV, see ThresholdTypes.
    #                              int 	blockSize,      # Size of a pixel neighborhood that is used to
    #                                                     calculate a threshold value for the pixel: 3, 5, 7, and so on.
    #                              double 	C           # Constant subtracted from the mean or weighted mean
    #                                                     (see the details below).
    #                                                     Normally, it is positive but may be zero or negative as well.
    # )
    # dst = cv.adaptiveThreshold( src, maxValue, adaptiveMethod, thresholdType, blockSize, C[, dst]	)
    def adaptiveThreshold(self, src_grey_img, max_value, adaptive_method, threshold_type, block_size=3, c=2):
        """
        【自适应阈值处理】
        该函数根据公式将灰度图像转换为二值图像.
        该函数可以对图像进行原位处理。
        :param src_grey_img:8位单通道图像。也就是255灰度图像
        :param max_value:非零值赋给满足条件的像素
        :param adaptive_method:使用的自适应阈值算法，参见 AdaptiveThresholdTypes。 BORDER_REPLICATE|BORDER_ISOLATED命令用于处理边界。
        :param threshold_type:阈值类型必须是 THRESH_BINARY或 THRESH_BINARY_INV，
        :param block_size:像素邻域的大小，用于计算像素的阈值:3、5、7等等。
        :param c:常数减去平均值或加权平均值(详见下文)。通常，它是正的，但也可能是零或负的。
        :return:
            binary_img: 二值化后的图像
        """
        # 如果输入不是灰度图，则先转换为灰度图，再继续
        if src_grey_img.shape[-1] != 1:
            src_grey_img = cv.cvtColor(src_grey_img, cv.COLOR_BGR2GRAY)
        ret, binary_img = cv.adaptiveThreshold(src_grey_img, max_value, adaptive_method, threshold_type, block_size, c)
        return ret, binary_img

    # double cv::threshold ( InputArray 	src,  # input array (multiple-channel, 8-bit or 32-bit floating point).
    #                        OutputArray 	dst,  # output array of the same size and type and
    #                                               the same number of channels as src.
    #                        double 	 thresh,  # threshold value.
    #                        double 	 maxval,  # maximum value to use with the THRESH_BINARY and
    #                                               THRESH_BINARY_INV thresholding types.
    #                        int 	       type   # thresholding type，see the consts
    # )
    # retval, dst = cv.threshold( src, thresh, maxval, type[, dst] )
    def threshold(self, src_grey_img, thresh_val, max_val, thresh_type):
        """
        【阈值处理】
        对每个数组元素应用固定级别的阈值。
            该函数对多通道阵列应用固定级阈值分割。
            该函数通常用于从灰度图像中获得双层(二值)图像(compare也可用于此目的)或用于去除噪声，即过滤出值过小或过大的像素。
            该函数支持几种类型的阈值划分。它们是由类型参数确定的。
        :param src_grey_img:8位单通道图像。也就是255灰度图像
        :param thresh_val:阈值
        :param max_val:与 THRESH_BINARY和 THRESH_BINARY_INV阈值类型一起使用的最大值。
        :param thresh_type: 阈值类型
        :return:
            binary_img: 二值化后的图像
        """
        # 如果输入不是灰度图，则先转换为灰度图，再继续
        if src_grey_img.shape[-1] != 1:
            src_grey_img = cv.cvtColor(src_grey_img, cv.COLOR_BGR2GRAY)
        ret, binary_img = cv.threshold(src_grey_img, thresh_val, max_val, thresh_type)
        return ret, binary_img

    # 查找边界，cv.findContours
    # 第二个参数，mode
    RETR_EXTERNAL = 0  # 仅仅检测外圈轮廓
    RETR_LIST = 1  # 检测所有轮廓，但是没有层级关系
    RETR_CCOMP = 2  # 仅仅两层包含关系，即只有外层和内层，假设有夹层，那么夹层也算外层，只要某个轮廓还包含有轮廓，都算外部轮廓
    RETR_TREE = 3  # 检测所有的轮廓，并建议非常完整的层级关系
    RETR_FLOODFILL = 4  # 无描述

    # 第三个参数，method
    CHAIN_APPROX_NONE = 1  # 相邻的轮廓点坐标只相差一个像素，所以是连续轮廓点
    CHAIN_APPROX_SIMPLE = 2  # 横、竖、对角线段只保存断点数据，比如矩形就只保存四个顶点。

    # void cv::findContours	( InputArray            image,
    #                         OutputArrayOfArrays   contours,
    #                         OutputArray           hierarchy,
    #                         int 	                mode,
    #                         int 	                method,
    #                         Point 	            offset = Point()
    #                         )
    # Parameters see:
    # https://docs.opencv.org/4.5.0/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e0

    # Python
    # contours, hierarchy	=	cv.findContours(	image, mode, method[, contours[, hierarchy[, offset]]]	)
    def findContours(self, image, mode, method):
        """
        寻找图片中的轮廓线
        :param image:待处理图像
        :param mode:检测轮廓的层级关系排列规则
        :param method:轮廓点的存储方式：
        :return:
            contours:检测到的轮廓，每个轮廓是由一些点构成的向量组成
            hierarchy:记录轮廓之间的关系，四个维度分别代表：同级后一个轮廓的序号、同级上一个轮廓的序号、第一个孩子序号，父亲序号
        """
        contours, hierarchy = cv.findContours(image, mode, method)
        return contours, hierarchy

    # 绘制轮廓
    FILLED = -1  # 请注意当thickness=FILLED时，该函数被设计为正确处理带有孔的连接组件，即使没有提供层次结构数据。
    # 这是通过使用奇偶法则分析所有的轮廓来完成的。如果你有一个单独检索的轮廓的联合集合，这可能会给出不正确的结果。
    # 为了解决这个问题，您需要为每个等高线子组分别调用drawContours，或者使用contourldx参数遍历集合。
    LINE_4 = 4      # 4-connected line (4链接线，十字连接？)
    LINE_8 = 8      # 8-connected line (8链接线，米子连接？)
    LINE_AA = 16    # antialiased line (抗锯齿连接）

    # void cv::drawContours	( InputOutputArray 	image,
    #                         InputArrayOfArrays 	contours,
    #                         int 	contourIdx,
    #                         const Scalar & 	color,
    #                         int 	thickness = 1,
    #                         int 	lineType = LINE_8,
    #                         InputArray 	hierarchy = noArray(),
    #                         int 	maxLevel = INT_MAX,
    #                         Point 	offset = Point()
    # )
    # Parameters: see:
    # https://docs.opencv.org/4.5.0/d6/d6e/group__imgproc__draw.html#ga746c0625f1781f1ffc9056259103edbc
    # Python:
    # image	=	cv.drawContours( image, contours, contourIdx, color
    #                           [, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]	)
    def drawContours(self, image, contours, contourIdx, color=(255, 255, 255), thickness=5, lineType=LINE_AA):
        """
        绘制给定的轮廓线。
        :param image:要绘制的图，注意，返回的图和输入的图是同一张，所以，只要轮廓的话，考虑新键一个新的空数组。
        :param contours:是list类型的数组，里面存储了很多array数组去代表各个轮廓
        :param contourIdx:从上面的轮廓list中取出哪一个画出来，-1代表全部
        :param color:线条颜色
        :param thickness:线条粗细，-1代表填充式画轮廓，整个轮廓内部被指定颜色填充
        :param lineType: 线条类型，虚线，实线等。
        :return:
            image:经过绘制的图片，注意，这里依旧是BGR模式，显示最好显示为 RGB => plt.imshow(img[...,::-1])
        """
        image = cv.drawContours(image, contours, contourIdx, color, thickness, lineType)
        return image
