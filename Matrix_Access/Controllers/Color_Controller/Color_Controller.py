from util.Color_Range_Exception import ColorRangeException
from Matrix_Access.Controllers.Controller_Interface import ControllerBase


class ColorController(ControllerBase):

    def __init__(self):
        super(ColorController, self).__init__()
        self.red_range = []
        self.green_range = []
        self.blue_range = []

        # 翻转已添加的range
        self.flip = False

    def flip_to_blacklist(self):
        """
        切换到黑名单模式
        :return:
        """
        self.flip = True

    def flip_to_whitelist(self):
        """
        切换到白名单模式
        :return:
        """
        self.flip = False

    def add_range_red(self, red_start, red_end):
        """
        添加 red 通道区域。
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

    def add_range_green(self, green_start, green_end):
        """
        添加 green 通道区域。
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

    def add_range_blue(self, blue_start, blue_end):
        """
        添加 blue 通道区域。
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

    def set_range_red(self, red_start, red_end):
        """
        设定 red 通道区域。
        red_start, red_end ∈ (0.001, 1) 且 red_start <= red_end
        :param red_start: 开始值
        :param red_end: 结束值
        :return:
        """
        self.clear_range_red()
        self.add_range_red(red_start, red_end)

    def set_range_green(self, green_start, green_end):
        """
        设定 green 通道区域。
        green_start, green_end ∈ (0, 1) 且 green_start <= green_end
        :param green_start: 开始值
        :param green_end: 结束值
        :return:
        """
        self.clear_range_green()
        self.add_range_green(green_start, green_end)

    def set_range_blue(self, blue_start, blue_end):
        """
        设定 blue 通道区域。
        blue_start, blue_end ∈ (0, 1) 且 blue_start <= blue_end
        :param blue_start: 开始值
        :param blue_end: 结束值
        :return:
        """
        self.clear_range_blue()
        self.add_range_blue(blue_start, blue_end)

    def clear_range_red(self):
        self.red_range = []

    def clear_range_green(self):
        self.green_range = []

    def clear_range_blue(self):
        self.blue_range = []

    def clear_range(self):
        self.red_range = []
        self.green_range = []
        self.blue_range = []

    def add_range(self, red_start=0, red_end=0, green_start=0, green_end=0, blue_start=0, blue_end=0):
        """
        一次性添加三个通道的区域。
        :param red_start: red 通道开始值
        :param red_end: red 通道结束值
        :param green_start: green 通道开始值
        :param green_end: green 通道结束值
        :param blue_start: blue 通道开始值
        :param blue_end: blue 通道结束值
        :return:
        """
        self.add_range_red(red_start, red_end)
        self.add_range_green(green_start, green_end)
        self.add_range_blue(blue_start, blue_end)

    def add_range_equally(self, start, end):
        """
        为三个通道添加相同的区域。
        :param start: 三个通道的开始值
        :param end: 三个通道的结束值
        :return:
        """
        self.add_range(start, end, start, end, start, end)

    def set_range(self, red_start=0, red_end=0, green_start=0, green_end=0, blue_start=0, blue_end=0):
        """
        一次性设定三个通道的区域。
        :param red_start: red 通道开始值
        :param red_end: red 通道结束值
        :param green_start: green 通道开始值
        :param green_end: green 通道结束值
        :param blue_start: blue 通道开始值
        :param blue_end: blue 通道结束值
        :return:
        """
        self.set_range_red(red_start, red_end)
        self.set_range_green(green_start, green_end)
        self.set_range_blue(blue_start, blue_end)

    def set_range_equally(self, start, end):
        """
        为三个通道添加相同的区域。
        :param start: 三个通道的开始值
        :param end: 三个通道的结束值
        :return:
        """
        self.set_range(start, end, start, end, start, end)

    # 以下是检测数值是否在区域内。写成三个是为了在程序运行时，节约传递参数的时间。
    def red_range_include(self, val):
        """
        检测数值 val 是否在任意已添加的 red 通道range内。是则返回 True，否则 False
        :param val: 输入的数值
        :return:
            True, if val is in one of ranges of red channel.
            False, if val is not in any ranges of red channel.
        """
        for ranges in self.red_range:
            if ranges[0] <= val <= ranges[1]:
                return True if not self.flip else False
        return False if not self.flip else True

    def green_range_include(self, val):
        """
        检测数值 val 是否在任意已添加的 green 通道range内。是则返回 True，否则 False
        :param val: 输入的数值
        :return:
            True, if val is in one of ranges of red channel.
            False, if val is not in any ranges of red channel.
        """
        for ranges in self.green_range:
            if ranges[0] <= val <= ranges[1]:
                return True if not self.flip else False
        return False if not self.flip else True

    def blue_range_include(self, val):
        """
        检测数值 val 是否在任意已添加的 green 通道range内。是则返回 True，否则 False
        :param val: 输入的数值
        :return:
            True, if val is in one of ranges of red channel.
            False, if val is not in any ranges of red channel.
        """
        for ranges in self.blue_range:
            if ranges[0] <= val <= ranges[1]:
                return True if not self.flip else False
        return False if not self.flip else True

    # 返回自己的类名称
    def get_self_name(self):
        return str(type(self)).split('.')[1][:-3]


