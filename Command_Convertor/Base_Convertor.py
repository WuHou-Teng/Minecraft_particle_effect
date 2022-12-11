from Const.Convertor_consts import *
from Execute_Generator.Execute import ExecuteBuilder
from Controllers.ControllerBox import ControllerToolBox


class Convertor(object):
    """
    将坐标矩阵转换为粒子的基础类
    对于相对坐标 ~x ~y ~z
    其中~x 是东+西-，~y是上+下-， ~z是南+北-
    对于实体视角坐标 ^x ^y ^z
    其中^x 是左+右-，^y是上+下-，^z则是前+后-。
    x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type
    1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined)
    """

    def __init__(self):
        # 要转换的矩阵文件
        self.mat_file = None
        # 指令版本
        self.edition = JAVA  # 生成版本为Java
        # 这里不写明粒子使用，由子类自行规定
        # self.particle = Particles_Java.end_rod  # 采用粒子end_rod

        # 采用相对坐标
        self.coo_type = RELA_COORD
        # 坐标模式字典
        self.coo_dict = {RELA_COORD: " ~", FACE_COORD: " ^", ABS_COORD: " "}

        # Execute 指令
        self.use_execute = True
        self.execute_header = ExecuteBuilder()

        # 变换: 添加控制器。可以自定义一系列对矩阵的修改。
        # 注意，控制器的特点是逐个对粒子进行变换，不关注整体。因此，其效果不如自定义函数那样强大，仅可以机械化的进行简单的变换。
        self.controller = ControllerToolBox()

    def coordinate_convertor(self, particle_data):
        """
        对单个粒子坐标转换.
        对于相对坐标 ~x ~y ~z
        其中~x 是东+西-，~y是上+下-， ~z是南+北-
        对于实体视角坐标 ^x ^y ^z
        其中^x 是左+右-，^y是上+下-，^z则是前+后-。
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined)
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
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined)
        :return:
            mat_array: 保存了整个矩阵的列表
        """
        mat_array = []
        if self.mat_file is not None:
            with open(self.mat_file, "r") as mat:
                mat_data = mat.readlines()
                for particles in mat_data:
                    print(particles)
                    if len(particles) > 0 and particles[0] != "#":
                        particles_info = particles.strip().split(',')
                        if len(particles_info) > 10:
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
            'force_normal', 'R', 'G', 'B', 'TR', 'TG', 'TB', 'type']
        :return:
            particle: 经过修改的粒子信息列表: 将必要的数据修改为数字
            [x, y, z, d_x, d_y, d_z, speed, count, 'force_normal', R, G, B, TR, TG, TB, 'type']
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

        return particle

    # 修改坐标相对性
    def set_coo_type(self, coo_type):
        self.coo_type = coo_type
        if coo_type not in self.coo_dict.keys():
            self.coo_type = RELA_COORD

    # 使用execute与否
    def execute_switch(self, true_or_false):
        self.use_execute = true_or_false

    # 返回自己的类名称
    def get_self_name(self):
        return str(type(self)).split('.')[1][:-3]
