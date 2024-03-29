from Matrix_Access.Controllers.Color_Control.Color_Controller import ColorController
from Matrix_Access.Matrix_Accesser import MatrixAccesser
from Matrix_Access.Particles import MCParticle


class ColorWhiteList(ColorController):
    """
    颜色白名单。只有处于白名单区域内的颜色会被转换器考虑，并最终转换为mc指令。
    注意，是三个通道的颜色全部位于白名单范围内，才会被认为是允许的颜色。
    """

    def __init__(self, index_name, red_range=None, green_range=None, blue_range=None):
        # 默认白名单为接受所有颜色。
        self.red_range = red_range if red_range is not None else [(0.001, 1)]
        self.green_range = green_range if green_range is not None else [(0, 1)]
        self.blue_range = blue_range if blue_range is not None else [(0, 1)]
        super(ColorWhiteList, self).__init__(index_name)

    def set_red_default(self):
        """
        将 red 通道设定为初始状态 [(0.001, 1)]
        :return:
        """
        self.red_range = [(0.001, 1)]

    def set_green_default(self):
        """
        将 green 通道设定为初始状态 [(0, 1)]
        :return:
        """
        self.green_range = [(0, 1)]

    def set_blue_default(self):
        """
        将 blue 通道设定为初始状态 [(0, 1)]
        :return:
        """
        self.blue_range = [(0, 1)]

    def set_default(self):
        """
        将所有通道的值设定为默认值。
        :return:
        """
        self.set_red_default()
        self.set_green_default()
        self.set_blue_default()

    # 如果处于白名单状态下，对任意一个通道的置空，都将导致任何颜色都不能通过检测。
    # 而在黑名单模式下，则意味着允许任何颜色。
    def clear_range_red(self):
        """
        如果处于白名单模式下，对任意一个通道的置空，都将导致任何颜色都不能通过检测。
        因此，此类默认将相应通道的 range设定为最低值。
        :return:
        """
        self.red_range = []
        if not self.flip:
            self.red_range = [(0.001, 0.001)]

    def clear_range_green(self):
        """
        如果处于白名单模式下，对任意一个通道的置空，都将导致任何颜色都不能通过检测。
        因此，此类默认将相应通道的 range设定为最低值。
        :return:
        """
        self.green_range = []
        if not self.flip:
            self.green_range = [(0, 0)]

    def clear_range_blue(self):
        """
        如果处于白名单模式下，对任意一个通道的置空，都将导致任何颜色都不能通过检测。
        因此，此类默认将相应通道的 range设定为最低值。
        :return:
        """
        self.blue_range = []
        if not self.flip:
            self.blue_range = [(0, 0)]

    def accept_color(self, color_list):
        """
        一个颜色，只有三个通道全部处于白名单内，才能被接受。只要有一个通道的颜色不位于白名单内，则返回false。
        而如果 flip==True, 则同样将结果翻转。
        :param color_list: 输入的三通道颜色
        :return:
            True, if all color are in one or more ranges of each channel
            False, if any color are not in any ranges of its channel
        """
        if (self.red_range_include(color_list[0]) and
                self.green_range_include(color_list[1]) and
                self.blue_range_include(color_list[2])):
            return True
        return False

    def process(self, particle):
        """
        继承自 ControllerBase，输入完整粒子信息后，对其修改，并返回
        :param particle: MCParticle 类，包含所有可直接调用的数字参数。
        :return:
            particle: 经过处理后的粒子数据。
                    （WhiteList不会对粒子数据进行修改，只会判断是否符合，）
                    （如果是，则返回原本的粒子。如果不是，则返回 None。）
        """
        assert type(particle) is MCParticle
        if self.accept_color([particle.r, particle.g, particle.b]):
            return particle
        else:
            return None

    def process_matrix(self, matrix_accesser) -> MatrixAccesser:
        # 复制一个list
        mat_list_copy = matrix_accesser.get_mat_list()
        # 创建一个空矩阵
        matrix = []
        for particle in mat_list_copy:
            result = self.process(particle)
            # 如果反馈的部位none，说明没有被过滤掉，添加到矩阵
            if result is not None:
                matrix.append(result)
        # 用新矩阵替换掉原访问器的矩阵。
        matrix_accesser.renew_mat_list(matrix)
        return matrix_accesser

    # 以下是先前写的一个function，逻辑比较混乱，不确定是否有bug，先放在这里。
    # 收到一个颜色后，判定是否在 白名单内 / 黑名单外
    # def __accept_color(self, color_list):
    #     # 一个颜色，只有三个通道全部处于白名单内，才能被接受
    #     # 红色通道
    #     count = 0
    #     for ranges in self.red_range:
    #         # 白名单模式
    #         if not self.flip:
    #             # 只要颜色在任意白名单区域内，则分数加一。
    #             if ranges[0] < color_list[0] < ranges[1]:
    #                 count += 1
    #                 break
    #         # 黑名单模式
    #         else:
    #             # 只要颜色在任意黑名单区域内，则直接返回False
    #             if ranges[0] < color_list[0] < ranges[1]:
    #                 return False
    #
    #     # 绿色通道
    #     for ranges in self.green_range:
    #         # 白名单模式
    #         if not self.flip:
    #             # 只要颜色在任意白名单区域内，则分数加一。
    #             if ranges[0] < color_list[1] < ranges[1]:
    #                 count += 1
    #                 break
    #         # 黑名单模式
    #         else:
    #             # 只要颜色在任意黑名单区域内，则直接返回False
    #             if ranges[0] < color_list[1] < ranges[1]:
    #                 return False
    #
    #     # 蓝色通道
    #     for ranges in self.blue_range:
    #         # 白名单模式
    #         if not self.flip:
    #             # 只要颜色在任意白名单区域内，则分数加一。
    #             if ranges[0] < color_list[2] < ranges[1]:
    #                 count += 1
    #                 break
    #         # 黑名单模式
    #         else:
    #             # 只要颜色在任意黑名单区域内，则直接返回False
    #             if ranges[0] < color_list[2] < ranges[1]:
    #                 return False
    #
    #     if not self.flip:
    #         return True if count == 3 else False
    #     else:
    #         return True


class ColorTransWhiteList(ColorWhiteList):
    """
    颜色白名单。只有处于白名单区域内的颜色会被转换器考虑，并最终转换为mc指令。
    注意，是三个通道的颜色全部位于白名单范围内，才会被认为是允许的颜色。
    """

    def __init__(self, index_name=None, red_range=None, green_range=None, blue_range=None):
        super().__init__(index_name, red_range, green_range, blue_range)

    def process(self, particle):
        """
        与ColorWhiteList类似，唯一不同的是该类的process对粒子的TransforColor起作用。
        :param particle: MCParticle 类，包含所有可直接调用的数字参数。
        :return:
            particle: 经过处理后的粒子数据。
                    （WhiteList不会对粒子数据进行修改，只会判断是否符合，）
                    （如果是，则返回原本的粒子。如果不是，则返回 None。）
        """
        assert type(particle) is MCParticle
        if self.accept_color([particle.rt, particle.gt, particle.bt]):
            return particle
        else:
            return None
