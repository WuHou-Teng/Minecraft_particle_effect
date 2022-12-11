from Controllers.Particle_Controller.Particle_Controller import ParticleController


class ParticleOfLocat(ParticleController):
    """
    根据粒子在空间中的位置，调整或者设定粒子的类型。
    例如，在相对范围10米内，所有粒子采用 end_rod，以外的粒子采用 end_chest
    有例如，设定绝对坐标中相应空间内的粒子种类。
    """
    def __init__(self):
        super(ParticleOfLocat, self).__init__()


