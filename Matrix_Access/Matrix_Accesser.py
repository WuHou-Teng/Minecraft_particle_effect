import copy


class MatrixAccesser(object):
    """
    与 MatrixGenerator 对应，该类用于系统的访问一个粒子矩阵文件。
    实例化此类，提供一个有效的粒子矩阵文件地址是强制性的。
    构造函数会在创建时尝试遍历整个粒子矩阵文件，并将相应的参数加载，备用。
    """
    def __init__(self, matrix_file_name):
        # 粒子矩阵文件名称
        self.mat_file = matrix_file_name
        # 直接读取粒子矩阵文件
        self.mat_array = self.read_mat()

    def get_mat_array(self):
        # 注意，返回内容一定是deep copy
        return copy.deepcopy(self.mat_array)

    def set_mat_file(self, matrix_file_name):
        self.mat_file = matrix_file_name
        self.mat_array = self.read_mat()

    def read_mat(self):
        """
        从相应的文件读取位置矩阵
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type, 延时(tick)
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined),  0
        :return:
            mat_array: 保存了整个矩阵的列表
        """
        mat_array = []
        if self.mat_file is not None:
            with open(self.mat_file, "r") as mat:
                mat_data = mat.readlines()
                for particles in mat_data:
                    # print(particles)
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

    # TODO 需要考虑计算的参数如下：
    # 各方向极点坐标
    #   x方向数值最小，最大的点
    #   y方向数值最小，最大的点
    #   z方向数值最小，最大的点
    # 矩阵外接长方体（该长方体与xyz轴对齐。）
    #   各顶点坐标
    #   长方体中心坐标
    # 矩阵外接圆
    #   圆心坐标
    #   圆的半径
    # 矩阵中所有粒子可能的延时时间。做一个列表，并返回。

