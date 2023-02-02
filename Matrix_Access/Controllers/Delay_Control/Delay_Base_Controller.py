from Matrix_Access.Controllers.Controller_Interface import ControllerBase
from Matrix_Access.Matrix_Const import *
from Matrix_Access.Particles import MCParticle


class DelayBaseController(ControllerBase):
    """
    延时控制器基类
    """
    def __init__(self, delay_type=ABSOLUTE):
        super().__init__()
        # 延时类型，默认为ADDITIONAL
        self.delay_type = delay_type
        # 时刻
        # 如果是累加计时，则是之前所有粒子的延时的和。
        # 如果是绝对计时，则是之前粒子中延时最大的那个。
        self.current_time = 0
        self.last_time = 0

    def switch_delay_type(self, delay_type=None):
        if delay_type is None:
            self.delay_type = ADDITIONAL if self.delay_type is ABSOLUTE else ABSOLUTE
        else:
            self.delay_type = delay_type

    def get_current_time(self):
        """
        获取目前指针所在的时刻。
        :return:
        """
        return self.current_time

    def record_time(self, particle):
        """
        记录时间，将上次粒子的时间信息复制到 last_time.
        将此次粒子的时间信息记录到 current_time。
        :param particle:  MCParticle 类，包含所有可直接调用的数字参数。
        """
        assert type(particle) is MCParticle
        self.last_time = self.current_time
        if self.delay_type is ADDITIONAL:
            # 累加时间轴下，总时刻就是所有粒子的延时的累加。
            self.current_time += particle.delay
        elif self.delay_type is ABSOLUTE:
            # 绝对时间轴下，总时刻就是上一个粒子的时刻。
            self.current_time = particle.delay





