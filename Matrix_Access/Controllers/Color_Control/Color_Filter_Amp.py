from Matrix_Access.Controllers.Color_Control.Color_Controller import ColorController
from Matrix_Access.Particles import MCParticle
from util.Filter_Amp_Ratio_Exception import FilterAmpRatioException
from Matrix_Access.Controllers.Color_Control.Color_Controller_Const import *


class ColorFilterAmp(ColorController):
    """
    颜色滤镜。用于对特定通道的颜色进行过滤 或者 增强
    """
    def __init__(self, index_name, red_range=None, green_range=None, blue_range=None,
                 filter_amp_ratio_red=FULL, filter_amp_ratio_green=FULL, filter_amp_ratio_blue=FULL):

        # self.red_range = []
        # self.green_range = []
        # self.blue_range = []
        # 过滤/增幅倍率。值在-1到255之间。
        # 如果值小于0，则对相应通道相应范围内的值进行过滤。
        # 如果值大于1，则对相应通道相应范围内的值进行过增幅。
        # 公式统一为 value * (1 + filter)
        self.filter_amp_ratio_red = filter_amp_ratio_red  # FULL = -1, 即，在滤镜内的颜色值会直接乘上 (1+FULL)==0 ，降为最低值。
        self.filter_amp_ratio_green = filter_amp_ratio_green
        self.filter_amp_ratio_blue = filter_amp_ratio_blue
        super(ColorFilterAmp, self).__init__(index_name, red_range, green_range, blue_range)

    def set_filter_amp_ratio_red(self, ratio):
        """
        设定过滤的比例。1则为完全不过滤，0则为完全过滤。
        :param ratio: 过滤比例 ∈ [-1,255]
        :return:
        """
        if ratio < -1 or ratio > 255:
            raise FilterAmpRatioException(self.get_self_name() + "set_filter_amp_ratio_red", "ratio = " + str(ratio))
        self.filter_amp_ratio_red = ratio

    def set_filter_amp_ratio_green(self, ratio):
        """
        设定过滤的比例。1则为完全不过滤，0则为完全过滤。
        :param ratio: 过滤比例 ∈ [-1,255]
        :return:
        """
        if ratio < -1 or ratio > 255:
            raise FilterAmpRatioException(self.get_self_name() + "set_filter_amp_ratio_green", "ratio = " + str(ratio))
        self.filter_amp_ratio_green = ratio

    def set_filter_amp_ratio_blue(self, ratio):
        """
        设定过滤的比例。1则为完全不过滤，0则为完全过滤。
        :param ratio: 过滤比例 ∈ [-1,255]
        :return:
        """
        if ratio < -1 or ratio > 255:
            raise FilterAmpRatioException(self.get_self_name() + "set_filter_amp_ratio_blue", "ratio = " + str(ratio))
        self.filter_amp_ratio_blue = ratio

    # 这里之前是写有原本关于range设定的类，现全部转移到父类，ColorChannels里面

    # 为处于范围内的颜色通道添加滤镜
    def filter_amp_the_color(self, color_list):
        """
        检测要转换的粒子任意通道的颜色是否在相应范围内，如果是，则为该通道的颜色添加滤镜
        :param color_list: [r, g, b], r, g, b ∈ [0,1]
        :return:
            color_list: 经过滤镜后的颜色。
        """

        # 红色通道
        if self.red_range_include(color_list[0]):
            color_list[0] = color_list[0] * (1 + self.filter_amp_ratio_red)
            # 只有红色通道一定要保证数值最低不低于0.001
            if color_list < 0.001:
                color_list[0] = 0.001
            if color_list[0] > 1:
                color_list[0] = 1
        # for ranges in self.red_range:
        #     if color_list[0] < ranges[0] or color_list[0] > ranges[1]:
        #         color_list[0] = color_list[0] * (1 + self.filter_amp_ratio_red)
        #         # 只有红色通道一定要保证数值最低不低于0.001
        #         if color_list < 0.001:
        #             color_list[0] = 0.001
        #         if color_list[0] > 1:
        #             color_list[0] = 1

        # 绿色通道
        if self.green_range_include(color_list[1]):
            color_list[1] = color_list[1] * (1 + self.filter_amp_ratio_green)
            if color_list[1] > 1:
                color_list[1] = 1
        # for ranges in self.green_range:
        #     if color_list[1] < ranges[0] or color_list[1] > ranges[1]:
        #         color_list[1] = color_list[1] * (1 + self.filter_amp_ratio_green)
        #         if color_list[1] > 1:
        #             color_list[1] = 1

        # 蓝色通道
        if self.blue_range_include(color_list[2]):
            color_list[2] = color_list[2] * (1 + self.filter_amp_ratio_blue)
            if color_list[2] > 1:
                color_list[2] = 1
        # for ranges in self.blue_range:
        #     if color_list[2] < ranges[0] or color_list[2] > ranges[1]:
        #         color_list[2] = color_list[2] * (1 + self.filter_amp_ratio_blue)
        #         if color_list[2] > 1:
        #             color_list[2] = 1
        return color_list

    def process(self, particle) -> MCParticle:
        """
        继承自 ControllerBase，输入完整粒子信息后，对其修改，并返回。
        :param particle: MCParticle 类，包含所有可直接调用的数字参数。
        :return:
            particle: 经过处理后的粒子数据。
        """
        assert type(particle) is MCParticle
        color_list = self.filter_amp_the_color([particle.r, particle.g, particle.b])
        particle.r = color_list[0]
        particle.g = color_list[1]
        particle.b = color_list[2]
        return particle

    def process_matrix(self, matrix_accesser):
        pass


class ColorTransFilterAmp(ColorFilterAmp):
    """
    该类和上面基本一致，唯一的区别是，该类对转变颜色作处理。
    """
    def __init__(self, index_name, red_range=None, green_range=None, blue_range=None,
                 filter_amp_ratio_red=FULL, filter_amp_ratio_green=FULL, filter_amp_ratio_blue=FULL):

        super(ColorFilterAmp).__init__(index_name, red_range, green_range, blue_range,
                                       filter_amp_ratio_red,
                                       filter_amp_ratio_green,
                                       filter_amp_ratio_blue)

    def process(self, particle):
        assert type(particle) is MCParticle
        color_list = self.filter_amp_the_color([particle.rt, particle.gt, particle.bt])
        particle.rt = color_list[0]
        particle.gt = color_list[1]
        particle.bt = color_list[2]
        return particle

