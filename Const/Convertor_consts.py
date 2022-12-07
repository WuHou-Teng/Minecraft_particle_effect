
JAVA = 1
BED_ROCK = 2

BLACK = 0
WHITE = 1

# 绝对坐标，相对坐标，面朝坐标
ABS_COORD = 0
RELA_COORD = 1
FACE_COORD = 2

# 粒子画默认最长与最宽
Height_MAX = 100
Width_MAX = 100

# 图片方向
West_East = 'x'
North_South = 'z'
Lay_Down = 'y'

# 图片对齐
LEFT_UP = 1
LEFT_MID = 2
LEFT_DOWN = 3
MID_UP = 4
MIDDLE = 5
MID_DOWN = 6
RIGHT_UP = 7
RIGHT_MID = 8
RIGHT_DOWN = 9

# 各通道颜色最大最小值
RED_MIN = 0.001
RED_MAX = 1
GREEN_MIN = 0
GREEN_MAX = 1
BLUE_MIN = 0
BLUE_MAX = 1

# 颜色滤除率。
FULL = -1   # 即为降低至最低值。
DAMP = -0.75
HALF = -0.5
QUART = -0.25  # 即为降低0.25倍，红色通道最低不低于0.001

NONE = 0  # 即为不滤除,也不增强

# 颜色增强率
SINGLE = 1  # 即为增强1倍，但最大不超过1
DOUBLE = 2
TRIPLE = 3
QUADRUPLE = 4







