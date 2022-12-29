from Command_Access.Execute_Generator.Entities.Area_Effect_Cloud import AreaEffectCloud, CloudTimer
# 尚未完成
from Command_Access.Execute_Generator.Entities.Player import PlayerEntity
# 尚未完成
from Command_Access.Execute_Generator.Entities.Boat import BoatEntity
# 尚未完成
from Command_Access.Execute_Generator.Entities.Armor_Stand import ArmorStandEntity


class EntityBox(object):
    """
    用来安放已经创建的Entity实例。
    """
    def __init__(self):
        self.entity_dict = {}}

    def add_entity(self, entity):
        """
        添加entity实例
        :param entity: 添加的新entity实例。必须是entity类
        """
        self.entity_dict[entity.get_name] = entity

    def get_entity(self, index_name):
        """
        返回具有相应index_name的entity
        :param index_name: 创建entity时，定义的名字。
        """
        if index_name in self.entity_dict.keys():
            return self.entity_dict.get(index_name)
        else:
            return None

    def get_entity_list(self):
        """
        返回盒子中包含的所有entity的index_name
        """
        return self.entity_dict.keys()


        

