from util.Color_Range_Exception import ColorRangeException
from util.Filter_Amp_Ratio_Exception import FilterAmpRatioException
from Const.Convertor_consts import *


class ColorFilterAmp(object):
    """
    颜色滤镜。用于对特定通道的颜色进行过滤。
    """
    def __init__(self):
        self.red_range = []
        self.green_range = []
        self.blue_range = []
        # 过滤/增幅倍率。值在-1到255之间。
        # 如果值小于0，则对相应通道相应范围内的值进行过滤。
        # 如果值大于1，则对相应通道相应范围内的值进行过增幅。
        # 公式统一为 value * (1 + filter)
        self.filter_amp_ratio_red = FULL  # FULL = -1, 即，在滤镜内的颜色值会直接乘上 (1+FULL)==0 ，降为最低值。
        self.filter_amp_ratio_green = FULL
        self.filter_amp_ratio_blue = FULL

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

    def add_filter_red(self, red_start, red_end):
        """
        添加 red 通道滤镜。
        red_start, red_end ∈ (0.001, 1) 且 red_start <= red_end
        :param red_start: 开始值
        :param red_end: 结束值
        :return:
        """
        if red_start < 0.001 or red_start > 1:
            raise ColorRangeException(self.get_self_name() + ".set_filter_red()", "red_start = " + str(red_start))
        if red_end < 0.001 or red_end > 1:
            raise ColorRangeException(self.get_self_name() + ".set_filter_red()", "red_end = " + str(red_end))
        if red_start > red_end:
            raise ColorRangeException(self.get_self_name() + ".set_filter_red()", 
                                      "red_start = " + str(red_start) + " > " "red_end = " + str(red_end))
        self.red_range.append((red_start, red_end))
        
    def add_filter_green(self, green_start, green_end):
        """
        添加 green 通道滤镜。
        green_start, green_end ∈ (0, 1) 且 green_start <= green_end
        :param green_start: 开始值
        :param green_end: 结束值
        :return:
        """
        if green_start < 0 or green_start > 1:
            raise ColorRangeException(self.get_self_name() + ".set_filter_green()", "green_start = " + str(green_start))
        if green_end < 0 or green_end > 1:
            raise ColorRangeException(self.get_self_name() + ".set_filter_green()", "green_end = " + str(green_end))
        if green_start > green_end:
            raise ColorRangeException(self.get_self_name() + ".set_filter_green()", 
                                      "green_start = " + str(green_start) + " > " "green_end = " + str(green_end))
        self.green_range.append((green_start, green_end))
        
    def add_filter_blue(self, blue_start, blue_end):
        """
        添加 blue 通道滤镜。
        blue_start, blue_end ∈ (0, 1) 且 blue_start <= blue_end
        :param blue_start: 开始值
        :param blue_end: 结束值
        :return:
        """
        if blue_start < 0 or blue_start > 1:
            raise ColorRangeException(self.get_self_name() + ".set_filter_blue()", "blue_start = " + str(blue_start))
        if blue_end < 0 or blue_end > 1:
            raise ColorRangeException(self.get_self_name() + ".set_filter_blue()", "blue_end = " + str(blue_end))
        if blue_start > blue_end:
            raise ColorRangeException(self.get_self_name() + ".set_filter_blue()",
                                      "blue_start = " + str(blue_start) + " > " "blue_end = " + str(blue_end))
        self.blue_range.append((blue_start, blue_end))

    def set_filter_red(self, red_start, red_end):
        """
        设定 red 通道滤镜。
        red_start, red_end ∈ (0.001, 1) 且 red_start <= red_end
        :param red_start: 开始值
        :param red_end: 结束值
        :return:
        """
        self.clear_filter_red()
        self.add_filter_red(red_start, red_end)

    def set_filter_green(self, green_start, green_end):
        """
        设定 green 通道滤镜
        green_start, green_end ∈ (0, 1) 且 green_start <= green_end
        :param green_start: 开始值
        :param green_end: 结束值
        :return:
        """
        self.clear_filter_green()
        self.add_filter_green(green_start, green_end)

    def set_filter_blue(self, blue_start, blue_end):
        """
        设定 blue 通道滤镜
        blue_start, blue_end ∈ (0, 1) 且 blue_start <= blue_end
        :param blue_start: 开始值
        :param blue_end: 结束值
        :return:
        """
        self.clear_filter_blue()
        self.add_filter_blue(blue_start, blue_end)

    def clear_filter_red(self):
        self.red_range = []

    def clear_filter_green(self):
        self.green_range = []

    def clear_filter_blue(self):
        self.blue_range = []

    def clear_filter(self):
        self.red_range = []
        self.green_range = []
        self.blue_range = []

    def add_filter(self, red_start=0, red_end=0, green_start=0, green_end=0, blue_start=0, blue_end=0):
        """
        一次性添加三个通道的滤镜。
        :param red_start: red 通道开始值
        :param red_end: red 通道结束值
        :param green_start: green 通道开始值
        :param green_end: green 通道结束值
        :param blue_start: blue 通道开始值
        :param blue_end: blue 通道结束值
        :return:
        """
        self.add_filter_red(red_start, red_end)
        self.add_filter_green(green_start, green_end)
        self.add_filter_blue(blue_start, blue_end)

    def add_filter_equally(self, start, end):
        """
        为三个通道添加相同的滤镜
        :param start: 三个通道的开始值
        :param end: 三个通道的结束值
        :return:
        """
        self.add_filter(start, end, start, end, start, end)

    def set_filter(self, red_start=0, red_end=0, green_start=0, green_end=0, blue_start=0, blue_end=0):
        """
        一次性设定三个通道的滤镜。
        :param red_start: red 通道开始值
        :param red_end: red 通道结束值
        :param green_start: green 通道开始值
        :param green_end: green 通道结束值
        :param blue_start: blue 通道开始值
        :param blue_end: blue 通道结束值
        :return:
        """
        self.set_filter_red(red_start, red_end)
        self.set_filter_green(green_start, green_end)
        self.set_filter_blue(blue_start, blue_end)

    # 将处于忽略范围内的颜色通道设定为最小值。
    def filter_the_color(self, color_list):
        """
        检测要转换的粒子任意通道的颜色是否在忽略颜色范围内，如果是，则直接将该通道设定为最小值。
        :param color_list: [r, g, b], r, g, b ∈ [0,1]
        :return:
            color_list: 经过滤镜后的颜色。
        """

        for filters in self.red_range:
            if color_list[0] < filters[0] or color_list[0] > filters[1]:
                color_list[0] = color_list[0] * (1 + self.filter_amp_ratio_red)
                # 只有红色通道一定要保证数值最低不低于0.001
                if color_list < 0.001:
                    color_list[0] = 0.001
                if color_list[0] > 1:
                    color_list[0] = 1
        for filters in self.green_range:
            if color_list[1] < filters[0] or color_list[1] > filters[1]:
                color_list[1] = color_list[1] * (1 + self.filter_amp_ratio_green)
                if color_list[1] > 1:
                    color_list[1] = 1
        for filters in self.blue_range:
            if color_list[2] < filters[0] or color_list[2] > filters[1]:
                color_list[2] = color_list[2] * (1 + self.filter_amp_ratio_blue)
                if color_list[2] > 1:
                    color_list[2] = 1
        return color_list

    # 返回自己的类名称
    def get_self_name(self):
        return str(type(self)).split('.')[1][:-3]
