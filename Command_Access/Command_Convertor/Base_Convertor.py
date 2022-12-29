from Command_Access.Command_Generator.Executes.Execute_Builder import ExecuteBuilder
from Matrix_Access.Controllers.Controller_Applier import ControllerApplier
from Matrix_Access.Matrix_Accesser import MatrixAccesser
from Command_Access.Const.Convertor_consts import *


class Convertor(object):
    """
    将坐标矩阵转换为粒子的基础类，
    对于相对坐标 ~x ~y ~z，
    其中~x 是东+西-，~y是上+下-， ~z是南+北-，
    对于实体视角坐标 ^x ^y ^z，
    其中^x 是左+右-，^y是上+下-，^z则是前+后-。
    x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type, 延时(tick)
    1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined)   0
    """

    def __init__(self):
        # 要转换的矩阵文件
        self.mat_file = None
        # 指令版本
        self.edition = JAVA  # 生成版本为Java
        # 这里不写明粒子使用，由子类自行规定
        # self.particle = Particles_Java.end_rod  # 采用粒子end_rod

        # 默认三个方向都采用相对坐标
        self.coo_type = [RELA_COORD, RELA_COORD, RELA_COORD]
        # 坐标模式字典
        self.coo_dict = {RELA_COORD: " ~", FACE_COORD: " ^", ABS_COORD: " "}

        # Execute 指令
        self.use_execute = True
        self.execute_header = ExecuteBuilder()

        # 关于延时。
        # 考虑封装一个计时控制器。这个控制器可以自动将特效分成 start，和content两个函数。start负责创建云计时器，content负责自循环。

        # 变换: 添加控制器。可以自定义一系列对矩阵的修改。
        # 注意，控制器的特点是逐个对粒子进行变换，不关注整体。因此，其效果不如自定义函数那样强大，仅可以机械化的进行简单的变换。
        # 再次注意，ControllerToolBox不具有写入matrix的功能，
        # 在convertor中可以直接调用ControllerToolBox进行转换，但是此后，转换得到的粒子矩阵不会被保留。
        self.controller = ControllerApplier()

        # 矩阵读取器
        self.matrix_access = None

    def set_mat_file(self, new_mat_file):
        self.mat_file = new_mat_file
        self.matrix_access = MatrixAccesser(self.mat_file)

    def coordinate_convertor(self, particle_data):
        """
        对单个粒子坐标转换.
        对于相对坐标 ~x ~y ~z
        其中~x 是东+西-，~y是上+下-， ~z是南+北-
        对于实体视角坐标 ^x ^y ^z
        其中^x 是左+右-，^y是上+下-，^z则是前+后-。
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type, 延时(tick)
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined)   0
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

    # 修改坐标相对性
    def set_coo_type(self, x_coo_type, y_coo_type=None, z_coo_type=None):
        if x_coo_type not in self.coo_dict.keys():
            x_coo_type = RELA_COORD
        if y_coo_type is None:
            y_coo_type = x_coo_type
        if z_coo_type is None:
            z_coo_type = x_coo_type
        self.coo_type = [x_coo_type, y_coo_type, z_coo_type]

    # 使用execute与否
    def execute_switch(self, true_or_false):
        self.use_execute = true_or_false

    def use_delay_switch(self, true_or_false):
        self.use_delay = true_or_false

    def set_timer_type(self, timer_type):
        """
        设定计时器方式。可以是schedule，也可以是体积云。
        :param timer_type: SCHEDULE / CLOUD
        """
        self.timer_type = timer_type

    # 返回自己的类名称
    def get_self_name(self):
        return str(type(self)).split('.')[1][:-3]
