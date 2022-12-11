from Matrix_Access.Controllers.Controller_Interface import ControllerBase
from Matrix_Access.Controllers.Motion_Controller.Motion_Controller_Consts import *


# 粒子运动本身就是多维度属性，包括粒子移动的距离，以及移动的速度，以及扩散粒子数量。这里默认粒子无扩散。
# 最终决定还是将offset和speed合并为Motion。实际上，速度和offset的比例是自动计算的。（0.1的速度总是允许粒子走完相应的距离。）
# 因此，速度与offset可以不必存在复杂的相关性。
# 而如果想分别对offset和speed设定于其余属性关联模式，可以添加两次控制器。
class MotionController(ControllerBase):
    """
    粒子空间位移/扩散控制器
    """
    def __init__(self):
        super(MotionController, self).__init__()
        self.x_delta = 0
        self.y_delta = 0
        self.z_delta = 0
        # offset模式，是直接将x_delta, y_delta, z_delta 加到现有的motion上，还是直接修改现有的motion
        # 默认为加上去
        self.offset_mode = Motion_ADD
        # 转换时，粒子运动范围倍率
        self.offset_multi = 1

        # speed, 粒子的速度实际是一个比例单位。0.1表示粒子向目标坐标移动一倍距离。0.2则是两倍距离，具体速度由 实际距离/时间常量 计算。
        self.speed = 0
        # speed模式，和offset模式类似。
        self.speed_mode = Motion_ADD

        # offset与speed关联方式：默认为无关联。
        self.relevance_mode = NO_RELEVANCE

    def process(self, particle):
        return particle


# 这里暂且保留独立的速度
class SpeedController(ControllerBase):
    """
    粒子移动速度控制器
    """
    def __init__(self):
        super(SpeedController, self).__init__()
        self.speed = 0
        # 设定模式默认为增加。
        self.speed_mode = Motion_ADD

    def process(self, particle):
        return particle
