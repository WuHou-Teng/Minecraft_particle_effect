from Controllers.Motion_Controller import MotionController


# 探讨移动与不同粒子位置的相关性
class MotionOfLocat(MotionController):
    """
    根据粒子的坐标，对粒子的移动做出改变。
    例如，可以设定为相对坐标10米内的粒子向上移动，其余粒子向下移动
    又例如，粒子移动速度与方位跟随空间位置改变而改变。
    """
    def __init__(self):
        super(MotionOfLocat, self).__init__()

