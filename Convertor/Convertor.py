import os
from Const import Particles_Java
from Const import Particles_bedRock
from Const.Convertor_consts import *
from Const.color import *
from util.Color_Range_Exception import ColorRangeException
from Execute_Generator.Execute import ExecuteBuilder


class Convertor(object):
    """
    将坐标矩阵转换为粒子的基础类
    对于相对坐标 ~x ~y ~z
    其中~x 是东+西-，~y是上+下-， ~z是南+北-
    对于实体视角坐标 ^x ^y ^z
    其中^x 是左+右-，^y是上+下-，^z则是前+后-。
     x,  y,  z, delta_x, delta_y, delta_z, speed, count, force_normal, particle_color(R, G, B), color transfer(R,G,B)
    10, 10, 10, 0,       0,       0,       0,     1,     f/n,          0.05-1, 0-1, 0-1,        0.05-1, 0-1, 0-1
    """

    def __init__(self):
        # 要转换的矩阵文件
        self.mat_file = ""
        # 指令版本
        self.edition = JAVA  # 生成版本为Java
        self.particle = Particles_Java.end_rod  # 采用粒子end_rod
        # TODO, 在Const中添加 颜色——粒子 对应字典， 黑白和彩色个来一套。
        # self.particle_dict = {"Black": BLACK, "White": WHITE, "Trans": TRANSP}
        # 采用相对坐标
        self.coo_type = RELA_COORD
        # 坐标模式字典
        self.coo_dict = {RELA_COORD: " ~", FACE_COORD: " ^", ABS_COORD: ""}
        self.default_ignore_color = []  # 即将黑色或者无色粒子视为不存在。

        # Execute 指令
        self.use_execute = True
        self.execute_header = ExecuteBuilder()

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
        对单个粒子坐标转换.
        对于相对坐标 ~x ~y ~z
        其中~x 是东+西-，~y是上+下-， ~z是南+北-
        对于实体视角坐标 ^x ^y ^z
        其中^x 是左+右-，^y是上+下-，^z则是前+后-。
         x,  y,  z, delta_x, delta_y, delta_z, speed, count, force_normal, particle_color(R, G, B), color transfer(R,G,B)
        10, 10, 10, 0,       0,       0,       0,     1,     f/n,          0.05-1, 0-1, 0-1,        0.05-1, 0-1, 0-1
        :param particle_data: 单个粒子坐标以及颜色
        :return:
            召唤单个粒子的指令
        """
        pass

    def mat_convertor(self, matrix):
        """
        对输入的整个矩阵经行转换
        :param matrix: 输入的坐标矩阵
        :return:
            funcs: 转换好的一整个func的字符串形式，
                  后面会写入相应的.mcfunction文件
        """
        pass

    def set_mat_file(self, new_mat_file):
        self.mat_file = new_mat_file

    def read_mat(self):
        """
        从相应的文件读取位置矩阵
         x,  y,  z, delta_x, delta_y, delta_z, speed, count, force_normal, particle_color(R, G, B), color transfer(R,G,B)
        10, 10, 10, 0,       0,       0,       0,     1,     f/n,          0.05-1, 0-1, 0-1,        0.05-1, 0-1, 0-1
        :return:
            mat_array: 保存了整个矩阵的列表
        """
        mat_array = []
        with open(self.mat_file, "r") as mat:
            mat_data = mat.readlines()
            for particles in mat_data:
                print(particles)
                if len(particles) > 0 and particles[0] != "#":
                    particles_info = particles.strip().split(',')
                    if len(particles_info) > 10:
                        for i in range(len(particles_info)):
                            particles_info[i] = particles_info[i].strip()
                        mat_array.append(particles_info)
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

    # 修改坐标相对性
    def set_coo_type(self, coo_type):
        self.coo_type = coo_type
        if coo_type not in self.coo_dict.keys():
            self.coo_type = RELA_COORD

    # 修改移动速度倍率
    def set_speed_multi(self, speed_multi):
        self.speed_multi = speed_multi

    # 修改粒子运动范围倍率
    def set_motion_multi(self, motion_multi):
        self.motion_multi = motion_multi

    # 使用execute与否
    def execute_switch(self, true_or_false):
        self.use_execute = true_or_false

    # 设定忽视颜色
    def set_default_ignore_color(self, range_begin, range_end=None):
        """
        设定在转化为粒子特效时，忽略的颜色区间。
        该区间应该是由 [r_1, g_1, b_1] 与 [r_2, g_2, b_2] 的两个列表或元组组成。
        其中 r_1<=r_2, g_1<=g_2, b_1<=b_2
        :param range_begin: 忽略颜色区间的开始 [r_1, g_1, b_1]
        :param range_end: 忽略颜色区间的结尾 [r_2, g_2, b_2]
        :return:
        """
        if range_end is None:
            range_end = range_begin
        for i in range(3):
            if range_begin[i] > range_end[i]:
                raise ColorRangeException(self.get_self_name() + ", set_default_ignore_color")
        color_range = [[range_begin[0], range_end[0]], [range_begin[1], range_end[1]], [range_begin[2], range_end[2]]]
        self.default_ignore_color.append(color_range)

    def empty_default_ignore_color(self):
        """
        清空忽略颜色列表
        :return:
        """
        self.default_ignore_color = []

    # 检测所给颜色是否在忽略颜色区间范围内
    def ignore_color(self, color_list):
        """
        检测要转换的粒子的颜色是否在忽略颜色范围内。
        :param color_list: [r, g, b] r, g, b ∈ [0,1]
        :return:
        """
        for color_range in self.default_ignore_color:
            if color_list[0] < color_range[0][0] or color_list[0] > color_range[0][1]:
                return False
            if color_list[1] < color_range[1][0] or color_list[1] > color_range[1][1]:
                return False
            if color_list[2] < color_range[2][0] or color_list[2] > color_range[2][1]:
                return False
        return True

    # 返回自己的类名称
    def get_self_name(self):
        return str(type(self)).split('.')[1][:-3]
