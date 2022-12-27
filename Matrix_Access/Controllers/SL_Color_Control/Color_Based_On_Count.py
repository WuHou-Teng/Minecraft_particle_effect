from Matrix_Access.Controllers.Color_Control.Color_Controller import ColorController


# 探讨粒子颜色和已经转化的粒子数量之间的关系。
class ColorOfCount(ColorController):
    """
    根据已经转化的粒子数量，对粒子的颜色进行调节。
    例如，每转化一个粒子，红色通道的颜色比例就增加0.01
    又例如，按照一定的随机性，对粒子颜色进行调整，制作特殊的效果。
    """
    def __init__(self):
        super(ColorOfCount, self).__init__()
