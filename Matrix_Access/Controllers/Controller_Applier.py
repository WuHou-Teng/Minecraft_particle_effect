from Matrix_Access.Controllers.Controller_Interface import ControllerBase
from Matrix_Access.Matrix_Accesser import MatrixAccesser
from Matrix_Access.Particles import MCParticle


class ControllerApplier(object):
    """
    该类是对所有控制器的一个整合。
    可以添加不同类型的控制器。
    """
    def __init__(self):
        self.controller_list = []

    def add_controller_to_apply_list(self, new_controller):
        """
        添加新的控制器到列表。
        :param new_controller: 新的控制器。
        :return:
            添加控制器后的 ControllerApplier
        """
        assert issubclass(type(new_controller), ControllerBase)
        self.controller_list.append(new_controller)
        return self
        # if issubclass(type(new_controller), ControllerBase):
        #     self.controller_list.append(new_controller)
        #     return True
        # else:
        #     return False

    def clear_controller_box(self):
        self.controller_list = []

    def get_controller_list(self):
        return self.controller_list

    def has_controllers(self):
        return len(self.controller_list) > 0

    def pop_controller(self, index):
        """
        将调用列表的其中一个删除并返回。
        :param index:
        :return:
        """
        if len(self.controller_list) > index:
            return self.controller_list.pop(index)

    def get_controller_at(self, index):
        """
        按照输入的序号，获得控制器列表中对应位置的控制器。
        :param index: 序号
        :return: 列表中的控制器。
        """
        if len(self.controller_list) > index:
            return self.controller_list[index]

    def apply_processing(self, particle) -> MCParticle:
        """
        遍历列表中的 Controller.process() 并返回经过修改的粒子。
        :param particle: 粒子信息
        :return:
            经过修改的粒子。
        """
        # 遍历所有的控制器。
        for controllers in self.controller_list:
            # 这里只是声明一次控制器的类型。方便程序调用。
            if issubclass(type(controllers), ControllerBase):
                # 将粒子信息丢给控制器的 process 函数，获得经过修改的粒子信息。
                particle = controllers.process(particle)
                # 如果返回为空，意味着改粒子在经过白名单筛选时没有通过。
                if particle is None:
                    # 终止for循环，直接返回空。
                    return None
        # 返回经过修改的粒子信息。
        return particle

    # TODO 为所有controller完善apply_matrix
    def apply_whole_matrix(self, matrix_accesser) -> MatrixAccesser:
        """
        遍历列表中的 Controller.process_matrix()，并返回经过修改的矩阵访问器。
        :param matrix_accesser: 粒子矩阵访问器
        :return:
            matrix_accesser: 经过控制器处理后的矩阵访问器
        """
        for controllers in self.controller_list:
            # 这里只是声明一次控制器的类型。方便程序调用。
            if issubclass(type(controllers), ControllerBase):
                matrix_accesser = controllers.process_matrix(matrix_accesser)
        return matrix_accesser


