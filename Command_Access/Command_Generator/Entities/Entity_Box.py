# 已完成。
from Command_Access.Command_Generator.Entities.Area_Effect_Cloud import AreaEffectCloud, CloudTimer
# 尚未完成
from Command_Access.Command_Generator.Entities.Player import PlayerEntity
# 尚未完成
from Command_Access.Command_Generator.Entities.Boat import BoatEntity
# 尚未完成
from Command_Access.Command_Generator.Entities.Armor_Stand import ArmorStandEntity
from util.Box import Box


class EntityBox(Box):
    """
    用来安放已经创建的Entity实例。
    """
    def __init__(self):
        super().__init__()
        self.entity_dict = {}

    def add_entity(self, entity):
        """
        添加entity实例
        :param entity: 添加的新entity实例。必须是entity类
        :return:
            entity的index_name
        """
        self.entity_dict[entity.get_name()] = entity
        return entity.get_name()

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

    def get_object_list(self):
        return self.get_entity_list()

    def add_object(self, new_object):
        return self.add_entity(new_object)

    def get_object(self, index_name):
        return self.get_entity(index_name)

    @staticmethod
    def new_cloud_timer(index_name, tag, age, duration):
        """
        创建新的云计时器
        :param index_name:
        :param tag:
        :param age:
        :param duration:
        :return:
            输出云计时器的 index_name
        """
        new_could_timer = CloudTimer(index_name=index_name, Tag=tag, Age=age, Duration=duration)
        # self.add_entity(new_could_timer)
        return new_could_timer

    # TODO 以后别的实体的快速创建也在这里加上。
        

