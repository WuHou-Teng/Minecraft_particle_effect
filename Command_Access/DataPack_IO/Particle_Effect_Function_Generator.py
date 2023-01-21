import os
# ok
from Command_Access.Command_Convertor.Homo_Convertor import HomoConverter
# TODO 尚未完成
from Command_Access.Command_Convertor.Color_Convertor import ColorConvertor
from Command_Access.Command_Generator.Executes.Execute_consts import *
from Command_Access.Command_Generator.Selector.Selector_Const import *
from Command_Access.Const import Particles_Java
from Command_Access.Const.Convertor_consts import *
# TODO 尚未完成
from Command_Access.DataPack_IO.Function_Writer import FunctionWriter
# TODO Layer 尚未完成
from Command_Access.Command_Generator.Executes.Execute_Builder import ExecuteBuilder
from Command_Access.Command_Generator.Executes.Execute_Layer_Box import ExecuteLayerBox
# ok
from Command_Access.Command_Generator.Entities.Entity_Box import EntityBox
# ok
from Command_Access.Command_Generator.Selector.Target_Selector_Box import TargetSelectorBox
# TODO ScoreBoardGenerator 尚未完成
from Command_Access.Command_Generator.Score_Board.ScoreBoard_Box import ScoreBoardBox

# ok
from Matrix_Access.Matrix_Accesser_Box import MatrixAccessBox
from Matrix_Access.Matrix_Accesser import MatrixAccesser
# ok
from Matrix_Access.Controllers.Controller_Box import ControllerBox
from Matrix_Access.Controllers.Controller_Applier import ControllerApplier
# TODO 尚未完成更细化的文件归类，但是能用
from Matrix_Access.Matrix_Writer import MatrixWriter


# TODO 图片到矩阵本身的转化尚未完成。


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
        :param new_effect_name: 新特效名字, 或者说新特效的命名空间
        """
        self.effect_name = new_effect_name
        # TODO 初始化两种转换器, 考虑直接删除转换器。
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
        self.matrix_access_box = MatrixAccessBox()

        # 初始化控制器盒子
        self.controller_box = ControllerBox()
        # 初始化控制器调用器
        self.controller_applier = ControllerApplier()
        # 初始化矩阵书写
        self.matrix_writer = MatrixWriter(None)

        # TODO 还有将图片转化为矩阵的工具需要初始化。

        # TODO 考虑直接将两个Convertor的内容移动到这里？毕竟将execute和 Controller独立后，Convertor就没剩下太多需要独立的功能了。
        self.edition = JAVA
        self.coo_type = [RELA_COORD, RELA_COORD, RELA_COORD]
        self.coo_dict = {RELA_COORD: " ~", FACE_COORD: " ^", ABS_COORD: " "}
        self.force_particle = None
        # 计时器设定
        self.use_timer = False  # 是否使用延时
        self.timer_type = CLOUD  # 可以是CLOUD=1, SCORE_BOARD=2 两种
        self.timer_count = 0    # 用来生成名字不同的timer
        # 特殊执行器设定
        # 注，计时器一定会用到特殊执行器，但是计时器使用的特殊执行器和此处是相互独立的。
        self.use_execute = True  # 是否使用特殊执行器，默认开启，否则会一命令方块为执行者。

    def switch_edition(self, edition):
        """
        设定生成的代码为Java版还是基岩版。（注，java版本目前默认1.18.2，基岩版尚未制作）
        :param edition: Java 版还是 BedRock版
        """
        self.edition = edition

    # 修改坐标相对性
    def set_coo_type(self, x_coo_type, y_coo_type=None, z_coo_type=None):
        """
        设定x，y，z轴上分别使用什么类型的坐标模式，包括：
        绝对坐标，ABS_COORD
        相对坐标，RELA_COORD
        面朝坐标，FACE_COORD
        :param x_coo_type: x轴坐标模式
        :param y_coo_type: y轴坐标模式
        :param z_coo_type: z轴坐标模式
        """
        if x_coo_type not in self.coo_dict.keys():
            x_coo_type = RELA_COORD
        if y_coo_type is None:
            y_coo_type = x_coo_type
        if z_coo_type is None:
            z_coo_type = x_coo_type
        self.coo_type = [x_coo_type, y_coo_type, z_coo_type]

    def static_particle_convertor(self, particle):
        """
        将粒子信息转化为静态粒子指令，只考虑粒子类型、坐标与扩散坐标，不考虑颜色、颜色转变和延时。
        对于相对坐标 ~x ~y ~z
        其中~x 是东+西-，~y是上+下-， ~z是南+北-
        对于实体视角坐标 ^x ^y ^z
        其中^x 是左+右-，^y是上+下-，^z则是前+后-。
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type, 延时(tick)
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined)   0

        :param particle: 单个粒子的所有信息
        :return:
            召唤单个粒子的指令
        """
        # 所有通过控制器对矩阵的修改，需要在转换前完成。
        # particle = self.controller_applier.apply_processing(particle)
        # 将particle列表中所有数据全部改为字符串。
        for i in range(len(particle)):
            if type(particle[i]) is float or type(particle[i]) is int:
                particle[i] = str(round(particle[i], 5))
        # 使用 ~ 还是 ^ 还是单纯的绝对坐标
        x_sign = self.coo_dict.get(self.coo_type[0])
        y_sign = self.coo_dict.get(self.coo_type[1])
        z_sign = self.coo_dict.get(self.coo_type[2])
        # force 还是 normal
        f_n = "force" if particle[8].strip() == "f" else "normal"

        particle_type = Particles_Java.particle_dict.get(particle[15]).strip()

        if self.edition is JAVA:
            coord_str = (x_sign + particle[0] + y_sign + particle[1] + z_sign + particle[2] +
                         " " + particle[3] + " " + particle[4] + " " + particle[5] + " " + particle[6] +
                         " " + particle[7] + " " + f_n)
            if self.force_particle is not None:
                return "particle " + self.force_particle + coord_str + "\n"
            else:
                return "particle " + particle_type + coord_str + "\n"
        else:
            # 基岩版的暂时搁置
            pass

    def color_particle_convertor(self, particle):
        """
        将粒子信息转化为静态粒子指令，虑粒子类型、坐标、扩散坐标与颜色。不考虑颜色转变和延时。
        :param particle: 单个粒子的所有信息
        :return:
            召唤单个粒子的指令
        """
        pass

    def color_transfer_particle_convertor(self, particle):
        """
        将粒子信息转化为静态粒子指令，虑粒子类型、坐标、扩散坐标、颜色、颜色转变。不考虑延时。
        :param particle: 单个粒子的所有信息
        :return:
            召唤单个粒子的指令
        """
        pass

    def mat_convertor(self, matrix_access, convertor_type=STATIC):
        """
        整个矩阵的转换器。可以调节粒子的转换类型。
        :param matrix_access: 矩阵访问器
        :param convertor_type: 粒子转换类型
        :return:
            经过转换的指令列表。
        """
        functions = []
        mat_list = matrix_access.get_mat_list()
        for particles in mat_list:
            if convertor_type is STATIC:
                order = self.static_particle_convertor(particles)
                functions.append(order)
            elif convertor_type is COLOR:
                order = self.color_particle_convertor(particles)
                functions.append(order)
            elif convertor_type is COLOR_TRANSFER:
                order = self.color_transfer_particle_convertor(particles)
                functions.append(order)
        return functions

    def generator(self, function_name, matrix_access, convertor_type=STATIC, timer_tag=None):
        """
        将一个矩阵转化为对应的 mc函数。
        该函数不会调用自定义的 Controller，所以任何需要对矩阵进行调整的过程，请调用另一个函数。
        该函数并没有提供设定 executeBuilder的途径，如果要自定义，请提前定义。
        :param function_name: 要保存到函数文件的文件名称，注意不要后缀，主要用于函数的循环。如果不循环，则用不到。
        :param matrix_access: 打开并保存了一个坐标矩阵的访问器
        :param convertor_type: 目前有：静态，颜色，颜色转换 三种可选。
        :param timer_tag: 自定义计时器tag
        :return:

        """
        # 将矩阵的基本指令转换好。
        functions = self.mat_convertor(matrix_access, convertor_type)

        mat_list = matrix_access.get_mat_list()

        # 计时处理
        timer = None
        if timer_tag is None:
            timer_tag = "default_timer_tag_" + str(self.timer_count)
        target_selector = None
        timer_layer = None

        # 如果使用计时器
        if self.use_timer:
            self.use_execute = True
            # 对于单个粒子的转换，如果使用计时器，则总是保证延时为绝对计时。
            # 所以总是先转换为绝对计时模式。
            controller_applier = ControllerApplier()
            controller_applier.add_controller_to_apply_list(
                self.controller_box.new_delay_type_switch_controller()
            )

            if self.timer_type == CLOUD:
                # 创建timer
                timer = self.entity_box.new_cloud_timer(
                    index_name="default_timer_" + str(self.timer_count),
                    tag=timer_tag,
                    age=0,
                    duration=matrix_access.max_delay
                )
                # 创建selector_target
                target_selector = self.selector_box.new_target_selector(
                    index_name=None,
                    entity_mark=NEAREST_PLAYER,
                    entity=timer
                )
                # 创建对应的execute_layer
                timer_layer = self.execute_layer_box.new_layer(
                    index_name=None,
                    modify=AS,
                    selector=target_selector
                )
                self.timer_count += 1
                # 将layer添加到对应的Builder中
                self.execute_builder.add_layer(timer_layer)

                for i in range(len(mat_list)):
                    timer.set_age_ticks(mat_list[i][16])
                    execute_part = self.execute_builder.to_string()
                    functions[i] = execute_part + functions[i]

                # 完成遍历后，还要在function结尾添加一个循环语句
                # 此时，Age不再被需要，直接设定为None
                timer.Age = None
                timer.update_self_value()   # 更新数据字典
                execute_part = self.execute_builder.to_string()     # 由于timer实体的Age已经被设定为None，因此，不会被写入字符串。
                loop_sentence = execute_part + "function " + self.effect_name + ":" + function_name
                functions.append(loop_sentence)
                # 完成后再把Age加回去
                timer.Age = 0
                timer.update_self_value()

            elif self.timer_type is SCORE_BOARD:
                # TODO 计分板模式尚未完成。
                pass

        # 不使用计时器
        else:
            # 但使用execute
            if self.use_execute:
                # 如果使用execute，但是忘记加目标，则自动添加以最近玩家身份发动的execute
                if len(self.execute_builder.layer) == 0:
                    self.execute_builder.add_layer(
                        self.execute_layer_box.new_layer()
                    )
                for i in range(len(mat_list)):
                    # timer.set_age_ticks(mat_list[i][16])
                    execute_part = self.execute_builder.to_string()
                    functions[i] = execute_part + functions[i]

            # execute也不用的话，就是原模原样的 functions

        # TODO 接下来是创建文件并写入。

    def open_new_matrix(self, matrix_file_address) -> MatrixAccesser:
        """
        创建一个新的矩阵访问器，将其添加到矩阵访问器盒子，并返回。
        :param matrix_file_address: 矩阵文件的完整路径，如果文件并非完整路径，则考虑从默认矩阵文件夹寻找。
        :return:
            new_matrix_accesser: 新的矩阵访问器。
        """
        return self.matrix_access_box.new_matrix_accesser(matrix_file_address)

    def summon_entity(self, entity, x=None, y=None, z=None, x_coo_type=RELA_COORD, y_coo_type=None, z_coo_type=None):
        """
        创建 summon 指令，一般用于作为粒子特效实体载体。
        :param entity: 创建好的实体
        :param x: x方向位置
        :param y: y方向位置
        :param z: z方向位置
        :param x_coo_type: x轴坐标模式
        :param y_coo_type: y轴坐标模式
        :param z_coo_type: z轴坐标模式
        :return:
        """
        if y_coo_type is None:
            y_coo_type = x_coo_type
        if z_coo_type is None:
            z_coo_type = x_coo_type
        x_sign = self.coo_dict.get(x_coo_type)
        y_sign = self.coo_dict.get(y_coo_type)
        z_sign = self.coo_dict.get(z_coo_type)
        nbt, entity_type, pos = entity.to_string_summon_nbt
        if x is None:
            x = pos[0]
        if y is None:
            y = pos[1]
        if z is None:
            z = pos[2]
        return f'summon {entity_type} {x_sign}{x} {y_sign}{y} {z_sign}{z} {nbt}'




# 测试
if __name__ == "__main__":
    datapack_address = ("C:\\Wuhou\\play\\minecraft\\1.18.2KuaYueII\\1.18.2KuaYueII\\.minecraft"
                        "\\saves\\新的世界 (1)\\datapacks\\partical_effect")
    new_function_name = "NewYear"
    pe_function_generator = PEFuncGenerator(datapack_address, new_function_name)






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
