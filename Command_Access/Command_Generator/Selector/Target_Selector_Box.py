from Command_Access.Command_Generator.Selector.Selector_Const import NEAREST_PLAYER
from Command_Access.Command_Generator.Selector.Target_Selector import TargetSelector
from util.Box import Box


class TargetSelectorBox(Box):
    """
    用来储存创建好的选择器。
    之后要放入ExecuteLayer才能作为指令写入funtion。
    """
    def __init__(self):
        super().__init__()
        self.selector_dict = {}

    def add_target_selector(self, target_selector):
        """
        添加TargetSelector实例
        :param target_selector: 添加新的Target_selector实例。必须是TargetSelector类
        """
        self.selector_dict[target_selector.get_name()] = target_selector
        return target_selector.get_name()

    def get_target_selector(self, index_name):
        """
        返回具有相应index_name的target_selector
        :param index_name: 创建target_selector时，定义的名字。
        """
        if index_name in self.selector_dict.keys():
            return self.selector_dict.get(index_name)
        else:
            return None

    def get_target_selector_list(self):
        """
        返回盒子中包含的所有target_selector的index_name
        """
        return list(self.selector_dict.keys())

    def get_object_list(self):
        return self.get_target_selector_list()

    def add_object(self, new_object):
        return self.add_target_selector(new_object)

    def get_object(self, index_name):
        return self.get_target_selector(index_name)

    def new_target_selector(self, index_name=None, entity_mark=NEAREST_PLAYER, entity=None):
        new_target_selector = TargetSelector(index_name, entity_mark, entity)
        # self.add_target_selector(new_target_selector)
        return new_target_selector

