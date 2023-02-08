# Entity_Mark
ALL_PLAYER = "@a"
NEAREST_PLAYER = "@p"
CURRENT_ENTITY = "@s"
ALL_ENTITY = "@e"
RANDOM_PLAYER = "@r"

# sort
NEAREST = "nearest"      # 最近的, 将目标由近到远排序。（@p的默认排序方式）
FURTHEST = "furthest"    # 最远的, 将目标由远到近排序。
RANDOM = "random"        # 随机的, 将目标随机排序。（@r的默认排序方式）
ARBITRARY = "arbitrary"  # 将目标按生成时间由远到近排序。（@a和@e的默认排序方式）

# 绝对坐标，相对坐标，面朝坐标
ABS_COORD = 0
RELA_COORD = 1
FACE_COORD = 2

COO_DICT = {RELA_COORD: "~", FACE_COORD: "^", ABS_COORD: ""}

