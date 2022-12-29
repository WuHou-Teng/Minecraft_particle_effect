from Command_Access.Execute_Generator.Selector.Selector_Const import *
from Command_Access.Execute_Generator.Selector import Selectors
from Command_Access.Execute_Generator.Entities import Entity


class TargetSelectorBox(object):
    """
    参考 ControllerToolBox, 为所有Selectors编写添加函数。方便用户调用
    """
    def __init__(self, index_name, entity_mark=NEAREST_PLAYER, entity=None):
        self.index_name = index_name
        self.entity_mark = entity_mark
        self.entity = entity
        self.selector_list = []

    def get_name(self):
        return self.index_name

    def add_tag(self, selector):
        assert selector.__class__.__base__ == Selectors
        self.selector_list.append(selector.to_string())

    def set_entity(self, entity):
        """
        添加实体, 后续 to_string()会向实体请求 nbt 信息方便execute锁定实体对象。
        :param entity: 是实体类或者是实体类的子类。
        :return:
        """
        # assert entity.__class__.__base__ == Entity
        self.entity = entity
        # self.selector_list.append(entity.to_string_select())

    def to_string(self):
        """
        将所有的选择器tag转换为一句可以直接放入execute的选择器语句。
        每次调用 to_string 都会重新向entity请求一次 to_string_select(), 因此可以做到更新entity数据。
        注：另外，如果想要控制实体的 to_string_select()不返回部分tag，只要将实体的那一项tag直接设定为 None.
        # TODO 其实我觉得这里在未来，将所有的tag都写成tag后，还是最好加一个白名单作为过滤器。
        # 否则通过将实体的某一项设定为 None来避免实体 to_string_select()不返回相应tag的操作还是隐式了。
        :return:
            selector_string = [type=...,distance=...] 等。
        """
        selector_string = self.entity_mark + "["
        for selectors in self.selector_list:
            selector_string += selectors
        if self.entity is not None:
            selector_string += self.entity.to_string_select()
        return selector_string + "]"

    def location(self, x=0, y=0, z=0,
                 x_coo_type=RELA_COORD, y_coo_type=RELA_COORD, z_coo_type=RELA_COORD):
        return Selectors.Location(x, y, z, x_coo_type, y_coo_type, z_coo_type)

    def distance(self, max_distance=0, min_distance=0, use_range=True):
        return Selectors.Distance(max_distance, min_distance, use_range)

    def vol_space(self, dx=0, dy=0, dz=0):
        return Selectors.VolSpace(dx, dy, dz)

    def score(self, score_name=None, score_min_value=None, score_max_value=None, use_range=None):
        score_select = Selectors.Scores()
        if score_name is not None and score_min_value is not None and score_max_value is not None:
            if use_range is None:
                use_range = False
            score_select.add_score(score_name, score_min_value, score_max_value, use_range)
        return score_select

    def tag(self, tag, flip=False):
        return Selectors.Tag(tag, flip)

    def team(self, team, flip=False):
        return Selectors.Team(team, flip)

    def name(self, name, flip=False):
        return Selectors.Name(name, flip)

    def entity_type(self, type_id=None, flip=None):
        type_select = Selectors.EntityType()
        if type_id is not None:
            if flip is None:
                flip = False
            type_select.add_type_judge(type_id, flip)
        return type_select

    def family(self, family_type, flip=False):
        return Selectors.Family(family_type, flip)

    def predicate(self, name_space_id, flip=False):
        return Selectors.Predicate(name_space_id, flip)

    def x_rotation(self, small_angle=-90, big_angle=90, use_range=True):
        return Selectors.XRotation(small_angle, big_angle, use_range)

    def y_rotation(self, small_angle=-180, big_angle=180, use_range=True):
        return Selectors.YRotation(small_angle, big_angle, use_range)

    def limit_sort(self, limit=1, sort=NEAREST):
        return Selectors.LimitSort(limit, sort)


# ————————————————————以下类弃用，改用上面的。————————————————————————
class TargetSelector(object):
    """
    在execute指令中，对象后往往需要添加相应的描述限制。
    例如 execute as @e[type=minecraft:item, distance=0..5, nbt={Item:{id:"minecraft:blaze_powder"}, OnGround:1b}] run...
    其中[type=minecraft:item, distance=0..5, nbt={Item:{id:"minecraft:blaze_powder"}, OnGround:1b}] 就是条件限制。
    该类是创建/添加条件限制的基类。
    """
    def __init__(self, entity_mark=ALL_ENTITY, location=None, distance=None, vol_space=None,
                 scores=None, tag=None, team=None, name=None, entity_type=None, family=None,
                 predicate=None, x_rotation=None, y_rotation=None, entity_NBT=None, limit=None, sort=None):
        """

        :param entity_mark: @a: 所有玩家
                            @p: 最近玩家
                            @s: 目前实体
                            @e: 所有实体
                            @r: 任意玩家

        :param location: (x, y, z) 具体位置

        :param distance: 根据到某点的欧几里得距离过滤目标。只允许使用非负数。<Distance>
                         @e[distance=10..12] — 选择所有距离执行位置大于等于10，且小于等于12个方块的实体。

        :param vol_space: [dx=<值>,dy=<值>,dz=<值>] — 选择所有位于一定长方体区域内部的目标。体积定义为从基准点开始，
                          向“X”方向（东方）延伸dx格（包括基准点本身，下同），
                          向“Y”方向（上方）延伸dy格，
                          并向“Z”方向（南方）延伸dz格。如果只指定了其中的部分参数，那么剩余的参数默认为0。

        :param scores: [scores={<记分项>=<值>,...}] — 根据指定目标的分数过滤目标。
                       所有的记分项都放在一个单独的标签中，并这个标签中分别列出分数选择器。
                       此选择器支持使用范围，在基岩版中，还可使用不等号（=!） <Score>

        :param tag: [tag=[<标签名>] — 选择所有有标签“标签名”的目标。
                    [tag=!<标签名>] — 选择所有没有标签“标签名”的目标。
                    [tag=] — 选择所有没有标签的目标。
                    [tag=!] — 选择所有有标签的目标。

        :param team: [team=<某队伍>] — 选择所有属于队伍“某队伍”的目标。
                     [team=!<某队伍>] — 选择所有不属队伍“某队伍”的目标。
                     [team=] — 选择所有不属于任何队伍的目标。
                     [team=!] — 选择所有属于任意队伍的目标。

        :param name:实体名称
                    [name=<某名称>] — 选择所有名字为“某名称”的目标。
                    [name=!<某名称>] — 选择所有名字不为“某名称”的目标。

        :param entity_type: [type=<实体类型>] — 选择所有特定的实体类型的目标。
                            [type=!<实体类型>] — 选择所有不是特定的实体类型的目标。

        :param family: [family=<族>] — 选择属于指定的族的实体。
                       [family=!<族>] — 选择不属于指定的族的实体。
                       原版行为包使用的默认值包括：
                            更广泛的大型族（例如mob、inanimate、monster、undead）
                            更具体的小型族（例如zombie、skeleton）
                            单个生物的族（例如wandering_trader、enderman、creeper）
                            与生成事件有挂钩的族（例如farmer、baby_turtle）

        :param predicate: [predicate=<命名空间ID>] — 选择所有匹配该谓词的目标。
                          [predicate=!<命名空间ID>] — 选定所有不匹配该谓词的目标。

        :param x_rotation: [x_rotation=<值>] — 根据指定目标的垂直旋转角度过滤目标。

        :param y_rotation: [y_rotation=<值>] — 根据指定目标的水平旋转角度过滤目标。

        :param entity_NBT: [nbt={NBT}] — 选择具有指定NBT的所有目标。NBT结构以其命令定义编写。

        :param limit: [limit=<值>] — 仅选择指定数量的目标。
        :param sort: 排序方式，有最近（NEAREST），最远（FURTHEST），随机（RANDOM），时间先后（ARBITRARY）四种。
                     [limit=<值>,sort=(nearest|furthest|random|arbitrary)] — 选择指定数量的目标，并指定优先级。
        """

        self.entity_mark = entity_mark
        self.location = location
        self.distance = distance
        self.vol_space = vol_space
        self.scores = scores
        self.tag = tag
        self.team = team
        self.name = name
        self.entity_type = entity_type
        self.family = family
        self.predicate = predicate
        self.x_rotation = x_rotation
        self.y_rotation = y_rotation

        self.limit = limit
        self.sort = sort

        # 实体标签信息，通过添加一个实体nbt一次性添加。是一个列表，包含多段字符串
        self.entity_NBT = entity_NBT

        self.condition = []

    def add_entity_info(self, entity_NBT):
        """
        :param entity_NBT: <dictionary>
        """
        self.entity_NBT = entity_NBT

    def get_condition(self):
        """
        直接返回已有的条件列表。
        :return:
            self.condition: 已有的条件列表
        """
        return self.condition

    def to_string(self):
        """
        将condition转换为字符串的形式，方便镶嵌到指令中
        :return:
        """
        string = "["
        for cond in self.condition:
            string += cond
        string += "]"
        return string

    def add_condition(self, new_condition):
        """
        添加新的条件。
        :param new_condition:
        :return:
        """
        self.condition.append(new_condition)

    def has_condition(self):
        return True if len(self.get_condition()) > 0 else False

    # TODO 这里我觉得以后还要根据不一样的对象添加条件。例如玩家，实体，或者item，都有各自特有的条件词缀。

