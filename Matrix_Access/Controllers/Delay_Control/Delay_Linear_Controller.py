from Matrix_Access.Controllers.Delay_Control.Delay_Base_Controller import DelayBaseController
from Matrix_Access.Matrix_Const import *


class DelayLinearController(DelayBaseController):
    """
    单纯的对输入的粒子增加或者减少相应的延时。
    """
    def __init__(self, delay_type=ABSOLUTE, tick_add=0):
        super().__init__(delay_type)
        self.tick_add = tick_add
        self.first_particle = True

    def process(self, particle):
        if self.delay_type is ADDITIONAL:
            # 如果计时方式为累加，只需要
            if self.first_particle:
                particle[16] += 1
                self.first_particle = False
                return particle
            else:
                return particle
        elif self.delay_type is ABSOLUTE:
            # 绝对时间轴，则依次+1即可。
            particle[16] += 1
            return particle


