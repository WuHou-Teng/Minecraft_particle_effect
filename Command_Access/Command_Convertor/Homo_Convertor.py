import os
from math import pi

from Command_Access.Command_Convertor.Base_Convertor import Convertor
from Command_Access.Const import Particles_Java
from Command_Access.Const.Convertor_consts import *
from Command_Access.DataPack_IO.Function_Writer import FunctionWriter
from Command_Access.Command_Generator.Executes.Execute_consts import *


class HomoConverter(Convertor):
    """
    二值转换器，只能识别黑白，产生黑白特效。
    x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type, 延时(tick)
    1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined),  0

    # 对于相对坐标 ~x ~y ~z
    # 其中~x 是东+西-，~y是上+下-， ~z是南+北-
    # 对于实体视角坐标 ^x ^z ^y
    # 其中^x 是左+右-，^y是上+下-，^z则是前+后-。
    """

    def __init__(self):
        super(HomoConverter, self).__init__()
        # 单色转换器,可以只使用一种粒子。所以允许直接规定。
        # 该参数如果不为None，则强制使用规定的粒子类型。如果为None，则采用矩阵中提供的粒子类型。
        self.force_particle = None
        # end_rod是27号粒子。
        # 双色转换器交给Color_dict_Convertor处理。

    def particle_convertor(self, particle_data):
        """
        对单个粒子坐标转换.
        对于相对坐标 ~x ~y ~z
        其中~x 是东+西-，~y是上+下-， ~z是南+北-
        对于实体视角坐标 ^x ^y ^z
        其中^x 是左+右-，^y是上+下-，^z则是前+后-。
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type, 延时(tick)
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined),  0
        :param particle_data: 单个粒子坐标以及颜色
        :return:
            召唤单个粒子的指令
        """

        # 将粒子丢去Controller box调整。
        particle_data = self.controller.apply_processing(particle_data)
        # 将所有的类型全部改为字符串。
        for i in range(len(particle_data)):
            if type(particle_data[i]) is float or type(particle_data[i]) is int:
                particle_data[i] = str(round(particle_data[i], 5))
        # 使用 ~ 还是 ^ 还是单纯的绝对坐标
        x_sign = self.coo_dict.get(self.coo_type[0])
        y_sign = self.coo_dict.get(self.coo_type[1])
        z_sign = self.coo_dict.get(self.coo_type[2])
        # force 还是 normal
        f_n = "force" if particle_data[8].strip() == "f" else "normal"
        particle = Particles_Java.particle_dict.get(particle_data[15]).strip()

        # 是否考虑延时设定:
        if self.use_delay:
            if self.timer_type is CLOUD:
                # TODO 修改ExecuteBuilder，为ExecuteLayer。execute指令是可以分层叠加的。可以叠很多层条件判定。
                pass

        # 如果使用execute，则提前准备好:
        if self.use_execute:
            if self.use_delay:
                pass

        # 开始翻译
        coord_str = (x_sign + particle_data[0] + y_sign + particle_data[1] + z_sign + particle_data[2] +
                     " " + particle_data[3] + " " + particle_data[4] + " " + particle_data[5] + " " + particle_data[6] +
                     " " + particle_data[7] + " " + f_n)

        if self.edition is JAVA:

            if self.use_execute:
                if self.force_particle is not None:

                    return self.execute_header.to_string() + "particle " + self.force_particle + coord_str + "\n"
                else:

                    return self.execute_header.to_string() + "particle " + particle + coord_str + "\n"
            else:
                if self.force_particle is not None:
                    return "particle " + self.force_particle + coord_str + "\n"
                else:
                    return "particle " + particle + coord_str + "\n"
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
        functions = []
        for data in matrix:
            functions.append(self.particle_convertor(data))
        return functions

    # 修改粒子类型
    def set_forced_particle(self, particle):
        self.force_particle = particle


# 用于方便测试的临时类。
class Cube(object):

    def __init__(self):
        self.convertor = HomoConverter()
        self.convertor.execute_header.set_modifier(AS)
        self.work_place = "C:\\Wuhou\\study\\python_test\\Mc_Effect\\Mc_Partical_effect_Repo\\"
        self.mat_address = "Matrix_Access\\Matrix_Files\\Square_effect\\"
        self.mat_file = "cube.csv"
        self.convertor.set_mat_file(self.work_place + self.mat_address + self.mat_file)

    def cube_rotate(self, x_angle, y_angle, z_angle, rotate_centre,
                    x_shift, y_shift, z_shift,
                    x_scale, y_scale, z_scale, scale_centre):
        # 添加旋转控制器。
        self.convertor.controller.add_controller_to_apply_list(
            self.convertor.controller.new_rotate_controller(x_angle, y_angle, z_angle, rotate_centre))

        # 添加缩放控制器
        self.convertor.controller.add_controller_to_apply_list(
            self.convertor.controller.new_scale_controller(x_scale, y_scale, z_scale, scale_centre)
        )

        # 添加位移控制器。
        self.convertor.controller.add_controller_to_apply_list(
            self.convertor.controller.new_shift_controller(x_shift, y_shift, z_shift)
        )

        result = self.convertor.mat_convertor(self.convertor.matrix_access.get_mat_list())
        self.convertor.controller.clear_controller_list()
        return result


if __name__ == "__main__":
    # ".minecraft\saves\新的世界 (1)\datapacks\partical_effect\data\square_effect\functions"
    game_address = "E:\\game\\mc\\1.18.2KuaYueII\\1.18.2KuaYueII"
    data_pack_address = os.path.join(game_address, ".minecraft\\saves\\新的世界 (1)\\datapacks\\partical_effect")
    name_space = "square_effect"
    function_name = "3d_rottest"
    func_writer = FunctionWriter(data_pack_address, name_space)
    # func_file = func_writer.new_func("3d_rotating")
    cube = Cube()
    #
    func_file = func_writer.new_func("3d_rotating")
    x_range = 73
    y_range = 1
    z_range = 1
    # func_writer.write_func("3d_rotating",
    #                        cube.cube_rotate(0 * pi / 36, 0 * pi / 36, 0 * pi / 36, [1.5, 1.5, 1.5], -1, -5, -1))
    for x_a in range(0, x_range):
        for y_a in range(0, y_range):
            for z_a in range(0, z_range):
                func_writer.add_func("3d_rotating",
                                     cube.cube_rotate(x_a * pi / 36, y_a * pi / 36, z_a * pi / 36, [1.5, 1.5, 1.5],
                                                      x_a - 1, -5 + y_a - 1, z_a - 1,
                                                      0.3, 5-x_a/5, 5-x_a/5, [1.5, 1.5, 1.5]))
