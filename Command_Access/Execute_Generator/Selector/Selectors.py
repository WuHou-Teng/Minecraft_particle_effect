from Command_Access.Execute_Generator.Selector.Selector_Const import *


class Selectors(object):
    """
    选择器标签 的 实体基类。

    """

    def __init__(self):
        pass

    def to_string(self):
        """
        将自身的内容输出为可以直接转化为mc指令的字符串。
        :return:
        """
        pass


class Location(Selectors):
    """
    location标签类, 修改目标选择器执行位置。
    """

    def __init__(self, x, y, z, x_coo_type=RELA_COORD, y_coo_type=RELA_COORD, z_coo_type=RELA_COORD):
        super().__init__()
        # 默认三个方向都采用相对坐标
        self.coo_type = [x_coo_type, y_coo_type, z_coo_type]
        self.coo_dict = {RELA_COORD: "~", FACE_COORD: "^", ABS_COORD: ""}
        self.x = x
        self.y = y
        self.z = z

    # 修改坐标相对性
    def set_coo_type(self, x_coo_type, y_coo_type=None, z_coo_type=None):
        if x_coo_type not in self.coo_dict.keys():
            x_coo_type = RELA_COORD
        if y_coo_type is None:
            y_coo_type = x_coo_type
        if z_coo_type is None:
            z_coo_type = x_coo_type
        self.coo_type = [x_coo_type, y_coo_type, z_coo_type]

    def to_string(self):
        return (f'x={self.coo_dict.get(self.coo_type[0])}{self.x},'
                f'y={self.coo_dict.get(self.coo_type[1])}{self.y},'
                f'z={self.coo_dict.get(self.coo_type[2])}{self.z},')


class Distance(Selectors):
    """
    distance 标签类，确定目标个测量中心的距离
    """

    def __init__(self, max_distance=0, min_distance=0, use_range=True):
        """
        :param max_distance: 最大距离
        :param min_distance: 最小距离, 如果最小距离大于最大距离，且use_range==True, 则写为 [distance=最小距离..]
                            而如果use_range==False, 则视最小距离为最大距离。
        :param use_range: 是否使用区间，否，则代表固定距离。
        """
        super(Distance, self).__init__()
        self.use_range = use_range

        self.max_distance = max_distance
        if self.max_distance < 0:
            self.max_distance = -self.max_distance

        self.min_distance = min_distance
        if self.min_distance < 0:
            self.min_distance = -self.min_distance
        if not use_range and self.min_distance > self.max_distance:
            self.max_distance = self.min_distance

    def to_string(self):
        if self.use_range:
            if self.min_distance < self.max_distance:
                return f'distance={self.min_distance}..{self.max_distance},'
            else:
                return f'distance={self.min_distance}..,'
        else:
            return f'distance={self.max_distance},'


class VolSpace(Selectors):
    """
    体积尺寸标签类。和 location配合使用，框出一篇区域。
    选择所有位于一定长方体区域内部的目标。
    体积定义为从基准点开始，
        向“X”方向（东方）延伸dx格（包括基准点本身，下同），
        向“Y”方向（上方）延伸dy格，
        向“Z”方向（南方）延伸dz格。
    如果只指定了其中的部分参数，那么剩余的参数默认为0。
    """

    def __init__(self, dx=0, dy=0, dz=0):
        super().__init__()
        # 这里我实在懒得去考虑某些复杂问题了，用户自己会用的话，就注意一下吧
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def to_string(self):
        return (f'dx={self.dx},'
                f'dy={self.dy},'
                f'dz={self.dz},')


class Scores(Selectors):
    """
    计分板标签类。因为该类可以具有多重数值，故设定为需要额外手动添加。
    """

    def __init__(self):
        super().__init__()
        self.score_list = []

    def add_score(self, score_name, score_min_value=0, score_max_value=0, use_range=False):
        if not use_range:
            self.score_list.append(f'{score_name}={score_max_value},')
        else:
            if score_min_value == score_max_value:
                self.score_list.append(f'{score_name}={score_max_value},')
            elif score_min_value < score_max_value:
                self.score_list.append(f'{score_name}={score_min_value}..{score_max_value},')
            elif score_min_value > score_max_value:
                self.score_list.append(f'{score_name}={score_min_value}..,')

    def to_string(self):
        if len(self.score_list) == 0:
            return None
        string = "score={"
        for scores in self.score_list:
            string += scores
        return string + "},"


class Tag(Selectors):
    """
    Tag 标签类
    """
    def __init__(self, tag, flip=False):
        super().__init__()
        self.tag = tag
        self.flip = flip

    def to_string(self):
        if not self.flip:
            return f'tag={self.tag},'
        else:
            return f'tag=!{self.tag},'


class Team(Selectors):
    """
    Team 标签类
    """
    def __init__(self, team, flip=False):
        """
        :param team: 队伍名字
        :param flip: 是否反选
        """
        super().__init__()
        self.flip = flip
        self.team = team

    def to_string(self):
        if not self.flip:
            return f'team={self.team},'
        else:
            return f'team=!{self.team},'


class Name(Selectors):
    """
    Name 标签类
    """
    def __init__(self, name=None, flip=False):
        """
        :param name: 名字中请不要包含空格
        :param flip: 是否反选
        """
        super().__init__()
        self.flip = flip
        self.name = name

    def to_string(self):
        #
        if self.name is None:
            return f'name=\"\"'

        if not self.flip:
            return f'name={self.name},'
        else:
            return f'name=!{self.name},'


class EntityType(Selectors):
    """
    type 标签类，因为该类可以具有多重数值，故设定为需要额外手动添加。
    """
    def __init__(self):
        super().__init__()
        self.type_list = []

    def add_type_judge(self, type_id, flip=False):
        if not flip:
            self.type_list.append(f'type={type_id},')
        else:
            self.type_list.append(f'type=!{type_id},')

    def to_string(self):
        string = ""
        for type_judge in self.type_list:
            string += type_judge
        return string


class Family(Selectors):
    """
    Family 标签类
    """
    def __init__(self, family, flip=False):
        """
        :param family: 族群名字
        :param flip: 是否反选
        """
        super().__init__()
        self.flip = flip
        self.family = family

    def to_string(self):
        if not self.flip:
            return f'family={self.family},'
        else:
            return f'family=!{self.family},'


class Predicate(Selectors):
    """
    Predicate 标签类
    """
    def __init__(self, name_space_id, flip=False):
        """
        :param name_space_id: 命名空间ID
        :param flip: 是否反选
        """
        super().__init__()
        self.flip = flip
        self.name_space_id = name_space_id

    def to_string(self):
        if not self.flip:
            return f'predicate={self.name_space_id},'
        else:
            return f'predicate=!{self.name_space_id},'


class XRotation(Selectors):
    """
    x_rotation 标签类。
    """
    def __init__(self, small_angle=-90, big_angle=90, use_range=True):
        super().__init__()
        self.use_range = use_range

        self.small_angle = small_angle
        # 如果角度在 -90 到 90 的范围外，则重新计算，将角度调整到范围内。
        if small_angle < -90 or small_angle > 90:
            self.small_angle = -(self.small_angle % 360 + 180)
        self.big_angle = big_angle
        if big_angle < -90 or big_angle > 90:
            self.big_angle = -(self.big_angle % 360 + 180)

        if not self.use_range and self.small_angle > self.big_angle:
            self.big_angle = self.small_angle

    def to_string(self):
        if self.use_range:
            if self.small_angle < self.big_angle:
                return f'x_rotation={self.small_angle}..{self.big_angle},'
            else:
                # 注意，如果small_angle和big_angle相等，则默认采用所有大于small_angle的角，而非所有小于big_angle的角。
                return f'x_rotation={self.small_angle}..,'
        else:
            return f'x_rotation={self.big_angle},'


class YRotation(Selectors):
    """
    y_rotation 标签类。
    """

    def __init__(self, small_angle=-90, big_angle=90, use_range=True):
        super().__init__()
        self.use_range = use_range

        self.small_angle = small_angle
        # 如果角度在 -90 到 90 的范围外，则重新计算，将角度调整到范围内。
        if small_angle < -180 or small_angle > 180:
            self.small_angle = self.small_angle % 360
        self.big_angle = big_angle
        if big_angle < -180 or big_angle > 180:
            self.big_angle = self.big_angle % 360

        if not self.use_range and self.small_angle > self.big_angle:
            self.big_angle = self.small_angle

    def to_string(self):
        if self.use_range:
            if self.small_angle < self.big_angle:
                return f'y_rotation={self.small_angle}..{self.big_angle},'
            else:
                # 注意，如果small_angle和big_angle相等，则默认采用所有大于small_angle的角，而非所有小于big_angle的角。
                return f'y_rotation={self.small_angle}..,'
        else:
            return f'y_rotation={self.big_angle},'


class LimitSort(Selectors):
    """
    limit_sort 标签类, 限制数量，同时指定技术方向。
    """
    def __init__(self, limit=1, sort=NEAREST):
        super().__init__()
        self.limit = limit
        self.sort = sort

    def to_string(self):
        return f"limit={self.limit},sort={self.sort},"


class NewClass(LimitSort, XRotation, YRotation, Predicate):
    
    def __init__(self):
        super().__init__()

