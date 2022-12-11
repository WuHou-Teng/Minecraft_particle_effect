from Command_Access import Command_Convertor
from Command_Access.Const.Particle_Color_dictionary import *


class ColorDictConvertor(Command_Convertor):
    """
    该类继承于Convertor类，同样是输出彩色粒子，但是该类是根据已有粒子的不同颜色进行转换的。
    需要提前设定 颜色-粒子 对应字典。
    """
    def __init__(self):
        super(ColorDictConvertor, self).__init__()

        # 默认粒子字典
        self.particle_dict = BIN_DIT_1


