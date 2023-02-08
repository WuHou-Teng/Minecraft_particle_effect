from Command_Access.Command_Generator.Selector.Selector_Const import *
from Command_Access.Command_Generator.Selector.Target_Selector import TargetSelector
from Command_Access.Command_Generator.Executes.Execute_consts import *


class ExecuteLayer(object):

    def __init__(self, index_name=None):
        self.index_name = index_name if index_name is not None else self.to_string()

    def to_string(self):
        pass


# TODO 条件子修饰符先摆了。还有别的，一并摆了。


class ExecuteConditionEntityLayer(ExecuteLayer):

    def __init__(self, index_name=None, condition_character=IF, selector=None):
        self.condition_character = condition_character
        self.condition_object = ENTITY
        self.selector = selector
        if self.selector is None:
            self.selector = TargetSelector("UnNamed", entity_mark=ALL_ENTITY)
        super().__init__(index_name)

    def to_string(self):
        return f'{self.condition_character} {self.condition_object} {self.selector.to_string()} '


class ExecuteConditionBlockLayer(ExecuteLayer):

    def __init__(self, index_name=None, condition_character=IF, x=0, y=0, z=0,
                 coo_type=RELA_COORD, block_type="minecraft:stone"):
        # TODO 需要添加我的时间所有方块的列表
        super().__init__(index_name)
        self.condition_character = condition_character
        self.condition_object = BLOCK
        self.coo_type = coo_type
        self.x = COO_DICT.get(self.coo_type) + str(x)
        self.y = COO_DICT.get(self.coo_type) + str(y)
        self.z = COO_DICT.get(self.coo_type) + str(z)
        self.block_type = block_type

    def to_string(self):
        return f'{self.condition_character} {self.condition_object} {self.x} {self.y} {self.z} {self.block_type} '


class ExecuteModifierLayer(ExecuteLayer):
    """
    单层 execute 以及后面跟的所有可能的指令块, 包含execute自己，以及一个目标选择器(Target Selector)
    由 ExecuteBuilder 组装后统一转换为字符串并输出。
    """

    def __init__(self, index_name=None, modifier=AS, selector=None):
        # self.base = 'execute'
        # TODO 条件子命令，if 或者 unless, 默认不启用，这个东西是另一个区域，还未完善。
        self.condition_subcommand = None

        # 方位/身份 修饰符，默认为 as
        # as at facing align anchored
        self.modifier_subcommand = modifier

        # 实体选择器,例如:
        # @e[type=minecraft:sheep,nbt={}]
        self.selector = selector
        if selector is None:
            self.selector = TargetSelector("UnNamed", entity_mark=NEAREST_PLAYER)

        super().__init__(index_name)

    def get_name(self):
        return self.index_name

    def get_selector(self):
        return self.selector

    def set_modifier(self, modifier):
        self.modifier_subcommand = modifier

    def set_selector(self, selector):
        self.selector = selector

    def to_string(self):
        return f'{self.modifier_subcommand} {self.selector.to_string()} '




