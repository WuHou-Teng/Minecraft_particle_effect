from Command_Convertor.Controllers.Controller_Interface import ControllerBase


class ScaleController(ControllerBase):
    """
    缩放控制器
    """
    def __init__(self):
        super(ScaleController, self).__init__()
        # 转换时，坐标间隔缩放倍率
        self.x_scale = 1
        self.y_scale = 1
        self.z_scale = 1
        # 缩放中心点，[x, y, z]
        # 如果是二维图片，推荐将旋转中心点设在图片的二维平面上。
        # TODO 以后最好设计一个保留一个物体整体空间坐标的类，并且能正确反馈物体的各项属性，包括大小，边界外切立方体坐标。
        self.scale_centre = [0, 0, 0]

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
        :param particle: [x, y, z, d_x, d_y, d_z, speed, count, force_normal, R, G, B, TR, TG, TB, type]
        :return:
            particle: 经过处理后的粒子数据。
        """
        x_new, y_new, z_new = self.apply_scale(self.scale_centre[0], self.scale_centre[1], self.scale_centre[2])
        particle[0] = x_new
        particle[1] = y_new
        particle[2] = z_new
        return particle
