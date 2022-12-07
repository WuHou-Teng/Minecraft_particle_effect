import os
from Const import Particles_Java
from Const import Particles_bedRock
from Const.Convertor_consts import *
from Const.Color import *
from util.Color_Range_Exception import ColorRangeException
from Execute_Generator.Execute import ExecuteBuilder
from Command_Convertor.Color_Controller.Color_Filter_Amp import ColorFilterAmp
from Command_Convertor.Color_Controller.Color_White_List import ColorWhiteList


class Convertor(object):
    """
    将坐标矩阵转换为粒子的基础类
    对于相对坐标 ~x ~y ~z
    其中~x 是东+西-，~y是上+下-， ~z是南+北-
    对于实体视角坐标 ^x ^y ^z
    其中^x 是左+右-，^y是上+下-，^z则是前+后-。
     x,  y,  z, delta_x, delta_y, delta_z, speed, count, force_normal, particle_color(R, G, B), color transfer(R,G,B)
    10, 10, 10, 0,       0,       0,       0,     1,     f/n,          0.001-1, 0-1, 0-1,        0.001-1, 0-1, 0-1
    """

    def __init__(self):
        # 要转换的矩阵文件
        self.mat_file = ""
        # 指令版本
        self.edition = JAVA  # 生成版本为Java
        # 这里不写明粒子使用，由子类自行规定
        # self.particle = Particles_Java.end_rod  # 采用粒子end_rod

        # 采用相对坐标
        self.coo_type = RELA_COORD
        # 坐标模式字典
        self.coo_dict = {RELA_COORD: " ~", FACE_COORD: " ^", ABS_COORD: ""}

        # 颜色过滤/增幅, 处于设定范围内的颜色，会被增幅或者削弱。详细内容请参考 ColorFilterAmp()
        # 颜色过滤/增幅器可以添加多个。
        empty_filter = ColorFilterAmp()
        self.color_filters = [empty_filter]
        # 只有三个通道的颜色都处于白名单范围内的粒子坐标会被最终转化为指令放入mcfunction
        self.color_white_list = ColorWhiteList()

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

        # TODO 转换时，为粒子添加移动。如果粒子本身delta_xyz不为零，则会将数值直接添加到delta_xyz上
        self.x_delta = 0
        self.y_delta = 0
        self.z_delta = 0

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
        x, y, z, delta_x, delta_y, delta_z, speed, count, force_normal, particle_color(R, G, B), color transfer(R,G,B)
        1, 1, 1, 0,       0,       0,       0,     1,     f/n,          0.001-1, 0-1, 0-1,        0.001-1, 0-1, 0-1
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
        x, y, z, delta_x, delta_y, delta_z, speed, count, force_normal, particle_color(R, G, B), color transfer(R,G,B)
        1, 1, 1, 0,       0,       0,       0,     1,     f/n,          0.05-1, 0-1, 0-1,        0.05-1, 0-1, 0-1
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
    # def set_particle(self, particle):
    #     self.particle = particle

    # 修改坐标相对性
    def set_coo_type(self, coo_type):
        self.coo_type = coo_type
        if coo_type not in self.coo_dict.keys():
            self.coo_type = RELA_COORD

    def add_filter(self, new_color_filter_amp=ColorFilterAmp()):
        """
        添加新的滤镜。推荐先设定好滤镜后再添加。
        :param new_color_filter_amp:
        """
        self.color_filters.append(new_color_filter_amp)

    def clear_filters(self):
        """
        清除所有已添加的滤镜，程序自动添加一个新的空白滤镜。
        """
        self.color_filters = [ColorFilterAmp()]

    # 修改移动速度倍率
    def set_speed_multi(self, speed_multi):
        """
        修改移动速度倍率，生成移动特效的时候，可能需要根据尺寸调整移动速度。
        :param speed_multi: 速度倍率调整。
        :return:
        """
        self.speed_multi = speed_multi

    # 修改粒子运动范围倍率
    def set_motion_multi(self, motion_multi):
        self.motion_multi = motion_multi

    # 使用execute与否
    def execute_switch(self, true_or_false):
        self.use_execute = true_or_false

    # 返回自己的类名称
    def get_self_name(self):
        return str(type(self)).split('.')[1][:-3]
