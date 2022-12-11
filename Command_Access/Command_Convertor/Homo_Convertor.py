from Command_Access.Const import Particles_Java
from Command_Access.Command_Convertor.Base_Convertor import Convertor


class HomoConverter(Convertor):
    """
    二值转换器，只能识别黑白，产生黑白特效。
    x, y, z, delta_x, delta_y, delta_z, speed, count, force_normal, particle_color(R, G, B), color transfer(R,G,B)
    1, 1, 1, 0,       0,       0,       0,     1,     f/n,          0.001-1, 0-1, 0-1,        0.001-1, 0-1, 0-1

    # 对于相对坐标 ~x ~y ~z
    # 其中~x 是东+西-，~y是上+下-， ~z是南+北-
    # 对于实体视角坐标 ^x ^z ^y
    # 其中^x 是左+右-，^y是上+下-，^z则是前+后-。
    """

    def __init__(self):
        super(HomoConverter, self).__init__()
        # 单色转换器,只使用一种粒子。所以直接规定。
        # 双色转换器交给Color_dict_Convertor处理。
        self.particle = Particles_Java.end_rod  # 采用粒子end_rod

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

        # 将粒子丢去Controller box调整。
        particle_data = self.controller.apply_processing(particle_data)
        # 将所有的类型全部改为字符串。
        for i in range(len(particle_data)):
            particle_data[i] = str(particle_data[i])
        # 使用 ~ 还是 ^ 还是单纯的绝对坐标
        front_sign = self.coo_dict.get(self.coo_type)
        # force 还是 normal
        f_n = "force" if particle_data[9].strip() == "f" else "normal"

        # 开始翻译
        coord_str = (front_sign + particle_data[0] + front_sign + particle_data[1] + front_sign + particle_data[2] +
                     " " + particle_data[3] + " " + particle_data[4] + " " + particle_data[5] + particle_data)
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
            if data[0] in self.color_filter:
                continue
            funcs += self.coordinate_convertor(data)
        return funcs

    # 修改粒子类型
    def set_particle(self, particle):
        self.particle = particle


if __name__ == "__main__":
    convertor = HomoConverter()
    mat_file_address = "E:\work\Interesting_things\python_test\Mc_Effect\Mc_Partical_effect_Repo\Matrix_Files\Square_effect\square.txt"
    convertor.set_shift(0, 3, 0)
    convertor.set_scale(0.5, 0.5, 0.5)
    convertor.set_particle(Particles_Java.falling_water)
    convertor.set_modifier(AS)
    func = convertor.mat_convertor(convertor.read_mat(mat_file_address))
    print(func)
