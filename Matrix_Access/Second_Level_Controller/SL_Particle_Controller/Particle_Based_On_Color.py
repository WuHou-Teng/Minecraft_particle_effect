from Matrix_Access.Controllers.Particle_Controller.Particle_Controller import ParticleController


class ParticleOfColor(ParticleController):
    """
    根据粒子颜色确定使用的粒子类型。
    此类需要预定义 颜色——粒子　字典，来帮助转化。

    """
    def __init__(self):
        super(ParticleOfColor, self).__init__()


