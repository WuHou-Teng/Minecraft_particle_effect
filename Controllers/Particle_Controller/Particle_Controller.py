from Controllers import ControllerBase


class ParticleController(ControllerBase):
    """
    粒子解析器。
    根据输入相应的数据，反馈应当使用的粒子。
    目前打算添加以下几种解析方式：
        * 根据颜色解析 ★
            —— 从粒子库中挑选与输入颜色最接近的颜色的粒子，并反馈。（支持 DIY）
        * 根据运动速度解析
            —— 自定义不同的速度对应不同的粒子类型。
        * 根据空间位置解析
            —— 自定义不同空间位置对应不同的粒子类型。
    """
    def __init__(self):
        super(ParticleController, self).__init__()
        # 粒子词典，可以根据输入的内容，反馈相应的粒子类型。
        self.particle_dict = None

