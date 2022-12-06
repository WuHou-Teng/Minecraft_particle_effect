from Execute_Generator.Condition import ConditionBuilder
from Const.Execute_consts import *


class ExecuteBuilder(object):
    """
    检测执行指令：execute 以及后面跟的所有可能的指令块
    """
    def __init__(self, modifier=AS, entity="@p"):
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
        self.condition = ConditionBuilder()

    def to_string(self):
        if self.child is None:
            if not self.condition.has_condition():
                return self.base + " " + self.modifier + " " + self.entity + " run "
            else:
                return self.base + " " + self.modifier + " " + self.entity + self.condition.to_string() + " run "
