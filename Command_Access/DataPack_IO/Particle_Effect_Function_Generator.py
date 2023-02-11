import copy
import os
from Command_Access.Command_Generator.Entities.Area_Effect_Cloud import CloudTimer

from Command_Access.Command_Generator.Executes.Execute_consts import *
from Command_Access.Command_Generator.Score_Board.ScoreBoard_Generator import ScoreBoard
from Command_Access.Command_Generator.Selector.Selector_Const import *
from Command_Access.Const import Particles_Java
from Command_Access.Const import Particles_x_fabric
from Command_Access.Const.Convertor_consts import *
# ok
from Command_Access.DataPack_IO.Function_Writer import FunctionWriter
# TODO Layer if, unless尚未完成
from Command_Access.Command_Generator.Executes.Execute_Builder import ExecuteBuilder
from Command_Access.Command_Generator.Executes.Execute_Layer_Box import ExecuteLayerBox
# ok
from Command_Access.Command_Generator.Entities.Entity_Box import EntityBox
# ok
from Command_Access.Command_Generator.Selector.Target_Selector_Box import TargetSelectorBox
from Command_Access.Command_Generator.Selector.Selector_Tags import ScoresTag
# TODO ScoreBoardGenerator 尚未完成
from Command_Access.Command_Generator.Score_Board.ScoreBoard_Box import ScoreBoardBox

# ok
from Matrix_Access.Matrix_Accesser_Box import MatrixAccessBox
from Matrix_Access.Matrix_Accesser import *
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
        # self.coo_dict = {RELA_COORD: "~", FACE_COORD: "^", ABS_COORD: ""}
        self.force_particle = None
        # 计时器设定
        self.use_timer = False  # 是否使用延时
        self.timer_type = CLOUD  # 可以是CLOUD=1, SCORE_BOARD=2 两种
        self.timer_count = 0  # 用来生成名字不同的timer
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
        if x_coo_type not in COO_DICT.keys():
            x_coo_type = RELA_COORD
        if y_coo_type is None:
            y_coo_type = x_coo_type
        if z_coo_type is None:
            z_coo_type = x_coo_type
        self.coo_type = [x_coo_type, y_coo_type, z_coo_type]

    def set_force_particle(self, particle_type):
        """
        # 设定全局的强制粒子类型
        :param particle_type: 粒子的编号，详见:
            Command_Access.Const.Particles_Java, Command_Access.Const.Particles_x_fabric
        """
        self.force_particle = particle_type

    def clear_force_particle(self):
        self.force_particle = None

    def set_auto_timer_type(self, timer_type):
        self.timer_type = timer_type

    def execute_switch(self, t_f):
        """
        开启或关闭execute使用。
        :param t_f: True or False
        :return:
        """
        self.use_execute = t_f

    def transfer_matrix_delay_to_absolute(self, matrix_accesser):
        assert type(matrix_accesser) is MatrixAccesser
        if matrix_accesser.delay_type == ABSOLUTE:
            pass
        else:
            temp_applier = ControllerApplier()
            temp_applier.add_controller_to_apply_list(
                self.controller_box.new_delay_type_switch_controller(
                    index_name="delay_temp",
                )
            )
            temp_applier.apply_whole_matrix(matrix_accesser)

    def normal_particle_convertor(self, particle):
        # TODO 标准格式更新
        """
        将粒子信息转化为静态粒子指令，只考虑下面列出的基本参数和附加参数，
        不考虑额外参数和 mod参数。

        # 基本参数
          x, y, z, particle_type,
          1, 1, 1, 0(Undefined),
        # 附加参数
          d_x, d_y, d_z, speed, count, force_normal,
          0,   0,   0,   0,     1,     f/n,
        # 额外参数
          Color(R, G, B),   color_transfer(R,G,B), 粒子大小,
          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      1,
        # mod参数
          持续时间(tick), 粒子透明度, 延时(tick)
          80,           1,        0

        对于相对坐标 ~x ~y ~z
        其中~x 是东+西-，~y是上+下-， ~z是南+北-
        对于实体视角坐标 ^x ^y ^z
        其中^x 是左+右-，^y是上+下-，^z则是前+后-。

        :param particle: 单个粒子的所有信息
        :return:
            召唤单个粒子的指令
        """
        # 所有通过控制器对矩阵的修改，需要在转换前完成。
        # particle = self.controller_applier.apply_processing(particle)
        # 提取粒子中所有信息
        assert type(particle) is MCParticle

        # force 还是 normal
        f_n = "force" if particle.f_n.strip() == "f" else "normal"

        particle_type = (Particles_Java.particle_dict.get(particle.particle_type).strip()
                         if self.force_particle is None
                         else Particles_Java.particle_dict.get(self.force_particle).strip())

        if self.edition is JAVA:
            # TODO viewer 选择器暂时默认为 @a
            return (f'particle {particle_type} '
                    f'{COO_DICT.get(self.coo_type[0])}{round(particle.x, 4)} '
                    f'{COO_DICT.get(self.coo_type[1])}{round(particle.y, 4)} '
                    f'{COO_DICT.get(self.coo_type[2])}{round(particle.z, 4)} '
                    f'{round(particle.dx, 4)} {round(particle.dy, 4)} {round(particle.dz, 4)} '
                    f'{round(particle.speed, 4)} {particle.count} {f_n} @a\n')

        else:
            # 基岩版的暂时搁置
            pass

    def dust_particle_convertor(self, particle):
        """
        将粒子信息转化为静态粒子指令，只考虑下面列出的基本参数，附加参数，额外参数，
        不考虑 mod参数。

        # 基本参数
          x, y, z, particle_type,
          1, 1, 1, 0(Undefined),
        # 附加参数
          d_x, d_y, d_z, speed, count, force_normal,
          0,   0,   0,   0,     1,     f/n,
        # 额外参数
          Color(R, G, B),   color_transfer(R,G,B), 粒子大小,
          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      1,
        # mod参数
          持续时间(tick), 粒子透明度, 延时(tick)
          80,           1,        0

        :param particle: MCParticle 实例
        :return:
            召唤单个粒子的指令
        """
        assert type(particle) is MCParticle

        # force 还是 normal
        f_n = "force" if particle.f_n.strip() == "f" else "normal"

        # 解析
        particle_type = (Particles_Java.particle_dict.get(particle.particle_type).strip()
                         if self.force_particle is None
                         else Particles_Java.particle_dict.get(self.force_particle).strip())

        if self.edition is JAVA:
            # TODO viewer 选择器暂时默认为 @a
            return (
                f'particle {particle_type} '
                f'{round(particle.r, 3)} {round(particle.g, 3)} {round(particle.b, 3)} '
                f'{round(particle.size, 3)} '
                f'{COO_DICT.get(self.coo_type[0])}{round(particle.x, 4)} '
                f'{COO_DICT.get(self.coo_type[1])}{round(particle.y, 4)} '
                f'{COO_DICT.get(self.coo_type[2])}{round(particle.z, 4)} '
                f'{round(particle.dx, 4)} '
                f'{round(particle.dy, 4)} '
                f'{round(particle.dz, 4)} '
                f'{round(particle.speed, 4)} {particle.count} {f_n} @a\n')

        else:
            # 基岩版的暂时搁置
            pass

    def dust_color_transfer_particle_convertor(self, particle):
        """
        将粒子信息转化为静态粒子指令，只考虑下面列出的基本参数，附加参数，额外参数，
        不考虑 mod参数。

        # 基本参数
          x, y, z, particle_type,
          1, 1, 1, 0(Undefined),
        # 附加参数
          d_x, d_y, d_z, speed, count, force_normal,
          0,   0,   0,   0,     1,     f/n,
        # 额外参数
          Color(R, G, B),   color_transfer(R,G,B), 粒子大小,
          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      1,
        # mod参数
          持续时间(tick), 粒子透明度, 延时(tick)
          80,           1,        0

        :param particle: MCParticle 实例
        :return:
            召唤单个粒子的指令
        """
        assert type(particle) is MCParticle

        # force 还是 normal
        f_n = "force" if particle.f_n.strip() == "f" else "normal"

        particle_type = (Particles_Java.particle_dict.get(particle.particle_type).strip()
                         if self.force_particle is None
                         else Particles_Java.particle_dict.get(self.force_particle).strip())

        if self.edition is JAVA:
            # TODO viewer 选择器暂时默认为 @a
            return (
                f'particle {particle_type} '
                f'{round(particle.r, 3)} '
                f'{round(particle.g, 3)} '
                f'{round(particle.b, 3)} '
                f'{round(particle.size, 4)} '
                f'{round(particle.rt, 3)} '
                f'{round(particle.gt, 3)} '
                f'{round(particle.bt, 3)} '
                f'{COO_DICT.get(self.coo_type[0])}{round(particle.x, 4)} '
                f'{COO_DICT.get(self.coo_type[1])}{round(particle.y, 4)} '
                f'{COO_DICT.get(self.coo_type[2])}{round(particle.z, 4)} '
                f'{round(particle.dx, 4)} '
                f'{round(particle.dy, 4)} '
                f'{round(particle.dz, 4)} '
                f'{round(particle.speed, 4)} {particle.count} {f_n} @a\n')

        else:
            # 基岩版的暂时搁置
            pass

    def particlex_convertor(self, particle, treat_as_normal=False):
        """
        将粒子信息转化为静态粒子指令，除了延时外，考虑所有参数。

        # 基本参数
          x, y, z, particle_type,
          1, 1, 1, 0(Undefined),
        # 附加参数
          d_x, d_y, d_z, speed, count, force_normal,
          0,   0,   0,   0,     1,     f/n,
        # 额外参数
          Color(R, G, B),   color_transfer(R,G,B), 粒子大小,
          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      1,
        # mod参数
          持续时间(tick), 粒子透明度, 延时(tick)
          80,           1,        0

        :param treat_as_normal: 是否将mod粒子视作普通粒子来处理延时。
        :param particle: MCParticle 实例
        :return:
        """
        assert type(particle) is MCParticle
        # particle = MCParticle(0, 0, 0)
        # 将particle列表中所有数据全部改为字符串。
        # x = str(round(particle.x, 3))
        # y = str(round(particle.y, 3))
        # z = str(round(particle.z, 3))

        # dx = str(round(particle.dx, 3))
        # dy = str(round(particle.dy, 3))
        # dz = str(round(particle.dz, 3))
        # time_on_moving = str(round(particle.speed, 3))
        # count = str(particle.count)

        # r = str(round(particle.r, 3))
        # g = str(round(particle.g, 3))
        # b = str(round(particle.b, 3))
        # rt = str(round(particle.rt, 3))
        # gt = str(round(particle.gt, 3))
        # bt = str(round(particle.bt, 3))

        # size = str(round(particle.size, 3))
        # duration = str(particle.duration)
        # transparency = str(round(particle.transparency, 3))
        # f_n = particle.f_n

        # 使用 ~ 还是 ^ 还是单纯的绝对坐标
        # x_sign = COO_DICT.get(self.coo_type[0])
        # y_sign = COO_DICT.get(self.coo_type[1])
        # z_sign = COO_DICT.get(self.coo_type[2])

        # force 还是 normal
        f_n = "force" if particle.f_n.strip() == "f" else "normal"

        particle_type = (Particles_x_fabric.particlex_dict.get(particle.particle_type).strip()
                         if self.force_particle is None
                         else Particles_x_fabric.particlex_dict.get(self.force_particle).strip())

        if self.edition is JAVA:
            # /particlex <粒子名> <颜色> *<渐变颜色>
            # <坐标> <向量> <行完全程所需时间> <数量> Force/Normal
            # <存在时间> <透明度> <大小缩放> <可以看到粒子效果的玩家>
            # TODO viewer 选择器暂时默认为 @a
            if not treat_as_normal:
                return (
                    f'particlex {particle_type} '
                    f'{round(particle.r, 3)} '
                    f'{round(particle.g, 3)} '
                    f'{round(particle.b, 3)} '
                    f'{round(particle.rt, 3)} '
                    f'{round(particle.gt, 3)} '
                    f'{round(particle.bt, 3)} '
                    f'{COO_DICT.get(self.coo_type[0])}{round(particle.x, 4)} '
                    f'{COO_DICT.get(self.coo_type[1])}{round(particle.y, 4)} '
                    f'{COO_DICT.get(self.coo_type[2])}{round(particle.z, 4)} '
                    f'{round(particle.dx, 4)} '
                    f'{round(particle.dy, 4)} '
                    f'{round(particle.dz, 4)} '
                    f'{round(particle.speed, 4)} {particle.count} {f_n} '
                    f'{particle.duration} {round(particle.transparency, 3)} {round(particle.size, 4)} @a '
                    f'{particle.delay} {particle.color_delay}\n')
            else:
                return (
                    f'particlex {particle_type} '
                    f'{round(particle.r, 3)} '
                    f'{round(particle.g, 3)} '
                    f'{round(particle.b, 3)} '
                    f'{round(particle.rt, 3)} '
                    f'{round(particle.gt, 3)} '
                    f'{round(particle.bt, 3)} '
                    f'{COO_DICT.get(self.coo_type[0])}{round(particle.x, 4)} '
                    f'{COO_DICT.get(self.coo_type[1])}{round(particle.y, 4)} '
                    f'{COO_DICT.get(self.coo_type[2])}{round(particle.z, 4)} '
                    f'{round(particle.dx, 4)} '
                    f'{round(particle.dy, 4)} '
                    f'{round(particle.dz, 4)} '
                    f'{round(particle.speed, 4)} {particle.count} {f_n} '
                    f'{particle.duration} {round(particle.transparency, 3)} {round(particle.size, 4)} @a '
                    f'0 {particle.color_delay}\n')

        else:
            # 基岩版的暂时搁置
            pass

    def mat_convertor(self, matrix_access, treat_mod_particle_as_normal=False):
        """
        整个矩阵的转换器。可以调节粒子的转换类型。
        :param matrix_access: 矩阵访问器
        :param treat_mod_particle_as_normal: 是否将mod粒子视为普通粒子处理，此项主要关乎后期的延时方式。
            mod粒子自带延时功能，而普通粒子并没有。因此mod粒子不需要要构建延时模块结构，使用mod粒子自带的延时功能会有更好的性能。
        :return:
            经过转换的指令列表。
        """
        mc_functions = []
        mat_list = matrix_access.get_mat_list()
        # TODO 根据粒子类型调用不同的函数
        for particles in mat_list:
            assert type(particles) is MCParticle
            particle_type = particles.particle_type
            # 如果强制粒子类型不为None，则将粒子类型定义为输入的强制粒子类型。
            if self.force_particle is not None:
                assert type(self.force_particle) is int
                particle_type = self.force_particle
            # 普通粒子
            # /particle <name> <pos> <delta> <speed> <count> [force|normal] [<viewer>]
            if particle_type < 100:
                order = self.normal_particle_convertor(particles)
                mc_functions.append(order)
            # dust粒子
            # /particle <name> <Color> <size> <pos> <delta> <speed> <count> [force|normal] [<viewer>]
            elif particle_type is Particles_Java.dust:
                order = self.dust_particle_convertor(particles)
                mc_functions.append(order)
            # dust_color_transition 粒子
            # /particle <name> <Color> <size> <> <pos> <delta> <speed> <count> [force|normal] [<viewer>]
            elif particle_type is Particles_Java.dust_color_transition:
                order = self.dust_color_transfer_particle_convertor(particles)
                mc_functions.append(order)
            # mod 粒子
            # /particlex <Particle_Name> <Color> *<Target_Color> <Pos> <Delta_Pos> <Speed> <Count> Force/Normal
            # <Time> <Alpha> <Scale> <Viewers>
            elif particle_type > 1000:
                if treat_mod_particle_as_normal:

                    order = self.particlex_convertor(particles, treat_mod_particle_as_normal)
                else:
                    order = self.particlex_convertor(particles)
                mc_functions.append(order)
        return mc_functions

    def generator(self, function_name, matrix_access, function_override=False, customer_execute_command=None,
                  timer_execute_layer=None, timer_selector=None,  timer_entity=None,
                  timer_tag=None):
        """
        将一个矩阵转化为对应的 mc函数文件。
        * 用户可以自己带入自己创建的 ExecuteLayer timer_execute_layer 用来生成相应的 计时execute语句。
        * 亦或者带入自己创建的 Selector timer_selector，
            程序会自动创建一个 ExecuteLayer timer_execute_layer, 接着生成计时execute语句。
        * 再或者带入自己建立的 CloudTimer / ScoreboardTimer timer_entity.
            程序会将其放入对应的 Selector timer_selector，
            再创建一个 ExecuteLayer timer_execute_layer, 接着生成计时execute语句。
        * 最后，可以只提供 str timer_tag 或者一切留空，所有的计时器实体，选择器，execute_layer均交给程序自动创建

        注意，该函数自动创建的任何 Entity, Selector, ExecuteLayer 都不会被加入相应的存储列表。

        该函数不会调用自定义的 Controller，所以任何需要对矩阵进行调整的过程，请调用另一个函数。
        该函数并没有提供设定 executeBuilder的途径，如果要自定义，请提前定义。

        :param function_name: 要保存到函数文件的文件名称，注意不要后缀，主要用于函数的循环。如果不循环，则用不到。
        :param matrix_access: 打开并保存了一个坐标矩阵的访问器
        :param function_override: 是否覆盖原有的函数。
        :param customer_execute_command: 用户自定义的 execute 指令。例如："execute as @p run", 程序会将其自动加到所有指令的开头。
                                         该参数只有当self.execute 为True时才会被采用

        :param timer_execute_layer: 必须为包含了 timer_entity 的 timer_selector 的 ExecuteLayer。如果该参数不为None，则不再考虑后三个参数。
        :param timer_selector: 必须为包含了 timer_entity 的 Selector。如果该参数不为None，则不再考虑后两个参数。
        :param timer_entity: 必须为计时器实体。如果该参数不为None，则不再考虑 timer_tag参数。
        :param timer_tag: 自定义计时器tag，只有当前面三个参数全部为 None时采用。

        :return:

        """
        # 将矩阵的基本指令转换好。
        if self.force_particle > 1000:
            print("<Warn> 使用mod粒子推荐使用generator_mod_particle以获得更好的性能")
        functions = self.mat_convertor(matrix_access)

        mat_list = matrix_access.get_mat_list()

        # 如果使用计时器
        if self.use_timer:
            # 使用计时器，则一定启用execute指令
            # self.use_execute = True
            # 清空execute_builder做好准备
            self.execute_builder.clear_layer()
            # 再创建一个score_tag
            score_tag = None
            # 如果输入的矩阵采用相对计时，则先转化为绝对计时
            self.transfer_matrix_delay_to_absolute(matrix_access)

            if timer_execute_layer is not None or timer_selector is not None:
                # 任意一个不为None时，考虑从中提取timer_entity，而非创建新的。
                timer_selector = timer_execute_layer.get_selector()
                # 获取存放在Selector中的entity，
                timer_entity = timer_selector.get_entity()
                # 如果这里是scoreboard，那么entity是None，接下来就到计分板控制部分。
                score_tag = None
                if timer_entity is None:
                    # 可能是计分板
                    for tags in timer_selector.get_selector_list():
                        if type(tags) is ScoresTag:
                            score_tag = tags
                            # TODO 这里直接默认积分Tag中保存的所有积分项的第一个, 写死了，不太好，但是没什么太好的办法。
                            # 如果用户真的丧心病狂的往ScoreTag里头赛不止一个计分项，那我摆了。
                            timer_entity = ScoreBoard(
                                index_name=score_tag.score_info_list[0][0],
                            )
                    # 经过循环后发现没有计分板，那就根据全局计时器类别创建。
                    if score_tag is None:
                        if self.timer_type == CLOUD:
                            # 创建timer
                            timer_entity = self.entity_box.new_cloud_timer(
                                index_name="default_timer_" + str(self.timer_count),
                                tag=timer_tag,
                                age=0,
                                # 记得计时器实际延时是粒子延时记录的1/5
                                duration=int(matrix_access.max_delay/5)
                            )
                            timer_selector.set_entity(timer_entity)
                        elif self.timer_type == SCOREBOARD:
                            timer_entity = ScoreBoard(
                                index_name="default_timer_" + str(self.timer_count)
                            )
                            score_tag = ScoresTag().add_score(timer_entity.index_name)
                            timer_selector.add_tag(score_tag)
                if timer_execute_layer is None:
                    # 创建对应的execute_layer
                    timer_execute_layer = self.execute_layer_box.new_layer(
                        index_name=None,
                        modify=AS,
                        selector=timer_selector
                    )

            elif timer_entity is not None:
                # timer_entity 不为空，则只需要创建新的selector和layer，将相应数据放进去即可。
                # 创建selector_target
                if type(timer_entity) is CloudTimer:
                    timer_selector = self.selector_box.new_target_selector(
                        index_name=None,
                        entity_mark=ALL_ENTITY,
                        entity=timer_entity
                    )

                elif type(timer_entity) is ScoreBoard:
                    timer_selector = self.selector_box.new_target_selector(
                        index_name=None,
                        entity_mark=ALL_ENTITY,
                        entity=None
                    )
                    score_tag = ScoresTag().add_score(timer_entity.index_name)
                    timer_selector.add_tag(score_tag)

                # 创建对应的execute_layer
                timer_execute_layer = self.execute_layer_box.new_layer(
                    index_name=None,
                    modify=AS,
                    selector=timer_selector
                )
            else:
                # 上述者皆未提供，于是全部自动生成。
                if timer_tag is None:
                    timer_tag = "default_timer_tag_" + str(self.timer_count)
                # 此时计时器类型根据全局计时器类型 self.timer_type 设定
                if self.timer_type == CLOUD:
                    # 创建timer
                    timer_entity = self.entity_box.new_cloud_timer(
                        index_name="default_timer_" + str(self.timer_count),
                        tag=timer_tag,
                        age=0,
                        # 记得计时器实际延时是粒子延时记录的1/5
                        duration=int(matrix_access.max_delay / 5)
                    )
                    # 创建selector_target
                    timer_selector = self.selector_box.new_target_selector(
                        index_name=None,
                        entity_mark=ALL_ENTITY,
                        entity=timer_entity
                    )

                if self.timer_type == SCOREBOARD:
                    # TODO 完善scoreboard 计时器，并作修改。
                    timer_entity = self.scoreboard_box.new_scoreboard(
                        name="default_timer_" + str(self.timer_count),
                    )
                    # 不同于Cloud，scoreboard不是实体，而是选择器内置的一个tag
                    timer_selector = self.selector_box.new_target_selector(
                        index_name=None,
                        entity_mark=ALL_ENTITY,
                        entity=None
                    )
                    timer_selector.add_tag(timer_selector.score(timer_entity.index_name))

                # 创建对应的execute_layer
                timer_execute_layer = self.execute_layer_box.new_layer(
                    index_name=None,
                    modify=AS,
                    selector=timer_selector
                )
                # 由于是自动新建的计时器，所以默认计时器数量+1，用于和之前的计时器名称作区分。
                self.timer_count += 1

            # 将layer添加到对应的Builder中
            self.execute_builder.add_layer(timer_execute_layer)

            # 为了保证在轮询时的定位，统一添加一个 "at @s"
            self.execute_builder.add_layer(
                self.execute_layer_box.new_layer(
                    index_name="temp_local",
                    modify=AT,
                    selector=self.selector_box.new_target_selector(None, CURRENT_ENTITY)
                )
            )

            # 完成基础环境的搭建，开始生成对应的函数
            # 首先区分Cloud 和 scoreboard
            if type(timer_entity) is ScoreBoard:
                for particle_index in range(len(mat_list)):
                    particle = mat_list[particle_index]
                    # 将粒子对应的延时更新到计分板的score_tag
                    # 记得计时器实际延时是粒子延时记录的1/5
                    score_tag.score_info_list[0][2] = int(particle.delay/5)
                    # 将计时器execute添加到function的前面。
                    functions[particle_index] = self.execute_builder.to_string() + functions[particle_index]
                # 添加结构性循环语句让函数只需一次调用就可以完成延时循环。
                # TODO 计分板尚未完善，此处暂时不添加。以及，上面是否可以直接 self.execute_builder.to_string()并不确定

            elif type(timer_entity) is CloudTimer:

                for particle_index in range(len(mat_list)):
                    particle = mat_list[particle_index]
                    # 修改计时器时刻
                    # 记得计时器实际延时是粒子延时记录的1/5
                    timer_entity.set_age_ticks(int(particle.delay/5))
                    # 将计时器execute添加到function的前面。
                    functions[particle_index] = self.execute_builder.to_string() + functions[particle_index]

                # 添加结构性循环语句让函数只需一次调用就可以完成延时循环。
                # 完成遍历后，还要在function结尾添加一个循环语句
                # 此时，Age不再被需要，直接设定为None
                timer_entity.Age = None
                timer_entity.update_self_value()  # 更新数据字典

                execute_part = self.execute_builder.to_string()  # 由于timer实体的Age已经被设定为None，因此，不会被写入字符串。
                loop_sentence = execute_part + "schedule function " + self.effect_name + ":" + function_name + " 1t"

                functions.append(loop_sentence)
                # 完成后再把Age加回去
                timer_entity.Age = 0
                timer_entity.update_self_value()

        # 不使用计时器但使用execute
        if self.use_execute and not self.use_timer:
            if customer_execute_command is not None and type(customer_execute_command) is str:
                execute_part = customer_execute_command.strip() + " "
            else:
                # 如果使用execute，但是忘记加目标，则自动添加以最近玩家身份发动的execute
                if len(self.execute_builder.layer) == 0:
                    self.execute_builder.add_layer(
                        self.execute_layer_box.new_layer(
                            selector=self.selector_box.new_target_selector(
                                entity_mark=NEAREST_PLAYER
                            )
                        )
                    )
                execute_part = self.execute_builder.to_string()
            for i in range(len(mat_list)):
                # timer.set_age_ticks(mat_list[i][16])
                # execute_part = self.execute_builder.to_string()
                functions[i] = execute_part + functions[i]

        # 在使用过execute_builder后，记得清空
        self.execute_builder.clear_layer()
        # execute也不用的话，就是原模原样的 functions

        # TODO 接下来是创建文件并写入。
        if function_override:
            self.function_writer.write_func(function_name, functions)
        else:
            self.function_writer.add_func(function_name, functions)
        if self.use_timer:
            self.timer_launcher_generator(function_name, timer_entity)

    def timer_launcher_generator(self, function_name, timer):
        """
        当采用计时器时，新建立一个函数用于初始化计时环境。
        :param function_name: 要启动的函数名称
        :param timer: 计时器实例（无论scoreboard还是效果云，语法一致。
        :return:
        """
        launcher_function_name = function_name + "_launcher"
        # TODO scoreboard 的 summon_self尚未完善。
        functions = [timer.summon_self(), f'function {self.effect_name}:{function_name}\n']
        self.function_writer.write_func(launcher_function_name, functions)

    def generator_mod_particle(self, function_name, matrix_access, function_override=False,
                               customer_execute_command=None):
        """
        与 generator 函数类似，但是该函数专门为mod粒子提供更高性能的指令形式。

        :param function_name: 要保存到函数文件的文件名称，注意不要后缀，主要用于函数的循环。如果不循环，则用不到。
        :param matrix_access: 打开并保存了一个坐标矩阵的访问器
        :param function_override: 是否覆盖原有的函数。
        :param customer_execute_command: 用户自定义的 execute 指令。例如："execute as @p run", 程序会将其自动加到所有指令的开头。
                                         该参数只有当self.execute 为True时才会被采用

        :return:

        """
        # 将矩阵的基本指令转换好。
        functions = self.mat_convertor(matrix_access)

        mat_list = matrix_access.get_mat_list()

        # mod 粒子无需构建计时器结构。

        # 不使用计时器但使用execute
        if self.use_execute and not self.use_timer:
            if customer_execute_command is not None and type(customer_execute_command) is str:
                execute_part = customer_execute_command.strip() + " "
            else:
                # 如果使用execute，但是忘记加目标，则自动添加以最近玩家身份发动的execute
                if len(self.execute_builder.layer) == 0:
                    self.execute_builder.add_layer(
                        self.execute_layer_box.new_layer(
                            selector=self.selector_box.new_target_selector(
                                entity_mark=NEAREST_PLAYER
                            )
                        )
                    )
                execute_part = self.execute_builder.to_string()
            for i in range(len(mat_list)):
                # timer.set_age_ticks(mat_list[i][16])
                # execute_part = self.execute_builder.to_string()
                functions[i] = execute_part + functions[i]

        # 在使用过execute_builder后，记得清空
        self.execute_builder.clear_layer()
        # execute也不用的话，就是原模原样的 functions

        # TODO 接下来是创建文件并写入。
        if function_override:
            self.function_writer.write_func(function_name, functions)
        else:
            self.function_writer.add_func(function_name, functions)

    def apply_controller_processing_and_save(self, matrix_access, new_mat_file_address=None,
                                             override=False, override_original_accesser=False) -> str:
        """
        调用控制器过程，并保存到新的矩阵文件。
        注意，该方法返回的是新矩阵文件的绝对路径地址而非新的矩阵访问器实例。

        :param matrix_access: 包含要处理的矩阵的矩阵访问器
        :param new_mat_file_address: 完成处理后的矩阵的文件保存目标，如果不提供则将新数据加到原矩阵文件末尾。
        :param override: 是否覆盖目标文件，默认不覆盖，会依次往后写。
        :param override_original_accesser: 是否同时用新的数据替换原本的矩阵访问器中保存的数据，注意，无论True or False，都不会对原有的矩阵文件本身改动。
        :return:
            完成处理后的矩阵的文件保存目标地址
        """
        matrix = []
        if new_mat_file_address is None:
            # 如果未提供新的矩阵名称，则直接采用原有的矩阵文件。
            new_mat_file_address = matrix_access.mat_file
            # 本就是自己写给自己，就没必要重新写一遍了。
            # override_original_accesser = False
        if self.controller_applier.has_controllers():
            for particles in matrix_access.get_mat_list():
                result = self.controller_applier.apply_processing(particles)
                if result is not None:
                    matrix.append(result)
            if new_mat_file_address != matrix_access.mat_file:
                if not override:
                    new_mat_file_address = self.matrix_writer.add_to_matrix_file(matrix, new_mat_file_address)
                else:
                    new_mat_file_address = self.matrix_writer.renew_matrix_file(matrix, new_mat_file_address)
            if override_original_accesser:
                matrix_access.renew_mat_list(matrix, False)
        return new_mat_file_address

    def apply_controller_processing_matrix_and_save(self, matrix_access, new_mat_file_address=None,
                                                    override=False, override_original_accesser=False) -> str:
        """
        与 apply_controller_processing_and_save 类似，不同的是，该方法调用控制器会要求部分控制器自动更新某些因矩阵变化产生的参数变化。
        :param matrix_access: 包含要处理的矩阵的矩阵访问器
        :param new_mat_file_address: 完成处理后的矩阵的文件保存目标，如果不提供则将新数据加到原矩阵文件末尾。
        :param override: 是否覆盖目标文件，默认不覆盖，会依次往后写。如果未提供 new_mat_file_address，则会向原矩阵文件修改，或添加新的粒子信息。
        :param override_original_accesser: 是否同时用新的数据替换原本的矩阵访问器中保存的数据，注意，此参数无论True or False，都不会对原有的矩阵文件本身改动。
        :return:
            完成处理后的矩阵的文件保存目标地址
        """

        if new_mat_file_address is None:
            # 如果未提供新的矩阵名称，则直接采用原有的矩阵文件。
            new_mat_file_address = matrix_access.mat_file

        if self.controller_applier.has_controllers():
            new_matrix = self.controller_applier.apply_whole_matrix(copy.deepcopy(matrix_access))
            if new_mat_file_address != matrix_access.mat_file:
                if not override:
                    new_mat_file_address = self.matrix_writer.add_to_matrix_file(new_matrix.mat_list, new_mat_file_address)
                else:
                    new_mat_file_address = self.matrix_writer.renew_matrix_file(new_matrix.mat_list, new_mat_file_address)
            if override_original_accesser:
                matrix_access.renew_mat_list(new_matrix.mat_list, False)
        return new_mat_file_address

    def apply_controller_processing(self, matrix_access) -> list:
        """
        直接将控制器对矩阵访问器数据的修改结果返回。
        :param matrix_access: MatrixAccesser 实例
        :return:
            matrix: 装有经过控制器修该的粒子的列表。
        """
        matrix = []
        if self.controller_applier.has_controllers():
            for particles in matrix_access.get_mat_list():
                result = self.controller_applier.apply_processing(particles)
                if result is not None:
                    matrix.append(result)
        return matrix

    def apply_controller_processing_matrix(self, matrix_access) -> MatrixAccesser:
        """
        与 apply_controller_processing 类似，不同的是，该方法调用控制器会要求部分控制器自动更新某些因矩阵变化产生的参数变化。
        例如，旋转算法所需要的旋转中心坐标。
        :param matrix_access: MatrixAccesser 实例
        :return:
            matrix: 装有经过控制器修该的粒子的列表。
        """
        new_matrix_accesser = None
        if self.controller_applier.has_controllers():
            new_matrix_accesser = self.controller_applier.apply_whole_matrix(copy.deepcopy(matrix_access))
        return new_matrix_accesser

    def open_new_matrix(self, matrix_file_address) -> MatrixAccesser:
        """
        创建一个新的矩阵访问器，将其添加到矩阵访问器盒子，并返回。
        :param matrix_file_address: 矩阵文件的完整路径，如果文件并非完整路径，则考虑从默认矩阵文件夹寻找。
        :return:
            new_matrix_accesser: 新的矩阵访问器。
        """
        return self.matrix_access_box.new_matrix_accesser(matrix_file_address)
