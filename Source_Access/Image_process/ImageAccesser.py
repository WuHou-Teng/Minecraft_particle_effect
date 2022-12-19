import os
from PIL import Image


class ImageAccesser(object):
    """
    待处理的图片，
    能够储存图片原数据，
    并且输出图片的各种变换，包括：
    灰度，二值，轮廓线
    resize（或许需要）
    切割
    旋转
    仿射变换
    """

    def __init__(self, image_address):
        # 创建一个图片的Access，必须提供有效的图片地址。
        self.image_address = image_address
        self.img = None
        self.load_image(self.image_address)

    def load_image(self, image_address):
        """
        加载图片到程序。将图片保存与 self.img
        :param image_address:
        :return:
        """
        # TODO 图片的读取方式，关乎于openCV和 pillow之间的矩阵转换。回头研究一下。
        # TODO 因为已有的转码方式式通过PIL来进行的，不确定PIL图片矩阵是否和openCV相同。

        self.image_address = image_address
        # 如果保存的图片内容不为空，则尝试关闭文件。
        if self.img is not None:
            try:
                self.img.close()
            except:
                self.img = None
        if not os.path.exists(self.image_address):
            self.image_address = None
            return "需要访问的图片不存在"
        try:
            self.img = Image.open(self.image_address)
            # self.img.close()
            return "图片读取成功，类型为" + os.path.basename(self.image_address).split(".")[-1]
        except:
            return "需要访问的图片格式不对，或者不存在"

    @property
    def i_width(self):

        return self.img.size[0] if self.img is not None else None

    @property
    def i_height(self):
        return self.img.size[1] if self.img is not None else None

    @property
    def binary(self):

        return self.img.convert("l")

    def get_sketch(self):
        """
        打算用python去调用那个网站的工具。
        :return:
        """
        pass
