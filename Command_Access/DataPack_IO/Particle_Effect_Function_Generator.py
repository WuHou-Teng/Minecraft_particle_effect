import os
# ok
from Command_Access.Command_Convertor.Homo_Convertor import HomoConverter
# 尚未完成
from Command_Access.Command_Convertor.Color_Convertor import ColorConvertor
# 尚未完成
from Command_Access.DataPack_IO.Function_Writer import FunctionWriter
# Layer 尚未完成
from Command_Access.Command_Generator.Executes.Execute_Builder import ExecuteBuilder
from Command_Access.Command_Generator.Executes.Execute_Layer_Box import ExecuteLayerBox
# ok
from Command_Access.Command_Generator.Entities.Entity_Box import EntityBox
# ok
from Command_Access.Command_Generator.Selector.Target_Selector_Box import TargetSelectorBox
# ScoreBoardGenerator 尚未完成
from Command_Access.Command_Generator.Score_Board.ScoreBoard_Box import ScoreBoardBox

# ok, MatrixAccesser本身尚未完成
from Matrix_Access.Matrix_Accesser_Box import MatrixAccessBox
# ok
from Matrix_Access.Controllers.Controller_Box import ControllerBox
from Matrix_Access.Controllers.Controller_Applier import ControllerApplier
# 尚未完成更细化的文件归类，但是能用
from Matrix_Access.Matrix_Writer import MatrixWriter


class PEFuncGenerator(object):
    """
    单个粒子特效生成器。
    包含矩阵读取，矩阵处理，
    指令生成，实体创建，计时，计分板
    指令转换 等一系列功能。
    """
    def __init__(self, datapack_address, new_effect_name):
        """
        初始化，把所有需要启动的模块都创建出来。
        :param datapack_address: 数据包地址
        :param new_effect_name: 新特效名字
        """
        self.effect_name = new_effect_name
        # 初始化两种转换器
        self.homo_convertor = HomoConverter()
        self.color_convertor = ColorConvertor()
        # 初始化函数书写器
        self.function_writer = FunctionWriter(datapack_address, new_effect_name)

        # 初始化实体盒子（用于储存之前创建的实体）
        self.entity_box = EntityBox()
        # 初始化选择器盒子（用于储存之前创建的选择器）
        self.selector_box = TargetSelectorBox()
        # 初始化执行生成器(类似ControllerApplier, 按照顺序储存并调用)
        self.execute_builder = ExecuteBuilder()
        # 初始化执行层盒子（用于储存之前创建的执行层）
        self.execute_layer_box = ExecuteLayerBox()
        # 初始化计分板盒子
        self.scoreboard_box = ScoreBoardBox()

        # 初始化矩阵访问器盒子（用于储存之前创建的访问器）
        self.matrix_access_box = MatrixAccessBox

        # 初始化控制器盒子
        self.controller_box = ControllerBox()
        # 初始化控制器调用器
        self.controller_applier = ControllerApplier()
        # 初始化矩阵书写
        self.matrix_writer = MatrixWriter()


# ——————————————————————以下类弃用，用上面的————————————————————————
class _ParticleEffectFuncGenerator(object):
    """
    粒子特效文件夹生成器。
    """

    # 考虑到未来可能要把很多个基础特效组合起来，变成复合特效。
    def __init__(self, new_effect_name="", data_pack_address="", matrix_addresses_list=""):
        """
        初始化
        :param new_effect_name: 新特效名称
        :param data_pack_address: 数据包地址
        :param matrix_addresses_list: 要添加的特效空间坐标+颜色矩阵列表。
        """
        self.cwd = os.getcwd()
        # 数据包地址应当一直指向data文件夹内
        # 例如
        # E:\\play_game\\mc\\1.18.2KuaYueII 乙烯\\1.18.2KuaYueII\\.minecraft\\saves\\新的世界 (1)
        # \\datapacks\\partical_effect\\data
        self.data_pack_address = data_pack_address
        # 一个包含了所有需要转换的特效矩阵的列表，该列表来自
        self.matrix_addresses_list = matrix_addresses_list
        # 每帧之间的时间间隔（tick）（可调）
        # mc 一秒 = 20 tick
        # self.frame_time_interval = frame_time_interval
        # 新的特效名称
        self.effect_name = new_effect_name

    # 创建新的特效文件夹
    def new_effect_folder(self):
        effect_address = os.path.join(self.data_pack_address, self.effect_name)
        if not os.path.exists(effect_address):
            os.mkdir(effect_address)
        return effect_address

    # 创建对应的特效文件夹
    def new_effect_func_folder(self, effect_address):
        new_effect_functions_folder = os.path.join(effect_address, "functions")
        if not os.path.exists(new_effect_functions_folder):
            os.mkdir(new_effect_functions_folder)
        return new_effect_functions_folder

    # 创建新的.mcfunction文件
    def new_main_function(self, func_name):
        pass

    # 创建新的帧
    def new_frame(self):
        pass

    # 修改指向的特效名称
    def set_effect_name(self, new_effect_name):
        self.effect_name = new_effect_name

    # 读取矩阵
    def read_mat(self, mat_file):
        """
        从相应的文件读取位置矩阵
        :param mat_file: 矩阵文件的位置
        :return:
            mat_array: 保存了整个矩阵的列表
        """
        mat_array = []
        with open(mat_file, "w+") as mat:
            mat_data = mat.readlines()
            for particles in mat_data:
                if len(particles) > 0 and particles[0] is not "#":
                    if len(particles.strip().split(',')) == 4:
                        mat_array.append(particles.strip().split(','))
            mat.close()
        return mat_array

# 创建过程：
# 首先添加新文件夹
# 然后添加functions文件夹
# 遍历矩阵列表，对每一个矩阵都视为一帧
# 然后添加新的function，这个新的function可能是单独的帧，也可能是别的function
# 最后写入相应的文件。
#