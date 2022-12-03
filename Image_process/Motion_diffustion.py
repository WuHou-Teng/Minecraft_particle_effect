
# 再尝试一次
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
        self.vistion = self.FORCE

    def set_delta_x(self, delta_x):
        self.delta_x = delta_x

    def set_delta_y(self, delta_y):
        self.delta_y = delta_y

    def set_delta_z(self, delta_z):
        self.delta_z = delta_z

    def set_motion(self, motion_list):
        self.delta_x = motion_list[0]
        self.delta_y = motion_list[1]
        self.delta_z = motion_list[2]

    def set_count(self, count):
        self.count = count

    def set_speed(self, speed):
        self.speed = speed

    def set_speed_default(self):
        self.speed = 0.1

    def set_vision(self, new_vision):
        self.vision = new_vision
        if new_vision not in self.VISION:
            self.vision = self.FORCE

    def set_motion_diffustion(self, motion_diffustion_list):
        self.delta_x = motion_diffustion_list[0]
        self.delta_y = motion_diffustion_list[1]
        self.delta_z = motion_diffustion_list[2]
        self.count = motion_diffustion_list[3]
        self.speed = motion_diffustion_list[4]
        self.vision = motion_diffustion_list[5]
