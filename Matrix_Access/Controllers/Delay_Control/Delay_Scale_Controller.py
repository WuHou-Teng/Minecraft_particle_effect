from Matrix_Access.Controllers.Delay_Control.Delay_Base_Controller import DelayBaseController
from Matrix_Access.Matrix_Const import *


class DelayScaleController(DelayBaseController):
    """
    按照比例缩放所有粒子的延时
    """
    def __init__(self, delay_type=ABSOLUTE, scale_ratio=1):
        super().__init__(delay_type)
        self.scale_ratio = scale_ratio
        if self.scale_ratio < 0:
            print("缩放率不和规定，已被调节至0")
            self.scale_ratio = 0

    def set_scale_ratio(self, new_scale_ratio):
        self.scale_ratio = new_scale_ratio
        if self.scale_ratio < 0:
            print("缩放率不和规定，已被调节至0")
            self.scale_ratio = 0

    def process(self, particle):
        """
        缩放延时。无论是累加计时，还是绝对计时，都是乘以缩放率即可。
        缩放率必须大于等于0. 如果缩放率为0, 则等效抹除所有的延时。
        :param particle: 粒子信息
        :return:
        """
        particle[16] *= self.scale_ratio
        return particle

