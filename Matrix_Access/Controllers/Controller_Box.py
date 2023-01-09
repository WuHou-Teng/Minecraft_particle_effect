from util.Box import Box
# 方位控制器
from Matrix_Access.Controllers.Location_Control.Scale_Controller import ScaleController
from Matrix_Access.Controllers.Location_Control.Rotate_Controller import RotateController
from Matrix_Access.Controllers.Location_Control.Shift_Controller import ShiftController
# 颜色控制器
from Matrix_Access.Controllers.Color_Control.Color_White_List import ColorWhiteList
from Matrix_Access.Controllers.Color_Control.Color_Filter_Amp import ColorFilterAmp
# 其余控制器还未完善，因此暂不添加。


class ControllerBox(Box):

    def __init__(self):
        super().__init__()
        self.controller_dict = {}

    def add_controller(self, controller):
        """
        添加Controller实例
        :param controller: 添加新的controller实例。类型必须为：Controller
        """
        self.controller_dict[controller.get_name()] = controller
        return controller.get_name()

    def get_controller(self, index_name):
        """
        返回具有相应index_name的controller
        :param index_name: 创建controller时，定义的名字。
        """
        if index_name in self.controller_dict.keys():
            return self.controller_dict.get(index_name)
        else:
            return None

    def get_controller_list(self):
        """
        返回盒子中包含的所有controller的index_name
        """
        return list(self.controller_dict.keys())

    def get_object_list(self):
        return self.get_controller_list()

    def add_object(self, new_object):
        return self.add_controller(new_object)

    def get_object(self, index_name):
        return self.get_controller(index_name)

    # ___________________________以下是方便程序设计，封装的控制器添加函数。————————————————————————————-

    def new_scale_controller(self, index_name, x_scale=1, y_scale=1, z_scale=1, scale_centre=None):
        """
        创建新的 ScaleController 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ScaleController
        """
        new_scale_controller = ScaleController(index_name, x_scale, y_scale, z_scale, scale_centre)
        self.add_controller(new_scale_controller)
        return new_scale_controller

    def new_shift_controller(self, index_name, x_shift=0, y_shift=0, z_shift=0):
        """
        创建新的 ShiftController 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ShiftController
        """
        new_shift_controller = ShiftController(index_name, x_shift, y_shift, z_shift)
        self.add_controller(new_shift_controller)
        return new_shift_controller

    def new_rotate_controller(self, index_name, x_angle=0, y_angle=0, z_angle=0, rotate_centre=None):
        """
        创建新的 RotateController 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 RotateController
        """
        new_rotate_controller = RotateController(index_name, x_angle, y_angle, z_angle, rotate_centre)
        self.add_controller(new_rotate_controller)
        return new_rotate_controller

    def new_color_filter_amp_controller(self, index_name, red_range=None, green_range=None, blue_range=None):
        """
        创建新的 ColorFilterAmp 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ColorFilterAmp
        """
        new_color_filter_amp = ColorFilterAmp(index_name, red_range, green_range, blue_range)
        self.add_controller(new_color_filter_amp)
        return new_color_filter_amp

    def new_color_white_list_controller(self, index_name, red_range=None, green_range=None, blue_range=None):
        """
        创建新的 ColorWhiteList 控制器。不会添加到列表，而是直接返回。
        :return:
            新的 ColorWhiteList
        """
        new_color_white_list = ColorWhiteList(index_name, red_range, green_range, blue_range)
        self.add_controller(new_color_white_list)
        return new_color_white_list

