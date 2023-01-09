import copy
import os
from Matrix_Access.Matrix_Const import *
import numpy as np


class MatrixAccesser(object):
    """
    与 MatrixGenerator 对应，该类用于系统的访问一个粒子矩阵文件。
    实例化此类，提供一个有效的粒子矩阵文件地址是强制性的。
    构造函数会在创建时尝试遍历整个粒子矩阵文件，并将相应的参数加载，备用。
    """
    def __init__(self, matrix_file_name):
        self.cwd = os.getcwd()
        # 粒子矩阵文件名称
        self.mat_file = matrix_file_name
        # 载入默认路径
        self.default_path = []
        self.load_matrix_file_path()
        # 直接读取粒子矩阵文件
        self.mat_list = self.read_mat()

        # 最大粒子数量
        self.particle_num = 0
        # 个方向上的方位列表
        self.x_array = None
        self.y_array = None
        self.z_array = None
        # 各方向上的极值
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0
        self.z_max = 0
        self.z_min = 0
        # 各方向极值坐标组成的长方体的中心点
        self.geom_centre = [0, 0, 0]
        # 个方向上坐标的平均值组成的中心点
        self.mean_centre = [0, 0, 0]
        # 延时
        self.delay_type = ADDITIONAL
        self.max_delay = 0
        self.delay_array = None

        # self.get_extra_info() 默认不调用，因为可能比较耗时间。

    def load_matrix_file_path(self):
        with open("./default_matrix_address.txt", "r", encoding="UTF-8") as dm_address:
            new_addresses = dm_address.readlines()
            for lines in new_addresses:
                if not lines.startswith("#"):
                    self.default_path.append(lines.strip())

    def get_name(self):
        return self.mat_file

    def get_mat_array(self):
        # 注意，返回内容一定是deep copy
        return copy.deepcopy(self.mat_list)

    def set_mat_file(self, matrix_file_name):
        self.mat_file = matrix_file_name
        self.mat_list = self.read_mat()

    def matrix_file_found(self, mat_file):
        if os.path.exists(mat_file):
            return mat_file
        for path in self.default_path:
            if os.path.exists(os.path.join(path, mat_file)):
                return os.path.join(path, mat_file)
        return None

    def read_mat(self):
        """
        从相应的文件读取位置矩阵
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type, 延时(tick)
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined),  0
        :return:
            mat_array: 保存了整个矩阵的列表
        """
        mat_array = []
        # 首先检索一边默认的文件夹。
        search_result = self.matrix_file_found(self.mat_file)
        if search_result is not None:
            with open(search_result, "r") as mat:
                mat_data = mat.readlines()
                for particles in mat_data:
                    # print(particles)
                    if len(particles) > 0 and particles[0] != "#":
                        particles_info = particles.strip().split(',')
                        if len(particles_info) == 17:
                            for i in range(len(particles_info)):

                                particles_info[i] = particles_info[i].strip()
                            # 将粒子信息的数据格式进行修改。
                            particles_info = self.alert_particle_format(particles_info)
                            mat_array.append(particles_info)
                mat.close()
        return mat_array

    def alert_particle_format(self, particle):
        """
        修改粒子信息列表内元素的数据格式。
        :param particle: 粒子信息列表,
            ['x', 'y', 'z', 'd_x', 'd_y', 'd_z', 'speed', 'count',
            'force_normal', 'R', 'G', 'B', 'TR', 'TG', 'TB', 'type', 'delay']
        :return:
            particle: 经过修改的粒子信息列表: 将必要的数据修改为数字
            [x, y, z, d_x, d_y, d_z, speed, count, 'force_normal', R, G, B, TR, TG, TB, 'type', 'delay']
        """
        particle[0] = float(particle[0])  # 坐标
        particle[1] = float(particle[1])
        particle[2] = float(particle[2])
        particle[3] = float(particle[3])  # 移动坐标
        particle[4] = float(particle[4])
        particle[5] = float(particle[5])
        particle[6] = float(particle[6])  # 速度
        particle[7] = int(particle[7])    # 数量

        particle[9] = float(particle[9])    # R
        particle[10] = float(particle[10])  # G
        particle[11] = float(particle[11])  # B

        particle[12] = float(particle[12])  # TR
        particle[13] = float(particle[13])  # TG
        particle[14] = float(particle[14])  # TB

        particle[15] = int(particle[15])    # 粒子种类

        particle[16] = int(particle[16])    # 延时tick数

        return particle

    # 整个矩阵内所有点的数量。
    # 各方向极点坐标
    #   x方向数值最小，最大的点
    #   y方向数值最小，最大的点
    #   z方向数值最小，最大的点
    # 矩阵外接长方体（该长方体与xyz轴对齐。）
    #   各顶点坐标
    #   长方体中心坐标

    # 矩阵中所有粒子可能的延时时间。做一个列表，并返回。

    def get_extra_info(self):
        """

        :return:
        """
        print("正在提取矩阵信息")
        self.particle_num = len(self.mat_list)

        mat_array = np.array(self.mat_list)
        self.x_array = mat_array[:, 0]
        self.y_array = mat_array[:, 1]
        self.z_array = mat_array[:, 2]
        self.delay_array = mat_array[:, 16]
        # for particle in self.mat_list:
        #     self.x_list.append(particle[0])
        #     self.y_list.append(particle[1])
        #     self.z_list.append(particle[2])
        #     self.delay_list.append(particle[16])

        # x_array = np.array(self.x_list)
        # y_array = np.array(self.y_list)
        # z_array = np.array(self.z_list)
        # delay_list = np.array(delay_list)

        # 获取最大时间。
        if self.delay_type is ADDITIONAL:
            self.max_delay = np.sum(self.delay_array)
        elif self.delay_type is ABSOLUTE:
            self.max_delay = np.max(self.delay_array)

        self.x_max = np.max(self.x_array)
        self.x_min = np.min(self.x_array)
        self.y_max = np.max(self.y_array)
        self.y_min = np.min(self.y_array)
        self.z_max = np.max(self.z_array)
        self.z_min = np.min(self.z_array)

        self.geom_centre = [(self.x_max + self.x_min)/2,
                            (self.y_max + self.y_min)/2,
                            (self.z_max + self.z_min)/2]
        self.mean_centre = [self.x_array.mean(),
                            self.y_array.mean(),
                            self.z_array.mean()]

        print("完成信息提取")

