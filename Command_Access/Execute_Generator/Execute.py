from Command_Access.Execute_Generator.Selector.Target_Selector import TargetSelector
from Command_Access.Execute_Generator.Execute_consts import *


class ExecuteLayer(object):
    """
    单层 execute 以及后面跟的所有可能的指令块, 包含execute自己，以及一个目标选择器(Target Selector)
    由 ExecuteBuilder 组装后统一转换为字符串并输出。
    """

    def __init__(self, modifier=AS, entity_mark=NEAREST_PLAYER, tags=None):
        self.base = 'execute'
        # 条件子命令，if 或者 unless, 默认不启用
        self.child = None

        # 方位/身份 修饰符，默认为 as
        # as at facing align anchored
        self.modifier = modifier

        # 确定目标实体, 默认值为最近玩家
        # @a @p @r @e @s
        self.entity = entity_mark

        # 特殊判定条件
        # 例如 [
        # 	nbt={Inventory:[{Slot:103b, Count:1b, tag:{Tags:["Core_of_Ifrit"]}}]},
        # 	nbt={Inventory:[{Slot:-106b, Count:1b, tag:{Tags:["meteor_fall"]}}]}
        # ]
        self.condition = TargetSelector()

    def set_modifier(self, modifier):
        self.modifier = modifier

    def set_entity(self, entity):
        self.entity = entity

    def to_string(self):
        if self.child is None:
            if not self.condition.has_condition():
                return self.base + " " + self.modifier + " " + self.entity + " run "
            else:
                return self.base + " " + self.modifier + " " + self.entity + self.condition.to_string() + " run "
        else:
            pass


class ExecuteBuilderNew(object):
    """
    将不同层的layer组合起来，再统一输出。
    """
    def __init__(self):
        self.layer = []

    def add_layer(self, modifier=AS, entity=NEAREST_PLAYER):



class ExecuteBuilder(object):
    """
    检测执行指令：execute 以及后面跟的所有可能的指令块
    TODO 未来指令生成器的雏形。
    """
    def __init__(self, modifier=AS, entity=NEAREST_PLAYER):
        self.base = 'execute'
        # 条件子命令，if 或者 unless, 默认不启用
        self.child = None

        # 方位/身份 修饰符，默认为 as
        # as at facing align anchored
        self.modifier = modifier

        # 确定目标实体, 默认值为最近玩家
        # @a @p @r @e @s
        self.entity = entity

        # 特殊判定条件
        # 例如 [
        # 	nbt={Inventory:[{Slot:103b, Count:1b, tag:{Tags:["Core_of_Ifrit"]}}]},
        # 	nbt={Inventory:[{Slot:-106b, Count:1b, tag:{Tags:["meteor_fall"]}}]}
        # ]
        self.condition = TargetSelector()

    def set_modifier(self, modifier):
        self.modifier = modifier

    def set_entity(self, entity):
        self.entity = entity

    def to_string(self):
        if self.child is None:
            if not self.condition.has_condition():
                return self.base + " " + self.modifier + " " + self.entity + " run "
            else:
                return self.base + " " + self.modifier + " " + self.entity + self.condition.to_string() + " run "
        else:
            pass
