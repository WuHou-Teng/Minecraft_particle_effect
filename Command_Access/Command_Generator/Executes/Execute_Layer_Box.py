from Command_Access.Command_Generator.Executes.Execute_Layer import ExecuteLayer
from Command_Access.Command_Generator.Executes.Execute_consts import AS
from util.Box import Box


class ExecuteLayerBox(Box):

    def __init__(self):
        super().__init__()
        self.execute_layer_dict = {}

    def add_execute_layer(self, execute_layer):
        """
        添加Controller实例
        :param execute_layer: 添加新的execute_layer实例。类型必须为：Controller
        """
        self.execute_layer_dict[execute_layer.get_name()] = execute_layer
        return execute_layer.get_name()

    def get_execute_layer(self, index_name):
        """
        返回具有相应index_name的execute_layer
        :param index_name: 创建execute_layer时，定义的名字。
        """
        if index_name in self.execute_layer_dict.keys():
            return self.execute_layer_dict.get(index_name)
        else:
            return None

    def get_execute_layer_list(self):
        """
        返回盒子中包含的所有execute_layer的index_name
        """
        return list(self.execute_layer_dict.keys())

    def get_object_list(self):
        return self.get_execute_layer_list()

    def add_object(self, new_object):
        return self.add_execute_layer(new_object)

    def get_object(self, index_name):
        return self.get_execute_layer(index_name)

    def new_layer(self, index_name=None, modify=AS, selector=None):
        new_execute_layer = ExecuteLayer(index_name, modify, selector)
        self.add_execute_layer(new_execute_layer)
        return new_execute_layer

