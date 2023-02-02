from Matrix_Access.Controllers.Delay_Control.Delay_Base_Controller import DelayBaseController
from Matrix_Access.Matrix_Const import *
from Matrix_Access.Particles import MCParticle


class DelayLinearController(DelayBaseController):
    """
    单纯的对输入的粒子增加或者减少相应的延时。
    """
    def __init__(self, delay_type=ABSOLUTE, tick_add=0):
        super().__init__(delay_type)
        self.tick_add = tick_add
        self.first_particle = True

    def process(self, particle):
        """
        增加或减少粒子延时
        :param particle:
        :return:
        """
        assert type(particle) is MCParticle
        if self.delay_type is ADDITIONAL:
            # 如果计时方式为累加，只需要在第一个数字上增减即可。
            # 该过程是否会出现负数无关紧要，因为最终转换都会转换为绝对时间轴，如果出现负数，则直接设定为0
            if self.first_particle:
                particle.delay += self.tick_add
                self.first_particle = False
                return particle
            else:
                return particle
        elif self.delay_type is ABSOLUTE:
            # 绝对时间轴，则依次加上即可。
            particle.delay += self.tick_add
            if particle.delay < 0:
                particle.delay = 0
            return particle
