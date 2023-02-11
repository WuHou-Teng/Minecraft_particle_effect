from Matrix_Access.Matrix_Const import *


class MCParticle(object):
    # 考虑添加__slot__来压缩体积。
    def __init__(self, x, y, z,
                 dx=DX, dy=DY, dz=DZ, time_on_moving=SPEED, count=COUNT, force_normal=FORCE_NORMAL,
                 r=COLOR_R, g=COLOR_G, b=COLOR_B, rt=COLOR_TG, gt=COLOR_TG, bt=COLOR_TB,
                 particle_type=PARTICLE_TYPE, size=SIZE, duration=DURATION, transparency=TRANS, delay=DELAY,
                 color_delay=COLOR_DELAY):
        """
        # 基本参数
          x, y, z,
          1, 1, 1,
        # 附加参数
          d_x, d_y, d_z, speed, count, force_normal,
          0,   0,   0,   0,     1,     f/n,
        # 额外参数
          Color(R, G, B),   color_transfer(R,G,B), particle_type, 粒子大小,
          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined),  1,
        # mod参数
          持续时间(tick), 粒子透明度, 延时(tick)
          80,           1,        0
        """
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.speed = time_on_moving if time_on_moving > 0 else 0.01
        self.count = count
        self.f_n = force_normal
        self.r = r
        self.g = g
        self.b = b
        self.rt = rt
        self.gt = gt
        self.bt = bt
        self.particle_type = particle_type
        self.size = size
        self.duration = duration
        self.transparency = transparency if transparency >= 0.11 else 0.11
        self.delay = delay
        self.color_delay = color_delay

    @property
    def data(self):
        return [self.x, self.y, self.z,
                self.dx, self.dy, self.dz,
                self.speed, self.count, self.f_n,
                self.r, self.g, self.b, self.rt, self.gt, self.bt,
                self.particle_type, self.size, self.duration,
                self.transparency, self.delay, self.color_delay]

