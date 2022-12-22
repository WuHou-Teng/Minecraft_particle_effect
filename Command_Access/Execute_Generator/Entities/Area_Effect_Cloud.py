from Command_Access.Execute_Generator.Entities.Entity import EntityBuilder
from Command_Access.Const.Particles_Java import *
from Command_Access.Execute_Generator.Entities.Entity_Const import AREA_EFFECT_CLOUD


class AreaEffectCloud(EntityBuilder):
    """
    效果云实体的创建。
    """

    def __init__(self, Tag=None, Age=None, Color=None, Duration=None, ReapplicationDelay=None,
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
        self.type = AREA_EFFECT_CLOUD

        super(AreaEffectCloud).__init__(Tags=Tag)
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

    def to_string(self):
        for keys in list(self.tag_dict.keys()):
            if self.tag_dict.get(keys) is not None:
                # TODO 添加到列表。不过这里tag部分是float类，得做区分。
                pass



class CloudTimer(AreaEffectCloud):
    """
    TODO 专门用于计时的标准效果云。
    最短的计时器。
    /summon minecraft:area_effect_cloud ~ -10 ~ {Tags:["try"], Duration:200, Age:0"}
    """

    def __init__(self, tag, age, duration):
        super(CloudTimer).__init__()
        self.age = age
        self.duration = duration

        # 默认具体位置为0，-10，0
        self.pos_x = 0
        self.pos_y = -10
        self.pos_z = 0


class EffectTag(object):
    """
    Effect tag 比较复杂，单独拿出来：
    Effects：施加状态效果的列表。
        ：某个独立的状态效果。
        状态效果[]
        Ambient：表示状态效果是否是被信标添加的。
        Amplifier：状态效果的等级。0表示等级1，以此类推。
        Duration：距离效果失效的时间刻数。
        FactorCalculationData：计算状态效果因子的数据，这些数据主要影响渲染效果。可能不存在。
            effect_changed_timestamp：渲染效果改变的时间。不小于0。
            factor_current：因子的当前值。
            factor_previous_frame：上一帧的因子值。
            factor_start：因子的起始值。
            factor_target：因子的结束值。
            had_effect_last_tick：在此刻之前是否有渲染效果。
            padding_duration：渲染效果的时间周期。不小于0。
        * HiddenEffect：相同类型的更低等级的状态效果，会在外层的效果过期后取代它。位于这里的状态效果的距离失效的刻数仍然会减少。可能不存在。
        Id：效果ID。
        ShowIcon：表示是否显示状态效果的图标。
        ShowParticles：表示是否显示粒子效果。
    """
    def __init__(self):
        pass


class HiddenEffectTag(EffectTag):
    """
    这个类属于Effect的子类。参数基本相同。
    """
    def __init__(self):
        super().__init__()
        pass
