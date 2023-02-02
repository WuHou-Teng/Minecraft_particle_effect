from Matrix_Access.Controllers.Controller_Interface import ControllerBase
from Matrix_Access.Particles import MCParticle


class ScaleController(ControllerBase):
    """
    缩放控制器
    """
    def __init__(self, index_name=None, x_scale=1, y_scale=1, z_scale=1, scale_centre=None):
        super(ScaleController, self).__init__(index_name)
        # 转换时，坐标间隔缩放倍率
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.z_scale = z_scale
        # 缩放中心点，[x, y, z]
        # 如果是二维图片，推荐将旋转中心点设在图片的二维平面上。
        self.scale_centre = scale_centre if scale_centre is not None else [0, 0, 0]

    def set_x_scale(self, new_x_scale):
        self.x_scale = new_x_scale

    def set_y_scale(self, new_y_scale):
        self.y_scale = new_y_scale

    def set_z_scale(self, new_z_scale):
        self.z_scale = new_z_scale

    def set_scale(self, new_x_scale, new_y_scale, new_z_scale):
        """
        各方向上坐标整体缩放。
        :param new_x_scale: x方向上的缩放倍率
        :param new_y_scale: y方向上的缩放倍率
        :param new_z_scale: z方向上的缩放倍率
        :return:
        """
        self.x_scale = new_x_scale
        self.y_scale = new_y_scale
        self.z_scale = new_z_scale

    def clear_scale(self):
        self.x_scale = 1
        self.y_scale = 1
        self.z_scale = 1

    def set_scale_centre(self, new_scale_centre):
        """
        设定缩放中心。
        :param new_scale_centre: 新的缩放中心点。如果是二维图片，推荐将缩放中心点设定在图片上。
        :return:
        """
        self.scale_centre = new_scale_centre

    def apply_scale(self, x, y, z):
        """
        对输入的粒子坐标，根据缩放中心的位置，进行各个位置上的缩放。
        :param x: 粒子 x坐标
        :param y: 粒子 y坐标
        :param z: 粒子 z坐标
        :return:
        """
        x_new = (x - self.scale_centre[0]) * self.x_scale + self.scale_centre[0]
        y_new = (y - self.scale_centre[1]) * self.y_scale + self.scale_centre[1]
        z_new = (z - self.scale_centre[2]) * self.z_scale + self.scale_centre[2]
        return x_new, y_new, z_new

    def process(self, particle):
        """
        继承自 ControllerBase，输入完整粒子信息后，对其修改，并返回。
        :param particle: MCParticle 类，包含所有可直接调用的数字参数。
        :return:
            particle: 经过处理后的粒子数据。
        """
        assert type(particle) is MCParticle
        x_new, y_new, z_new = self.apply_scale(particle.x, particle.y, particle.z)
        particle.x = x_new
        particle.y = y_new
        particle.z = z_new
        return particle
