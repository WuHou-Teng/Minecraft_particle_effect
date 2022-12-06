
class ConditionBuilder(object):
    """
    在execute指令中，对象后往往需要添加相应的描述限制。
    例如 execute as @e[type=minecraft:item, distance=0..5, nbt={Item:{id:"minecraft:blaze_powder"}, OnGround:1b}] run...
    其中[type=minecraft:item, distance=0..5, nbt={Item:{id:"minecraft:blaze_powder"}, OnGround:1b}] 就是条件限制。
    该类是创建/添加条件限制的基类。
    """
    def __init__(self):
        self.condition = []

    def get_condition(self):
        """
        直接返回已有的条件列表。
        :return:
            self.condition: 已有的条件列表
        """
        return self.condition

    def to_string(self):
        """
        将condition转换为字符串的形式，方便镶嵌到指令中
        :return:
        """
        string = "["
        for cond in self.condition:
            string += cond
        string += "]"
        return string

    def add_condition(self, new_condition):
        """
        添加新的条件。
        :param new_condition:
        :return:
        """
        self.condition.append(new_condition)

    def has_condition(self):
        return True if len(self.get_condition()) > 0 else False

    # TODO 这里我觉得以后还要根据不一样的对象添加条件。例如玩家，实体，或者item，都有各自特有的条件词缀。

