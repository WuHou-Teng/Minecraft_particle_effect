# -*- coding:utf-8 -*-
import copy
import os
from Matrix_Access.Matrix_Const import *
from Matrix_Access.Matrix_Writer import MatrixWriter
from Matrix_Access.Particles import MCParticle
import numpy as np


def complete_particle_format(particle):
    """
    :param particle: 粒子信息列表,
        ['x', 'y', 'z',
        'd_x', 'd_y', 'd_z', 'speed', 'count', 'force_normal',
        'R', 'G', 'B', 'TR', 'TG', 'TB', 'type','size',
        'duration', 'transparency', 'delay']
    :return:
        new_particle: MCParticle 类，包含所有可直接调用的数字参数。
    """
    # 检测粒子长度，并补全。
    if len(particle) < 20:
        for i in range(len(particle), 20):
            particle.append(DEFAULT_INFO[i])
    new_particle = MCParticle(float(particle[0]),  # 坐标
                              float(particle[1]),
                              float(particle[2]),
                              float(particle[3]),  # 移动坐标
                              float(particle[4]),
                              float(particle[5]),
                              float(particle[6]),  # 速度
                              int(particle[7]),  # 数量
                              particle[8],  # force or normal
                              float(particle[9]),  # R
                              float(particle[10]),  # G
                              float(particle[11]),  # B
                              float(particle[12]),  # RT
                              float(particle[13]),  # GT
                              float(particle[14]),  # BT
                              int(particle[15]),  # 粒子种类
                              float(particle[16]),  # 粒子大小
                              int(particle[17]),  # 粒子持续时常x_tick数
                              float(particle[18]),  # 粒子透明度
                              int(particle[19]))  # 延时x_tick数
    return new_particle


class MatrixAccesser(object):
    """
    与 MatrixGenerator 对应，该类用于系统的访问一个粒子矩阵文件。
    实例化此类，提供一个有效的粒子矩阵文件地址是强制性的。
    构造函数会在创建时尝试遍历整个粒子矩阵文件，并将相应的参数加载，备用。
    """

    def __init__(self, matrix_file, delay_type=ABSOLUTE):
        self.cwd = os.getcwd()
        # 粒子矩阵文件名称或绝对地址。如果仅仅提供了名称，程序会自动前往默认文件夹寻找。
        # self.mat_file = matrix_file
        self.mat_name = matrix_file
        # 载入默认路径
        self.default_path = []
        self.load_matrix_file_path()
        self.mat_file = self.matrix_file_found(self.mat_name)
        if self.mat_file is None:
            raise FileNotFoundError(f"矩阵文件不存在: {self.mat_name}")
        # 直接读取粒子矩阵文件，如果文件不存在，则返回空列表。
        self.mat_list = self.read_mat()

        # 最大粒子数量
        self.particle_num = 0
        # 个方向上的方位列表
        self.x_array = []
        self.y_array = []
        self.z_array = []
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
        self.delay_type = delay_type
        self.max_delay = 0
        self.delay_array = []

        self.get_extra_info()  # 可能比较耗时间。

    def load_matrix_file_path(self):
        """
        将默认路径加载到程序。方便在用户只提供matrix名字的时候，自动补全地址。
        :return:
        """
        with open(os.path.join(self.cwd, "Configs/default_matrix_address.txt"), "r", encoding="utf-8") as dm_address:
            new_addresses = dm_address.readlines()
            for lines in new_addresses:
                if not lines.startswith("#"):
                    self.default_path.append(lines.strip())

    def matrix_file_found(self, mat_file):
        """
        检测在默认path中是否包含目标 matrix。如果包含直接返回。优先度顺序按照 default_matrix_address.txt中排列。
        :param mat_file: 输入的 matrix文件名称
        :return:
        """
        if os.path.exists(mat_file):
            return mat_file
        for path in self.default_path:
            if os.path.exists(os.path.join(path, mat_file)):
                return os.path.join(path, mat_file)
            if os.path.exists(os.path.join(path, mat_file) + ".csv"):
                return os.path.join(path, mat_file)
        return None

    def get_name(self):
        return os.path.basename(self.mat_name)

    def get_mat_list(self):
        """
        获取已经读取的矩阵文件的内容的复制。
        :return:
        """
        # 注意，返回内容一定是deep copy
        return copy.deepcopy(self.mat_list)

    def set_mat_file(self, matrix_file_name):
        """
        将矩阵访问器的箭头指向新的矩阵文件。
        :param matrix_file_name:
        :return:
        """
        self.mat_file = matrix_file_name
        self.mat_list = self.read_mat()

    def reload_mat_list(self):
        """
        重新读取指向的矩阵文件，一般是 mat列表交给控制器更改后，再重新读取数据
        :return:
        """
        self.mat_list = self.read_mat()
        self.get_extra_info()

    def renew_mat_list(self, new_mat_list, update_original_file=False):
        """
        更新mat列表，一般是 mat列表交给控制器更改后，再重新放回对应的矩阵访问器。
        :param new_mat_list: 经过更改的 mat列表
        :param update_original_file: 是否将更新同步到对于的文件。
        :return:
        """
        self.mat_list = new_mat_list
        self.get_extra_info()
        if update_original_file:
            m_writer = MatrixWriter(self.mat_file)
            m_writer.renew_matrix_file(self.mat_list)

    def append_mat_list(self, new_mar_list, update_original_file=False):
        """
        更新mat列表，一般是 mat列表交给控制器更改后，再重新放回对应的矩阵访问器。
        不同的是，这里是直接添加到原来的列表末尾的。
        :param new_mar_list: 经过更改的 mat列表
        :param update_original_file: 是否将更新同步到对于的文件。
        :return:
        """
        self.mat_list = self.mat_file + new_mar_list
        self.get_extra_info()
        if update_original_file:
            m_writer = MatrixWriter(self.mat_file)
            m_writer.add_to_matrix_file(self.mat_list)

    def read_mat(self):
        """
        从相应的文件中读取矩阵数据。
        # 基本参数
          x, y, z, particle_type,
          1, 1, 1, 0(Undefined),
        # 附加参数
          d_x, d_y, d_z, speed, count, force_normal,
          0,   0,   0,   0,     1,     f/n,
        # 额外参数
          Color(R, G, B),   color_transfer(R,G), particle_type, 粒子大小,
          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,    0(Undefined),  1,
        # mod参数
          持续时间(x_tick=tick/5), 粒子透明度, 延时(x_tick=tick/5), 颜色渐变延时(x_tick=tick/5)
          80,                    1,        0,                   0

        :return:
            mat_array: 保存了整个矩阵的列表. 如果文件不存在，则返回空列表。
        """
        print("正在读取matrix文件并载入粒子信息")
        mat_array = []
        # 首先检索一边默认的文件夹。
        # search_result = self.matrix_file_found(self.mat_file)
        if self.mat_file is not None:
            with open(self.mat_file, "r", encoding='utf-8') as mat:
                mat_data = mat.readlines()
                for particles in mat_data:
                    # print(particles)
                    if len(particles) > 0 and particles[0] != "#":
                        particles_info = particles.strip().split(',')
                        if len(particles_info) >= 3:
                            for i in range(len(particles_info)):
                                particles_info[i] = particles_info[i].strip()
                            # 将粒子信息的数据格式进行修改。并生成新的粒子类。
                            particles_info = complete_particle_format(particles_info)
                            mat_array.append(particles_info)
                mat.close()
        print("完成粒子信息载入。")
        return mat_array

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

        # mat_array = np.array(self.mat_list)
        # self.x_array = mat_array[:, 0]
        # self.y_array = mat_array[:, 1]
        # self.z_array = mat_array[:, 2]
        # self.delay_array = mat_array[:, 16]

        for particle in self.mat_list:
            self.x_array.append(particle.x)
            self.y_array.append(particle.y)
            self.z_array.append(particle.z)
            self.delay_array.append(particle.delay)

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

        self.geom_centre = [(self.x_max + self.x_min) / 2,
                            (self.y_max + self.y_min) / 2,
                            (self.z_max + self.z_min) / 2]
        self.mean_centre = [np.mean(self.x_array),
                            np.mean(self.y_array),
                            np.mean(self.z_array)]

        print("完成信息提取")

# if __name__ == "__main__":
#     particles = [1, 2, 3]
#     print(complete_particle_format(particles))
