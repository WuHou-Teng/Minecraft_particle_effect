from Matrix_Access.Controllers.Controller_Interface import ControllerBase
from Matrix_Access.Particles import MCParticle


class ShiftController(ControllerBase):
    """
    对粒子的坐标进行平移。
    """
    def __init__(self, index_name, x_shift=0, y_shift=0, z_shift=0):

        # 转换时，三个方向的偏移量。
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.z_shift = z_shift

        super(ShiftController, self).__init__(index_name)

    def set_x_shift(self, new_x):
        """
        设定 x轴偏移量
        :param new_x: x方向坐标，东 + 西 -， 如果是实体视角坐标，则是 左 + 右 -
        :return:
        """
        self.x_shift = new_x

    def set_y_shift(self, new_y):
        """
        设定 y轴偏移量
        :param new_y: y方向坐标，上 + 下 -
        :return:
        """
        self.y_shift = new_y

    def set_z_shift(self, new_z):
        """
        设定 z轴偏移量
        :param new_z: z方向坐标，南 + 北 -， 如果是实体视角坐标，则是 前 + 后 -
        :return:
        """
        self.z_shift = new_z

    def set_shift(self, x, y, z):
        """
        坐标整体平移。
        :param x: x方向坐标，东 + 西 -， 如果是实体视角坐标，则是 左 + 右 -
        :param y: y方向坐标，上 + 下 -
        :param z: z方向坐标，南 + 北 -， 如果是实体视角坐标，则是 前 + 后 -
        :return:
        """
        self.x_shift = x
        self.y_shift = y
        self.z_shift = z

    def do_shift(self, x, y, z):
        """
        将现有的坐标偏移量直接加到输入的粒子坐标上，并返回。
        :param x: 粒子 x轴坐标
        :param y: 粒子 y轴坐标
        :param z: 粒子 z轴坐标
        :return:
        """
        return x + self.x_shift, y + self.y_shift, z + self.z_shift

    def process(self, particle):
        """
        继承自 ControllerBase，输入完整粒子信息后，对其修改，并返回。
        :param particle: MCParticle 类，包含所有可直接调用的数字参数。
        :return:
        """
        assert type(particle) is MCParticle
        new_x, new_y, new_z = self.do_shift(particle.x, particle.y, particle.z)
        particle.x = new_x
        particle.y = new_y
        particle.z = new_z
        return particle
