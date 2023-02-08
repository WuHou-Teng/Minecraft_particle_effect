from Command_Access.Const.Particles_Java import end_rod


# 关于延时方式
ADDITIONAL = 0  # 累加计时
ABSOLUTE = 1    # 绝对时间轴


# 补全粒子信息时用到的默认参数
DX = 0
DY = 0
DZ = 0
SPEED = 0.3
COUNT = 1
FORCE_NORMAL = 'f'
COLOR_R = 1.0
COLOR_G = 1.0
COLOR_B = 1.0
COLOR_TR = 1.0
COLOR_TG = 1.0
COLOR_TB = 1.0
PARTICLE_TYPE = end_rod
SIZE = 0.0625
DURATION = 80
TRANS = 1
DELAY = 0

DEFAULT_INFO = [0, 0, 0,
                DX, DY, DZ, SPEED, COUNT, FORCE_NORMAL,
                COLOR_R, COLOR_G, COLOR_B, COLOR_TR, COLOR_TG, COLOR_TB,
                PARTICLE_TYPE, SIZE,
                DURATION, TRANS, DELAY]
