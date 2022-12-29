from Command_Access.Execute_Generator.Selector.Target_Selector import TargetSelectorBox

# TODO 这里回去后记得改个名字。TargetSelectorBox 改成 TargetSelector
# Selectors 文件名，改成SelectorTags

class TargetSelectorBoxBox(object):
    """
    用来储存创建好的选择器。
    之后要放入ExecuteLayer才能作为指令写入funtion。
    """
    def __init__(self):
        self.selector_dict = {}

    def add_target_selector(self, target_selector):
        """
        添加TargetSelector实例
        :param target_selector: 添加新的Target_selector实例。必须是TargetSelector类
        """
        self.selector_dict[target_selector.get_name] = target_selector

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
        return self.selector_dict.keys()


