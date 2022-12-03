import os
from PIL import Image
from Const.Other_const import *
from Motion_diffusion import MotionDiffusion


class ImageSampling(object):

    def __init__(self, image='', height_limit=Height_MAX, width_limit=Width_MAX, direction=West_East, align=LEFT_DOWN):
        # 图片本身
        self.image_address = image
        self.img = []
        self.img_width = 0
        self.img_height = 0

        # 图片最大大小。默认为100x100
        self.height_limit = height_limit
        self.width_limit = width_limit
        # 是否固定长宽比
        self.fixed_aspect_ratio = True
        # 图片缩放，实际呈现的图片大小，本质是调节粒子间距。
        self.height_scale, self.width_scale = 1, 1
        # 图片缩放是根据最大大小自动计算的。但也可以自己定义确定的缩放大小。
        self.force_scale = False
        # 下采样率, 2就是2x2的像素采集一个像素数据。
        # 下采样不应改变图片的整体大小，只改变采样点的稀疏程度
        self.down_sample = 1
        # 图片对齐方式，也就是规定原点(0,0)位置，这个值会
        # 左上，左中，左下，中上，正中，中下，右上，右中，右下，
        self.align = align
        # 坐标平移, 根据align计算，不接受直接改变。
        self._height_shift, self._width_shift = 0, 0
        # 粒子图片呈现方向，
        # West_East   即为东西平面，也就是面向x方向显示全图
        # North_South 即为南北平面，也就是面向z方向显示全图
        # Lay_Down    即为水平面，也就是将图片水平呈现
        self.direction = direction

        # TODO 关于粒子运动，准备在这里保留粒子运动的设定
        # motion and diffusion
        self.motion_diffusion = MotionDiffusion()

    # TODO transfer 函数待完成。
    def transfer(self):
        if not os.path.exists(self.image_address):
            return "需要访问的图片不存在"
        try:
            self.img = Image.open(self.image_address)
            self.img_width = self.img.size[0]
            self.img_height = self.img.size[1]

        except:
            # TODO 不确定这里的打印异常能否正常运行
            # print(str(Exception))
            return "需要访问的图片格式不对，或者不存在"

    def set_img_to_load(self, img_address):
        self.image_address = img_address

    def set_max_height(self, height):
        self.height_limit = height

    def set_max_width(self, width):
        self.width_limit = width

    def lock_aspect_ratio(self):
        self.fixed_aspect_ratio = True

    def unlock_aspect_ratio(self):
        self.fixed_aspect_ratio = False

    def scale_auto(self):
        self.force_scale = False

    def scale_diy(self):
        self.force_scale = True

    def set_direction(self, direction):
        self.direction = direction

    def set_align(self, align):
        """
        从左上，左中，左下，中上，正中，中下，右上，右中，右下 中选一个
        :return:
        """
        if align in [LEFT_DOWN, LEFT_MID, LEFT_UP,
                     RIGHT_DOWN, RIGHT_UP, RIGHT_MID,
                     MID_DOWN, MID_UP, MIDDLE]:
            self.align = align

    def set_down_sample(self, down_sample):
        self.down_sample = down_sample

    # def load_image(self):
    #     try:
    #         return = Image.open(self.image_address)
    #     except FileNotFoundError:
    #         # TODO 不确定这里的异常抛出怎么写更好
    #         raise()

    def calculate_scale(self):
        height_scale = self.height_limit / self.img_height
        width_scale = self.width_limit / self.img_width
        if self.fixed_aspect_ratio:
            scale_ratio = height_scale if height_scale < width_scale else width_scale
            self.height_scale = self.width_scale = scale_ratio

        else:
            self.height_scale = height_scale
            self.width_scale = width_scale

    def calculate_shift(self):
        if self.align == LEFT_DOWN:

            self._width_shift = 0
            self._height_shift = round(self.img_height / self.height_scale)

        elif self.align == LEFT_MID:

            self._width_shift = 0
            self._height_shift = round(self.img_height / self.height_scale) / 2

        elif self.align == LEFT_UP:

            self._width_shift = 0
            self._height_shift = 0

        elif self.align == MID_DOWN:

            self._width_shift = round(self.img_width / self.width_scale) / 2
            self._height_shift = round(self.img_height / self.height_scale)

        elif self.align == MIDDLE:

            self._width_shift = round(self.img_width / self.width_scale) / 2
            self._height_shift = round(self.img_height / self.height_scale) / 2

        elif self.align == MID_UP:

            self._width_shift = round(self.img_width / self.width_scale) / 2
            self._height_shift = 0

        elif self.align == RIGHT_DOWN:

            self._width_shift = round(self.img_width / self.width_scale)
            self._height_shift = round(self.img_height / self.height_scale)

        elif self.align == RIGHT_MID:

            self._width_shift = round(self.img_width / self.width_scale)
            self._height_shift = round(self.img_height / self.height_scale) / 2

        elif self.align == RIGHT_UP:

            self._width_shift = round(self.img_width / self.width_scale)
            self._height_shift = 0
