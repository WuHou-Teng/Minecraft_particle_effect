import math
from Matrix_Access.Controllers.Controller_Interface import ControllerBase


class RotateController(ControllerBase):
    """
    对粒子的坐标进行旋转变化
    """
    def __init__(self, x_angle=0, y_angle=0, z_angle=0, rotate_centre=None):
        super(RotateController, self).__init__()
        # 转换时，各方向上的旋转角度。采用弧度单位。

        self.x_angle = x_angle
        self.y_angle = y_angle
        self.z_angle = z_angle
        # 旋转中心点
        # TODO 这里同样需要：以后最好设计一个保留一个物体整体空间坐标的类，并且能正确反馈物体的各项属性，包括大小，边界外切立方体坐标。
        self.rotate_centre = rotate_centre if rotate_centre is not None else [0, 0, 0]

    def set_x_angle(self, x_angle):
        self.x_angle = x_angle

    def set_y_angle(self, y_angle):
        self.y_angle = y_angle

    def set_z_angle(self, z_angle):
        self.z_angle = z_angle

    def set_rotate_angle(self, x_angle, y_angle, z_angle):
        """
        设定不同方向上的旋转角度，数字为正则【顺时针旋转】，数字为负则【逆时针旋转】
        :param x_angle: 以x轴为旋转轴，旋转的角度，采用弧度单位
        :param y_angle: 以y轴为旋转轴，旋转的角度，采用弧度单位
        :param z_angle: 以z轴为旋转轴，旋转的角度，采用弧度单位
        :return:
        """
        self.x_angle = x_angle
        self.y_angle = y_angle
        self.z_angle = z_angle

    def clear_angle(self):
        """
        清空旋转角。
        :return:
        """
        self.x_angle = 0
        self.y_angle = 0
        self.z_angle = 0

    def set_rotate_centre(self, central_point):
        """
        设定旋转中心。
        :param central_point: [x, y, z] 长度为 3 的列表，包含旋转中心点的坐标。默认为 [0,0,0]
        :return:
        """
        self.rotate_centre = central_point

    def apply_rotate_x(self, x, y, z):
        """
        沿着 x轴的旋转
        :param x: 粒子的 x坐标，
        :param y: 粒子的 y坐标
        :param z: 粒子的 z坐标
        :return:
            new_x, new_y, new_z: 粒子的新坐标。
        """
        # 因为以x轴旋转，所以x坐标不变。
        new_x = x
        # print("y: " + str(y) + "  rot:" + str(self.rotate_centre))
        dy = y - self.rotate_centre[1]
        dz = z - self.rotate_centre[2]
        # 求原本的角度, 其中，y视为纵轴，z视为横轴。
        if dz == 0:
            angle = math.pi/2
        else:
            angle = math.atan(dy / dz)
        # 求模
        dyz = math.pow(dy*dy + dz*dz, 0.5)
        # 计算新的y和z的坐标。
        new_y = self.rotate_centre[1] + math.sin(self.x_angle + angle) * dyz
        new_z = self.rotate_centre[2] + math.cos(self.x_angle + angle) * dyz
        return new_x, new_y, new_z

    def apply_rotate_z(self, x, y, z):
        """
        沿着 z轴的旋转
        :param x: 粒子的 x坐标，
        :param y: 粒子的 y坐标
        :param z: 粒子的 z坐标
        :return:
            new_x, new_y, new_z: 粒子的新坐标。
        """
        # 因为以z轴旋转，所以z坐标不变。
        new_z = z
        dy = y - self.rotate_centre[1]
        dx = x - self.rotate_centre[0]
        # 求原本的角度, 其中，y视为纵轴，x视为横轴。
        if dx == 0:
            angle = math.pi/2
        else:
            angle = math.atan(dy / dx)
        # 求模
        dyx = math.pow(dy*dy + dx*dx, 0.5)
        # 计算新的y和z的坐标。
        new_y = self.rotate_centre[1] + math.sin(self.z_angle + angle) * dyx
        new_x = self.rotate_centre[0] + math.cos(self.z_angle + angle) * dyx
        return new_x, new_y, new_z

    def apply_rotate_y(self, x, y, z):
        """
        沿着 y轴的旋转
        :param x: 粒子的 x坐标，
        :param y: 粒子的 y坐标
        :param z: 粒子的 z坐标
        :return:
            new_x, new_y, new_z: 粒子的新坐标。
        """
        # 因为以y轴旋转，所以y坐标不变。
        new_y = y
        dz = z - self.rotate_centre[2]
        dx = x - self.rotate_centre[0]
        # print("dx = x - " + "rotate_centre[0]" + " = " + str(x) + " - " +
        # str(self.rotate_centre[0]) + " = " + str(dx))
        # print("dz = z - " + "rotate_centre[2]" + " = " + str(z) + " - " +
        # str(self.rotate_centre[2]) + " = " + str(dz))
        # 求原本的角度, 其中，z视为纵轴，x视为横轴。
        if dx == 0:
            angle = math.pi/2
        else:
            angle = math.atan(dz / dx)

        # print("angle is: " + str(angle/math.pi) + "Π")

        # 求模
        dzx = math.pow(dx*dx + dz*dz, 0.5)
        # 计算新的y和z的坐标。
        new_z = self.rotate_centre[2] + math.sin(self.y_angle + angle) * dzx
        new_x = self.rotate_centre[0] + math.cos(self.y_angle + angle) * dzx
        # print("x 坐标从 " + str(x) + " 到 " + str(new_x))
        # print("z 坐标从 " + str(z) + " 到 " + str(new_z))
        # print("点从(" + str(x) + ", " + str(z) + ") 移动到" + "(" + str(new_x) + ", " + str(new_z) + ")")
        # print("————————————————————————————————————————")
        return new_x, new_y, new_z

    def process(self, particle):
        """
        继承自 ControllerBase，输入完整粒子信息后，对其修改，并返回。
        :param particle: [x, y, z, d_x, d_y, d_z, speed, count, force_normal, R, G, B, TR, TG, TB, type]
        :return:
            particle: 经过处理后的粒子数据。
        """
        # 由于旋转不对物体形状改变，所以xyz三个方向的旋转，施加顺序无需相同。
        x_new = particle[0]
        y_new = particle[1]
        z_new = particle[2]
        x_new, y_new, z_new = self.apply_rotate_x(x_new, y_new, z_new)
        x_new, y_new, z_new = self.apply_rotate_z(x_new, y_new, z_new)
        x_new, y_new, z_new = self.apply_rotate_y(x_new, y_new, z_new)
        particle[0] = x_new
        particle[1] = y_new
        particle[2] = z_new
        return particle


