from Matrix_Access.Controllers.Color_Control.Color_Controller import ColorController


# 探讨粒子颜色和粒子运动方式之间的关系。
class ColorOfMotion(ColorController):
    """
    根据粒子的移动方式，对粒子的颜色进行修改。
    例如，向上移动的粒子为蓝色，其余为红色。
    又例如，不同移动速度的粒子分别对应不同的颜色。
    """
    def __init__(self):
        super(ColorOfMotion, self).__init__()
