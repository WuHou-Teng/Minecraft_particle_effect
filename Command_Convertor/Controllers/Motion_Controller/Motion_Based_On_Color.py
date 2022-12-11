from Command_Convertor.Controllers.Motion_Controller.Motion_Controller import MotionController


# 探讨移动与颜色的相关性。
class MotionOfColor(MotionController):
    """
    根据不同的粒子颜色，对粒子的移动做出改变。
    例如，可以设定为只有紫色的粒子向前移动，其余粒子向后移动。
    又例如，赤橙黄绿青蓝紫，每种颜色移动速度不同，移动角度也不同。
    """
    def __init__(self):
        super(MotionOfColor, self).__init__()
