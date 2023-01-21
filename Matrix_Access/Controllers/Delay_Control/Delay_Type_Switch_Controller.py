from Matrix_Access.Controllers.Delay_Control.Delay_Base_Controller import DelayBaseController
from Matrix_Access.Matrix_Const import *


class DelayTypeSwitchController(DelayBaseController):
    """
    将输入粒子的延时格式从 ADDITIONAL 和 ABSOLUTE之间相互转换。
    """
    def __init__(self, delay_type=ADDITIONAL, type_switch_to=ABSOLUTE):
        super().__init__(delay_type)
        self.type_switch_to = type_switch_to

    def set_delay_type_switch_to(self, delay_type):
        self.type_switch_to = delay_type

    def process(self, particle):
        # 如果转换类型一样，则维持不变直接输出。
        if self.type_switch_to == self.delay_type:
            return particle
        # 否则考虑从累加时间轴到绝对时间轴
        else:
            self.record_time(particle)  # 首先记录时刻
            if self.type_switch_to is ADDITIONAL:
                # 从绝对时间轴转化为累加时间轴。
                # 考虑到绝对时间轴中，时刻可能不是按照顺序排列的。
                # 所以允许delay为负数。
                particle[16] = particle[16] - self.last_time
            elif self.type_switch_to is ABSOLUTE:
                # 从累加时间轴到绝对时间轴。当前粒子时刻就是当前时刻。
                particle[16] = self.current_time
                # 如果转换后发现，绝对时间轴存在小于0的时间，则将其修改为0，
                if particle[16] < 0:
                    particle[16] = 0
            return particle




