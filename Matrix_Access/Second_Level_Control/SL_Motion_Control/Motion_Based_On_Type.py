from Matrix_Access.Controllers.Motion_Control.Motion_Controller import MotionController


# 探讨移动与不同粒子类型的相关性
class MotionOfType(MotionController):
    """
    根据不同类型的粒子，对粒子的移动做出改变。
    例如，可以设定为只有end_rod粒子向前移动，其余粒子向后移动。
    又例如，对每一种不同的粒子类型设定不一样的速度。
    """
    def __init__(self):
        super(MotionOfType, self).__init__()
