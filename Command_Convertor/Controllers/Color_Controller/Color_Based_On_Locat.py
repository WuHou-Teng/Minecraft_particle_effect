from Command_Convertor.Controllers.Color_Controller.Color_Controller import ColorController


# 探讨粒子颜色与空间位置的关系
class ColorOfLocat(ColorController):
    """
    根据粒子在空间中的位置修改粒子的颜色。
    例如: 可以设定相对距离10米内的粒子为红色。其余为蓝色。
    又例如，可以让粒子的颜色随着坐标改变而改变。
    """
    def __init__(self):
        super(ColorOfLocat, self).__init__()
