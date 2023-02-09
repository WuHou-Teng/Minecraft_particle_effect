from Matrix_Access.Controllers.Color_Control.Color_Controller import ColorController
from Matrix_Access.Matrix_Accesser import MatrixAccesser
from Matrix_Access.Particles import MCParticle
from Matrix_Access.Controllers.Color_Control.Color_Controller_Const import *


class ColorPaintErasure(ColorController):
    """
    对任意通道的颜色进行线性加减。与别的颜色控制器不同，该控制器默认全通道执行。但依旧可以手动更改作用范围。
    """
    def __init__(self, index_name, red_range=FULL_RANGE, green_range=FULL_RANGE, blue_range=FULL_RANGE,
                 red_paint=0, green_paint=0, blue_paint=0):
        self.red_paint = red_paint if -1 < red_paint < 1 else 0
        self.green_paint = green_paint if -1 < green_paint < 1 else 0
        self.blue_paint = blue_paint if -1 < blue_paint < 1 else 0
        super().__init__(index_name, red_range, green_range, blue_range)

    def process(self, particle) -> MCParticle:
        """
        将对应颜色通道需要添加(减少)的颜色值添加到粒子上。并返回
        :param particle: MCParticle 实例
        :return:
            处理后的 MCParticle 实例
        """
        assert type(particle) is MCParticle
        if self.red_range_include(particle.r):
            particle.r = particle.r + self.red_paint
            if particle.r <= 0:
                particle.r = 0.001
            elif particle > 1:
                particle.r = 1
        if self.green_range_include(particle.g):
            particle.g = particle.g + self.green_paint
            if particle.g <= 0:
                particle.g = 0
            elif particle > 1:
                particle.g = 1
        if self.blue_range_include(particle.b):
            particle.b = particle.b + self.blue_paint
            if particle.b <= 0:
                particle.b = 0.001
            elif particle > 1:
                particle.b = 1

        return particle


class ColorTransPaintErasure(ColorPaintErasure):
    """
    此类与 ColorPaintErasure 基本相同，区别是此类用于处理粒子的转变颜色
    """

    def __init__(self, index_name, red_range=FULL_RANGE, green_range=FULL_RANGE, blue_range=FULL_RANGE,
                 red_paint=0, green_paint=0, blue_paint=0):
        super().__init__(index_name, red_range, green_range, blue_range,
                         red_paint, green_paint, blue_paint)

    def process(self, particle) -> MCParticle:
        """
        将对应颜色通道需要添加(减少)的颜色值添加到粒子上。并返回
        :param particle: MCParticle 实例
        :return:
            处理后的 MCParticle 实例
        """
        assert type(particle) is MCParticle
        if self.red_range_include(particle.rt):
            particle.rt = particle.rt + self.red_paint
            if particle.rt <= 0:
                particle.rt = 0.001
            elif particle > 1:
                particle.rt = 1
        if self.green_range_include(particle.gt):
            particle.gt = particle.gt + self.green_paint
            if particle.gt <= 0:
                particle.gt = 0
            elif particle > 1:
                particle.gt = 1
        if self.blue_range_include(particle.bt):
            particle.bt = particle.bt + self.blue_paint
            if particle.bt <= 0:
                particle.bt = 0.001
            elif particle > 1:
                particle.bt = 1

        return particle


