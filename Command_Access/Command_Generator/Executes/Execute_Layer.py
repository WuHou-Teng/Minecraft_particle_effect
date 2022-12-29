from Command_Access.Command_Generator.Selector.Target_Selector import TargetSelector
from Command_Access.Command_Generator.Executes.Execute_consts import *


class ExecuteLayer(object):
    """
    单层 execute 以及后面跟的所有可能的指令块, 包含execute自己，以及一个目标选择器(Target Selector)
    由 ExecuteBuilder 组装后统一转换为字符串并输出。
    """

    def __init__(self, index_name=None, modifier=AS, selector=None):
        self.index_name = index_name if index_name is not None else self.to_string()

        self.base = 'execute'
        # TODO 条件子命令，if 或者 unless, 默认不启用，这个东西是另一个区域，还未完善。
        self.child = None

        # 方位/身份 修饰符，默认为 as
        # as at facing align anchored
        self.modifier = modifier

        # 实体选择器,例如:
        # @e[type=minecraft:sheep,nbt={}]
        self.selector = selector
        if selector is None:
            self.selector = TargetSelector("UnNamed", entity_mark=NEAREST_PLAYER)

    def get_name(self):
        return self.index_name

    def set_modifier(self, modifier):
        self.modifier = modifier

    def set_selector(self, selector):
        self.selector = selector

    def to_string(self):
        if self.child is None:
            return f'{self.base} {self.modifier} {self.selector.to_string()} run '
        else:
            pass




