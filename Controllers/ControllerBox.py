from Controllers.Controller_Interface import ControllerBase
# 方位控制器
from Controllers.Location_Controller.Scale_Controller import ScaleController
from Controllers.Location_Controller.Rotate_Controller import RotateController
from Controllers.Location_Controller.Shift_Controller import ShiftController
# 颜色控制器
from Controllers.Color_Controller.Color_White_List import ColorWhiteList
from Controllers.Color_Controller.Color_Filter_Amp import ColorFilterAmp
# 其余控制器还未完善，因此暂不添加。


class ControllerToolBox(object):
    """
    该类是对所有控制器的一个整合。
    可以添加不同类型的控制器。
    """
    def __init__(self):
        self.controller_list = []

    def controller_box_add(self, new_controller):
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

    # ___________________________以下是方便程序设计，封装的控制器添加函数。————————————————————————————-

    def new_scale_controller(self):
        """
        创建新的 ScaleController 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ScaleController
        """
        return ScaleController()

    def new_shift_controller(self):
        """
        创建新的 ShiftController 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ShiftController
        """
        return ShiftController()

    def new_rotate_controller(self):
        """
        创建新的 RotateController 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 RotateController
        """
        return RotateController()

    def new_color_filter_amp_controller(self):
        """
        创建新的 ColorFilterAmp 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ColorFilterAmp
        """
        return ColorFilterAmp()


    def new_color_white_list_controller(self):
        """
        创建新的 ColorWhiteList 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ColorWhiteList
        """
        return ColorWhiteList()
