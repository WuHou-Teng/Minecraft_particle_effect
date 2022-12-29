from Matrix_Access.Controllers.Controller_Applier import ControllerApplier


class MatrixGenerator(object):
    """
    将读取的数据转化为坐标矩阵，并保存到相应的位置。
    此类同样具有调用控制器的能力。
    以及调用函数的能力。
    """
    def __init__(self):
        # 变换: 添加控制器。可以自定义一系列对矩阵的修改。
        # 注意，控制器的特点是逐个对粒子进行变换，不关注整体。因此，其效果不如自定义函数那样强大，仅可以机械化的进行简单的变换。
        self.controller = ControllerApplier()

