from Controllers.Particle_Controller.Particle_Controller import ParticleController


class ParticleOfMotion(ParticleController):
    """
    根据粒子的运动方式确定粒子的类型。
    例如，向前移动的粒子
    """
    def __init__(self):
        super(ParticleOfMotion, self).__init__()


