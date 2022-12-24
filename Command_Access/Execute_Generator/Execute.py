from Command_Access.Execute_Generator.Selector.Target_Selector import TargetSelectorBox
from Command_Access.Execute_Generator.Execute_consts import *


class ExecuteLayer(object):
    """
    单层 execute 以及后面跟的所有可能的指令块, 包含execute自己，以及一个目标选择器(Target Selector)
    由 ExecuteBuilder 组装后统一转换为字符串并输出。
    """

    def __init__(self, modifier=AS, selector=None):
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
            self.selector = TargetSelectorBox(entity_mark=NEAREST_PLAYER)

    def set_modifier(self, modifier):
        self.modifier = modifier

    def set_selector(self, selector):
        self.selector = selector

    def to_string(self):
        if self.child is None:
            return f'{self.base} {self.modifier} {self.selector.to_string()} run '
        else:
            pass


class ExecuteBuilder(object):
    """
    将不同层的layer组合起来，再统一输出。
    """
    def __init__(self):
        self.layer = []

    def add_layer(self, execute_layer):
        self.layer.append(execute_layer)

    def new_layer(self, modifier=AS, selector=None):
        return ExecuteLayer(modifier, selector)

    def to_string(self):
        """
        将所有的execute层叠加为一整句指令。如果没有layer，则返回”“
        :return:
        """
        execute_sentence = ""
        for layers in self.layer:
            execute_sentence += layers.to_string()
        return execute_sentence


if __name__ == "__main__":
    from Command_Access.Execute_Generator.Entities.Area_Effect_Cloud import CloudTimer
    # execute 指令 创建工具
    execute_builder = ExecuteBuilder()
    # 计时器实体
    timer_e = CloudTimer("wuhou", Age=0, Duration=200)
    # 实体选择器
    selector_box = TargetSelectorBox(ALL_ENTITY, timer_e)
    # execute 层
    execute_layer = ExecuteLayer(AS, selector_box)
    execute_layer2 = ExecuteLayer(AS)
    # 将execute 层添加到execute创建器中
    execute_builder.add_layer(execute_layer)
    execute_builder.add_layer(execute_layer2)

    print(execute_builder.to_string())


