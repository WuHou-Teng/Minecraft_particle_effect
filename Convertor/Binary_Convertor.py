import os
from Const import Particles_Java
from Const import Particles_bedRock
from Const.Other_const import *


class BinConverter(object):
    """
    二值转换器，只能识别黑白，产生黑白特效。
    # particle_color, x,  y,  z, delta_x, delta_y, delta_z, speed, count, force or normal
      1,             10, 10, 10, 0,       0,       0,       0,     1,     f/n

    # 对于相对坐标 ~x ~y ~z
    # 其中~x 是东+西-，~y是上+下-， ~z是南+北-
    # 对于实体视角坐标 ^x ^z ^y
    # 其中^x 是左+右-，^y是上+下-，^z则是前+后-。
    """

    def __init__(self, modifier=AS, entity="@p"):
        self.edition = JAVA         # 生成版本为Java
        self.particle = Particles_Java.end_rod     # 采用粒子end_rod
        # 粒子对应字典
        self.particle_dict = {"Black": BLACK, "White": WHITE, "Trans": TRANSP}
        # 采用相对坐标
        self.coo_type = RELA_COORD
        # 坐标模式字典
        self.coo_dict = {RELA_COORD: " ~", FACE_COORD: " ^", ABS_COORD: ""}
        self.default_ignore_color = [BLACK, TRANSP]   # 即将黑色或者无色粒子视为不存在。

        # 方位/身份 修饰符，默认为 as
        # as at facing align anchored
        self.modifier = modifier

        # 确定目标实体, 默认值为最近玩家
        # @a @p @r @e @s
        self.entity = entity

        # 转换时，三个方向的偏移量。
        self.x_shift = 0
        self.y_shift = 0
        self.z_shift = 0

        # 转换时，坐标间隔缩放倍率
        self.x_scale = 0.1
        self.y_scale = 0.1
        self.z_scale = 0.1

        # 转换时，粒子运动范围倍率
        self.motion_multi = 1

        # 转换时，可能需要同样更改移动速度。
        self.speed_multi = 1

    def coordinate_convertor(self, particle_data):
        """
        对单个粒子坐标转换
        # particle_color, x,  y,  z, delta_x, delta_y, delta_z, speed, count, force or normal
          1,             10, 10, 10, 0,       0,       0,       0,     1,     f/n
        :param particle_data: 单个粒子坐标及颜色
        :return:
            召唤单个粒子的指令
        """
        coord_str = ""
        # 使用 ~ 还是 ^ 还是单纯的绝对坐标
        front_sign = self.coo_dict.get(self.coo_type)
        # force 还是 normal
        f_n = "force" if particle_data[9].strip() == "f" else "normal"
        # 开始翻译
        coord_str = (front_sign + str(round(int(particle_data[1]) * self.x_scale, 2) + self.x_shift) +
                     front_sign + str(round(int(particle_data[2]) * self.y_scale, 2) + self.y_shift) +
                     front_sign + str(round(int(particle_data[3]) * self.z_scale, 2) + self.z_shift) +
                     " " + str(round(int(particle_data[4]) * self.motion_multi)) +
                     " " + str(round(int(particle_data[5]) * self.motion_multi)) +
                     " " + str(round(int(particle_data[6]) * self.motion_multi)) +
                     " " + str(round(int(particle_data[7]) * self.speed_multi)) +
                     " " + particle_data[8] + " " + f_n)

        if self.edition is JAVA:
            return ("execute " + self.modifier + " " + self.entity + " run particle " + self.particle.strip() +
                    coord_str + "\n")
        else:
            # 基岩版的暂时搁置
            pass

    def mat_convertor(self, matrix):
        """
        对输入的整个矩阵经行转换
        :param matrix: 输入的坐标矩阵
        :return:
            funcs: 转换好的一整个func的字符串形式，
                  后面会写入相应的.mcfunction文件
        """
        funcs = ""
        for data in matrix:
            if data[0] in self.default_ignore_color:
                continue
            funcs += self.coordinate_convertor(data)
        return funcs

    # 读取矩阵
    def read_mat(self, mat_file):
        """
        从相应的文件读取位置矩阵
        :param mat_file: 矩阵文件的位置
        :return:
            mat_array: 保存了整个矩阵的列表
        """
        mat_array = []
        with open(mat_file, "r") as mat:
            mat_data = mat.readlines()
            for particles in mat_data:
                print(particles)
                if len(particles) > 0 and particles[0] != "#":
                    if len(particles.strip().split(',')) == 10:
                        mat_array.append(particles.strip().split(','))
                        # TODO 没有对内容进一步strip，可能导致问题。不过问题暂时不大。
            mat.close()
        return mat_array

    # 修改shift
    def set_shift(self, x, z, y):
        self.x_shift = x
        self.z_shift = y
        self.y_shift = z

    # 修改缩放
    def set_scale(self, x, y, z):
        self.x_scale = x
        self.y_scale = y
        self.z_scale = z

    # 修改粒子类型
    def set_particle(self, particle):
        self.particle = particle

    # 修改方位修饰符修饰符
    def set_modifier(self, modifier):
        self.modifier = modifier

    # 修改目标实体
    def set_entity(self, entity):
        self.entity = entity

    # 修改对象
    def set_coo_type(self, coo_type):
        self.coo_type = coo_type
        if coo_type not in self.particle_dict.keys():
            self.coo_type = RELA_COORD

    # 修改移动速度倍率
    def set_speed_multi(self, speed_multi):
        self.speed_multi = speed_multi

    # 修改粒子运动范围倍率
    def set_motion_multi(self, motion_multi):
        self.motion_multi = motion_multi

    # 设定忽视颜色
    def set_default_ignore_color(self, default_ignore_color):
        self.default_ignore_color = default_ignore_color
        if type(default_ignore_color) is not list:
            self.default_ignore_color = self.default_ignore_color = [BLACK, TRANSP]


if __name__ == "__main__":
    convertor = BinConverter()
    mat_file_address = "E:\work\Interesting_things\python_test\Mc_Effect\Mc_Partical_effect_Repo\Matrix_Files\Square_effect\square.txt"
    convertor.set_shift(0, 3, 0)
    convertor.set_scale(0.5, 0.5, 0.5)
    convertor.set_particle(Particles_Java.falling_water)
    convertor.set_modifier(AS)
    func = convertor.mat_convertor(convertor.read_mat(mat_file_address))
    print(func)



