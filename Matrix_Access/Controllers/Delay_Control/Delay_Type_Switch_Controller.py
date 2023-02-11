from Matrix_Access.Controllers.Delay_Control.Delay_Base_Controller import DelayBaseController
from Matrix_Access.Matrix_Accesser import MatrixAccesser
from Matrix_Access.Matrix_Const import *
from Matrix_Access.Particles import MCParticle


class DelayTypeSwitchController(DelayBaseController):
    """
    将输入粒子的延时格式从 ADDITIONAL 和 ABSOLUTE之间相互转换。
    """
    def __init__(self, index_name, delay_type=ADDITIONAL, type_switch_to=ABSOLUTE):
        self.type_switch_to = type_switch_to
        super().__init__(index_name, delay_type)

    def set_delay_type_switch_to(self, delay_type):
        self.type_switch_to = delay_type

    def process(self, particle):
        """
        将输入粒子的延时格式从 ADDITIONAL 和 ABSOLUTE之间相互转换。
        :param particle: MCParticle 类，包含所有可直接调用的数字参数。
        :return:
        """
        assert type(particle) is MCParticle
        # 如果转换类型一样，则维持不变直接输出。
        if self.type_switch_to == self.delay_type:
            return particle
        # 否则考虑转换时间轴
        else:
            self.record_time(particle)  # 首先记录时刻
            if self.type_switch_to is ADDITIONAL:
                # 从绝对时间轴转化为累加时间轴。
                # 考虑到绝对时间轴中，时刻可能不是按照顺序排列的。
                # 所以允许delay为负数。
                particle.delay = particle.delay - self.last_time
            elif self.type_switch_to is ABSOLUTE:
                # 从累加时间轴到绝对时间轴。当前粒子时刻就是当前时刻。
                particle.delay = self.current_time
                # 如果转换后发现，绝对时间轴存在小于0的时间，则将其修改为0，
                if particle.delay < 0:
                    particle.delay = 0
            return particle

    def process_matrix(self, matrix_accesser):
        """
        从矩阵的宏观角度去修改delay_type, 会默认自动调用 update_dependency
        :param matrix_accesser:
        :return:
        """
        self.update_dependency(matrix_accesser)
        assert type(matrix_accesser) is MatrixAccesser
        for particle in matrix_accesser.mat_list:
            self.process(particle)
        matrix_accesser.delay_type = self.type_switch_to
        return matrix_accesser

    def update_dependency(self, matrix_accesser):
        self.current_time = 0
        self.last_time = 0
        self.delay_type = matrix_accesser.delay_type