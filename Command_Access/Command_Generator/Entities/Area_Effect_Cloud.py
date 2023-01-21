from Command_Access.Command_Generator.Entities.Entity import EntityBuilder
from Command_Access.Const.Particles_Java import *
from Command_Access.Command_Generator.Entities.Entity_Const import AREA_EFFECT_CLOUD
from Command_Access.Command_Generator.Effects.Effect_Box import EffectBox


class AreaEffectCloud(EntityBuilder):
    """
    效果云实体的创建。
    """

    def __init__(self,index_name, Tag=None, Age=None, Color=None, Duration=None, ReapplicationDelay=None,
                 WaitTime=None, DurationOnUse=None, Owner=None, Radius=None, RadiusOnUse=None,
                 RadiusPerTick=None, Particle=None, Potion=None, Effects=None):
        """
        初始化，包含所有可能需要的参数
        :param Tag: 自定义的记分板标签数据。可能不存在。
        :param Age: 效果区域的已持续时间。
        :param Color: 效果区域粒子的颜色。使用与显示属性中color标签相同的格式。
        :param Duration: 效果区域的最长持续时间。效果区域的持续时间超过此值时消失，无论其半径为何。
        :param ReapplicationDelay: 再次施加状态效果的冷却倒计时，以刻为单位。
        :param WaitTime: 再次施加状态效果的冷却倒计时，以刻为单位。
        :param DurationOnUse: 效果区域生效前的等待时间。在已持续时间未到达此时间前，效果区域不施加状态效果。
        :param Owner: 效果区域创建者的UUID，以四个整数的数组形式存储。可能不存在。
        :param Radius: 效果区域的半径。
        :param RadiusOnUse: 施加状态效果后效果区域半径的改变量。正常情况下为负值。
        :param RadiusPerTick: 效果区域半径每刻的改变量。正常情况下为负值。
        :param Particle: 组成效果区域的粒子，此字符串的格式与particle命令中的格式相同。
        :param Potion: 默认药水效果的名称，有效的ID请参见药水数据值。可能不存在。
        :param Effects: 施加状态效果的列表。
        """
        # 效果云实体，所以类型为AREA_EFFECT_CLOUD

        super().__init__(index_name=index_name, Tags=Tag)
        self.entity_type = AREA_EFFECT_CLOUD
        self.Age = Age
        self.Color = Color
        self.Duration = Duration
        self.ReapplicationDelay = ReapplicationDelay
        self.WaitTime = WaitTime
        self.DurationOnUse = DurationOnUse
        self.Owner = Owner
        self.Radius = Radius
        self.RadiusOnUse = RadiusOnUse
        self.RadiusPerTick = RadiusPerTick
        self.Particle = Particle
        self.Potion = Potion
        # TODO EffectBox类见: <Command_Access.Command_Generator.Effects.Effect_Box>
        self.Effects = Effects

        self.update_value("Age", self.Age)
        self.update_value("Color", self.Color)
        self.update_value("Duration", self.Duration)
        self.update_value("ReapplicationDelay", self.ReapplicationDelay)
        self.update_value("WaitTime", self.WaitTime)
        self.update_value("DurationOnUse", self.DurationOnUse)
        self.update_value("Owner", self.Owner)
        self.update_value("Radius", self.Radius)
        self.update_value("RadiusOnUse", self.RadiusOnUse)
        self.update_value("RadiusPerTick", self.RadiusPerTick)
        self.update_value("Particle", self.Particle)
        self.update_value("Potion", self.Potion)
        self.update_value("Effects", self.Effects)

    def update_self_value(self):
        self.update_value("Age", self.Age)
        self.update_value("Color", self.Color)
        self.update_value("Duration", self.Duration)
        self.update_value("ReapplicationDelay", self.ReapplicationDelay)
        self.update_value("WaitTime", self.WaitTime)
        self.update_value("DurationOnUse", self.DurationOnUse)
        self.update_value("Owner", self.Owner)
        self.update_value("Radius", self.Radius)
        self.update_value("RadiusOnUse", self.RadiusOnUse)
        self.update_value("RadiusPerTick", self.RadiusPerTick)
        self.update_value("Particle", self.Particle)
        self.update_value("Potion", self.Potion)
        self.update_value("Effects", self.Effects)

    def set_default(self, Tag=None, Age=0, Color=None, Duration=200, ReapplicationDelay=20,
                    WaitTime=0, DurationOnUse=-10, Owner=None, Radius=2, RadiusOnUse=-0.1,
                    RadiusPerTick=-0.01, Particle=None, Potion=None, Effects=None):
        self.Age = Age
        self.Color = Color
        self.Duration = Duration
        self.ReapplicationDelay = ReapplicationDelay
        self.WaitTime = WaitTime
        self.DurationOnUse = DurationOnUse
        self.Owner = Owner
        self.Radius = Radius
        self.RadiusOnUse = RadiusOnUse
        self.RadiusPerTick = RadiusPerTick
        self.Particle = Particle
        self.Potion = Potion
        self.Effects = Effects

        self.update_self_value()

    def to_string_nbt(self):
        nbt_str = "{"

        for keys in list(self.tag_dict.keys()):
            if self.tag_dict.get(keys) is not None:
                if keys == "Tags":
                    new_tag = f'{keys}:[\"{self.tag_dict.get(keys)}\"]'
                else:
                    new_tag = f'{keys}:{self.tag_dict.get(keys)}'
                # TODO 这里直接用穷举，手动添加 ”，“ 显然是偷懒的。预期正式的指令生成器会将所有的tag都写成类。
                if keys == "Radius" or keys == "RadiusOnUse" or keys == "RadiusPerTick":
                    new_tag += 'f'
                if keys == "Pos":
                    continue
                if keys == "Particle":
                    new_tag = f'{keys}:\"{particle_dict.get(self.tag_dict.get(keys)).strip()}\"'
                nbt_str += new_tag
                nbt_str += ","
        nbt_str += '}'
        return nbt_str

    def to_string_select_nbt(self):
        nbt_str = self.to_string_nbt()
        return "nbt=" + nbt_str, self.entity_type

    def to_string_select(self):
        return f'type={self.entity_type},nbt={self.to_string_nbt()},'

    def to_string_summon_nbt(self):
        if self.Pos is None:
            self.Pos = (0, 0, 0)
        return self.to_string_nbt(), self.entity_type, self.Pos

    def to_string_summon(self):
        if self.Pos is None:
            self.Pos = (0, 0, 0)
        return f'summon {self.entity_type} ~{self.Pos[0]} ~{self.Pos[1]} ~{self.Pos[2]} {self.to_string_nbt()}'


class CloudTimer(AreaEffectCloud):
    """
    专门用于计时的标准效果云。
    最短的计时器。
    /summon minecraft:area_effect_cloud ~ -10 ~ {Tags:["try"], Duration:200, Age:0"}
    """

    def __init__(self, index_name, Tag, Age, Duration, Radius=None, RadiusPerTick=None, Particle=None):

        # self.Age = Age
        # self.Duration = Duration
        super().__init__(index_name=index_name, Tag=Tag, Age=Age, Duration=Duration, Radius=Radius,
                         RadiusPerTick=RadiusPerTick, Particle=Particle)
        # 默认具体位置为0，0，0
        self.Pos = (0, 0, 0)
        # self.update_self_value()

    def ticks_past(self, ticks):
        if self.Age + ticks > self.Duration:
            print("时间超过计时器长度，请重新设定计时器。")
        self.Age += ticks
        self.tag_dict["Age"] = self.Age

    def second_past(self, second):
        if self.Age + second*20 > self.Duration:
            print("时间超过计时器长度，请重新设定计时器。")
        self.Age += round(second*20)
        self.tag_dict["Age"] = self.Age

    def set_age_ticks(self, ticks):
        """
        直接设定Age的tick数量，因为考虑到某些matrix可能并非按照时间排序。
        :param ticks:
        :return:
        """
        self.Age = ticks
        self.tag_dict["Age"] = self.Age

    def to_string_select_no_age(self):
        """
        这里唯一的区别就是，在选择器中不会添加 Age 标签，方便迭代指令更宽泛的锁定目标。
        :return:
        """
        nbt_str = "{"
        for keys in list(self.tag_dict.keys()):
            if self.tag_dict.get(keys) is not None:
                if keys == "Tags":
                    new_tag = f'{keys}:[\"{self.tag_dict.get(keys)}\"]'
                else:
                    new_tag = f'{keys}:{self.tag_dict.get(keys)}'
                if keys == "Radius" or keys == "RadiusOnUse" or keys == "RadiusPerTick":
                    new_tag += 'f'
                if keys == "Pos" or keys == "Age":
                    continue
                if keys == "Particle":
                    new_tag = f'{keys}:\"{particle_dict.get(self.tag_dict.get(keys)).strip()}\"'
                nbt_str += new_tag
                nbt_str += ","
        nbt_str += '}'
        return f'type={self.entity_type},nbt={nbt_str},'


if __name__ == "__main__":
    # new_cloud = CloudTimer("wuhou", Age=0, Duration=200)
    # print(new_cloud.to_string_summon())
    new_timer = CloudTimer("start1", "start1", 0, 200, Particle=end_rod, Radius=3)
    print(new_timer.to_string_summon())
    for time in range(0, 200, 10):
        new_timer.ticks_past(50)
        print(new_timer.to_string_select())

