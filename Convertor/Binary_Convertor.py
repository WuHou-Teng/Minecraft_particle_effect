import os
from Const import Particles_Java
from Const import Particles_bedRock
from Const.Other_const import *


class BinConverter(object):
    """
    二值转换器，只能识别黑白，产生黑白特效。
    # x,  z,  y,  particle_color (如果是二值，则颜色只有0，1，2三种，分别对应，黑，白，透明)
     10, 10, 10,  1

    # 对于相对坐标 ~x ~z ~y
    # 其中~x 是东+西-，~z是上+下-， ~y是南+北-
    # 对于实体视角坐标 ^x ^z ^y
    # 其中^x 是左+右-，^z是上+下-，^y则是前+后-。
    """

    def __init__(self, entity="@s"):
        self.edition = JAVA         # 生成版本为Java
        self.particle = Particles_Java.end_rod     # 采用粒子end_rod
        self.relative_coo = RELA_COORD    # 采用相对坐标
        self.default_ignore_color = [BLACK, TRANSP]   # 即将黑色粒子视为无色。

        # 确定目标实体, 默认值为指令方块自己
        self.entity = entity

        # 转换时，三个方向的偏移量。
        self.x_shift = 0
        self.z_shift = 0
        self.y_shift = 0

        # 转换时，坐标间隔缩放倍率
        self.x_scale = 0.1
        self.z_scale = 0.1
        self.y_scale = 0.1

    def coordinate_convertor(self, particle_data):
        """
        对单个粒子坐标转换
        :param particle_data: 单个粒子坐标及颜色
        :return:
            召唤单个粒子的指令
        """
        coord_str = ""
        # 相对坐标
        if self.relative_coo == RELA_COORD:
            coord_str = (" ~" + str(particle_data[0] * self.x_scale + self.x_shift) +
                         " ~" + str(particle_data[1] * self.z_scale + self.z_shift) +
                         " ~" + str(particle_data[2] * self.y_scale + self.y_shift))
        # 实体视角坐标,注意，此时xzy分别代表，左右，上下，前后
        elif self.relative_coo == FACE_COORD:
            coord_str = (" ^" + str(particle_data[0] * self.x_scale + self.x_shift) +
                         " ^" + str(particle_data[1] * self.z_scale + self.z_shift) +
                         " ^" + str(particle_data[2] * self.y_scale + self.y_shift))
        # 绝对坐标
        elif self.relative_coo == ABS_COORD:
            coord_str = (" " + str(particle_data[0] * self.x_scale + self.x_shift) +
                         " " + str(particle_data[1] * self.z_scale + self.z_shift) +
                         " " + str(particle_data[2] * self.y_scale + self.y_shift))
        if self.edition is JAVA:
            return "execute at " + self.entity + " run particle " + self.particle + coord_str + "\n"
        else:
            # 基岩版的暂时搁置
            pass

    def mat_convertor(self, matrix):
        """
        对输入的整个矩阵经行转换
        :param matrix: 输入的坐标矩阵
        :return:
            func: 转换好的一整个func的字符串形式，
                  后面会写入相应的.mcfunction文件
        """
        func = ""
        for data in matrix:
            if data[3] in self.default_ignore_color:
                continue
            func += self.coordinate_convertor(data)
        return func

    # 读取矩阵
    def read_mat(self, mat_file):
        mat_array = []
        with open(mat_file, "w+") as mat:
            mat_data = mat.readlines()
            for particles in mat_data:
                if len(particles) > 0 and particles[0] is not "#":
                    if len(particles.strip().split(',')) == 4:
                        mat_array.append(particles.strip().split(','))
            mat.close()
        return mat_array

