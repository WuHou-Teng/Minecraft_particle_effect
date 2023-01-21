from Command_Access.Command_Generator.Executes.Execute_Layer import ExecuteLayer
from Command_Access.Command_Generator.Executes.Execute_consts import AS, ALL_ENTITY
from Command_Access.Command_Generator.Selector.Target_Selector import TargetSelector


class ExecuteBuilder(object):
    """
    将不同层的layer组合起来，再统一输出。
    """
    def __init__(self):
        self.layer = []

    def add_layer(self, new_execute_layer):
        self.layer.append(new_execute_layer)

    def new_layer(self, modifier=AS, selector=None):
        return ExecuteLayer(modifier, selector)

    def clear_layer(self):
        self.layer = []

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
    from Command_Access.Command_Generator.Entities.Area_Effect_Cloud import CloudTimer
    # execute 指令 创建工具
    execute_builder = ExecuteBuilder()
    # 计时器实体
    timer_e = CloudTimer(index_name="wuhou", Tag="wuhou", Age=0, Duration=200)
    # 实体选择器
    selector_box = TargetSelector(index_name="wuhou", entity_mark=ALL_ENTITY, entity=timer_e)
    # execute 层
    execute_layer = ExecuteLayer("作为计时器", AS, selector_box)
    execute_layer2 = ExecuteLayer("作为最近玩家", AS)
    # 将execute 层添加到execute创建器中
    execute_builder.add_layer(execute_layer)
    execute_builder.add_layer(execute_layer2)

    print(execute_builder.to_string())
