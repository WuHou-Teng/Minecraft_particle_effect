from Matrix_Access.Controllers.Controller_Interface import ControllerBase


class ControllerApplier(object):
    """
    该类是对所有控制器的一个整合。
    可以添加不同类型的控制器。
    """
    def __init__(self):
        self.controller_list = []

    def add_controller_to_apply_list(self, new_controller) -> bool:
        """
        添加新的控制器到列表。
        :param new_controller: 新的控制器。
        :return:
            控制器是否添加成功。如果控制器不合法，则会添加失败。
        """
        if issubclass(type(new_controller), ControllerBase):
            self.controller_list.append(new_controller)
            return True
        else:
            return False

    def clear_controller_box(self):
        self.controller_list = []

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

    def apply_processing(self, particle):
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


