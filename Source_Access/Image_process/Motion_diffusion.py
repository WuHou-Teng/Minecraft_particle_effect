
class MotionDiffusion(object):
    FORCE = 'force'
    NORMAL = 'normal'
    VISION = [FORCE, NORMAL]

    def __init__(self):
        self.delta_x = 0
        self.delta_y = 0
        self.delta_z = 0
        self.count = 0
        self.speed = 0
        self.vision = self.FORCE

    def set_delta_x(self, delta_x):
        self.delta_x = delta_x if type(delta_x) == int or type(delta_x) == float else 0

    def set_delta_y(self, delta_y):
        self.delta_y = delta_y if type(delta_y) == int or type(delta_y) == float else 0

    def set_delta_z(self, delta_z):
        self.delta_z = delta_z if type(delta_z) == int or type(delta_z) == float else 0

    def set_motion(self, motion_list):
        self.set_delta_x(motion_list[0])
        self.set_delta_y(motion_list[1])
        self.set_delta_z(motion_list[2])

    def set_count(self, count):
        self.count = count if type(count) == int else 0

    def set_speed(self, speed):
        self.speed = speed if type(speed) == int or type(speed) == float else 0

    def set_speed_standard(self):
        self.speed = 0.1

    def set_vision(self, new_vision):
        self.vision = new_vision if new_vision in self.VISION else self.FORCE

    def set_motion_diffusion(self, motion_diffusion_list):
        self.set_motion(motion_diffusion_list[:3])
        self.set_count(motion_diffusion_list[3])
        self.set_speed(motion_diffusion_list[4])
        self.set_vision(motion_diffusion_list[5])
