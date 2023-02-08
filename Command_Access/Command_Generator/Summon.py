from Command_Access.Command_Generator.Selector.Selector_Const import RELA_COORD, FACE_COORD, ABS_COORD


class SummonBuilder(object):
    """
    用于创建 Summon 指令相关。
    """
    def __init__(self, entity):
        """
        简而言之，需要一个实体的实际
        :param entity:
        """
        self.entity = entity
        self.coo_type = [RELA_COORD, RELA_COORD, RELA_COORD]
        self.coo_dict = {RELA_COORD: "~", FACE_COORD: "^", ABS_COORD: ""}

    def summon_entity(self, x=None, y=None, z=None, x_coo_type=RELA_COORD, y_coo_type=None, z_coo_type=None):
        """
        创建 summon 指令，一般用于作为粒子特效实体载体。
        :param x: x方向位置
        :param y: y方向位置
        :param z: z方向位置
        :param x_coo_type: x轴坐标模式
        :param y_coo_type: y轴坐标模式
        :param z_coo_type: z轴坐标模式
        :return:
        """
        if y_coo_type is None:
            y_coo_type = x_coo_type
        if z_coo_type is None:
            z_coo_type = x_coo_type
        x_sign = self.coo_dict.get(x_coo_type)
        y_sign = self.coo_dict.get(y_coo_type)
        z_sign = self.coo_dict.get(z_coo_type)
        nbt, entity_type, pos = self.entity.to_string_summon_nbt()
        if x is None:
            x = pos[0]
        if y is None:
            y = pos[1]
        if z is None:
            z = pos[2]
        return f'summon {entity_type} {x_sign}{x} {y_sign}{y} {z_sign}{z} {nbt}'
