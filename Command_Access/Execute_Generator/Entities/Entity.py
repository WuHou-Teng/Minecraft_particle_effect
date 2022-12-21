

class EntityBuilder(object):
    """
    mc实体的抽象类，包含部分实体通用标签。
    """
    def __init__(self, Air=None, CustomName=None, CustomNameVisible=None, FallDistance=None,
                 Fire=None, Glowing=None, HasVisualFire=None, Invulnerable=None, Motion=None,
                 NoGravity=None, OnGround=None, Passengers=None, PortalCooldown=None, Pos=None,
                 Rotation=None, Silent=None, Tags=None, TicksFrozen=None, UUID=None):
        """

        :param Air: 当前实体所剩的空气值。在空气中充满至300，折算为生物淹没在水中15秒后生物才开始窒息，
                    如该实体生命值为20点，那么实体在35秒后才会死亡。如果此项小于等于0时实体在水中，那么其每秒会受到1点伤害。
        :param CustomName: 当前实体的自定义名称的JSON文本。
                    会出现在玩家的死亡信息与村民的交易界面，以及玩家的光标指向的实体的上方。可能不存在。
        :param CustomNameVisible: 如果为true且实体拥有自定义名称，那么名称会总是显示在它们上方，而不受光标指向的影响。
                    若实体并没有自定义名称，显示的则是默认的名称。可能不存在。
        :param FallDistance: 当前实体已经坠落的距离。值越大，实体落地时对其造成伤害更多。
        :param Fire: 距离火熄灭剩余的时间刻数。负值表示当前实体能够在火中站立而不着火的时间，未着火时默认为-20。
        :param Glowing: 表示实体是否有发光的轮廓线。可能不存在。
        :param HasVisualFire: 如果为true，那么实体会看起来已着火，但实际上可能未着火。可能不存在。
        :param Invulnerable: 如果为true，那么当前实体不会受到除虚空伤害外的任何伤害，但这些实体仍然会被处于创造模式的玩家伤害到。
                    此项对于生物与非生物实体的作用是类似的：生物不会受到任何来源（包括药水）的伤害，
                    无法被钓鱼竿、攻击、爆炸或者抛射物推动；除支持物被移除外，诸如载具的物件都不会被摧毁。
        :param Motion: 当前实体的速度，单位是米/每刻。(x, y, z)
                    ：X轴速度分量。
                    ：Y轴速度分量。
                    ：Z轴速度分量。
        :param NoGravity: 如果为true，实体在空中不会坠落，在盔甲架上的效果却是使 Motion标签将失去效果。可能不存在。
        :param OnGround: 表示实体是否正在接触地面。
        :param Passengers: 正在骑乘当前实体的实体的数据。两个实体都能控制移动，被刷怪笼召唤时生成条件由最上方的实体决定。
        :param PortalCooldown: 距离当前实体可以再次穿过下界传送门向回传送的时间刻数。在初次传送后，起始值为300刻（15秒）并逐渐倒计时至0。
        :param Pos: 当前实体的坐标。(x, y, z)
                    ：X轴坐标。
                    ：Y轴坐标。
                    ：Z轴坐标。
        :param Rotation: 实体的旋转角度。
                    ：当前实体以Y轴为中心，俯视时顺时针的角度（即偏转角）。正南方为0。不会超过360度。
                    ：当前实体与水平面之间的倾斜角（即俯仰角）。水平面为0，正值表示面朝下方，相反则为上方。不超过正负90度。
        :param Silent: 表示当前实体是否不会发出任何声音。可能不存在。
        :param Tags: 自定义的记分板标签数据。可能不存在。
        :param TicksFrozen: 实体的冷冻时间，不小于0。当实体在细雪中时每刻增加1，离开细雪则每刻减少2。可能不存在。
        :param UUID: 实体的UUID，用4个32位整数表示，按从高位到低位的顺序存储。
        """
        # 实体自身种类设定为None。因为该类是基类。
        self.type = None

        self.Air = Air
        self.CustomName = CustomName
        self.CustomNameVisible = CustomNameVisible
        self.FallDistance = FallDistance
        self.Fire = Fire
        self.Glowing = Glowing
        self.HasVisualFire = HasVisualFire
        self.Invulnerable = Invulnerable
        self.Motion = Motion
        self.NoGravity = NoGravity
        self.OnGround = OnGround
        self.Passengers = Passengers
        self.PortalCooldown = PortalCooldown
        self.Pos = Pos
        self.Rotation = Rotation
        self.Silent = Silent
        self.Tags = Tags
        self.TicksFrozen = TicksFrozen
        self.UUID = UUID

        # 创建字典，将所有的标签塞进去。
        # TODO 增加一个词典是有意义的。方便传递数据，以及遍历。不过，可能要考虑，是否应该直接将原始数据丢尽dict，还是处理后丢尽dict。
        self.tag_dict = {}
        self.update_self_value()

    def update_self_value(self):
        self.update_value("Air", self.Air)
        self.update_value("CustomName", self.CustomName)
        self.update_value("CustomNameVisible", self.CustomNameVisible)
        self.update_value("FallDistance", self.FallDistance)
        self.update_value("Fire", self.Fire)
        self.update_value("Glowing", self.Glowing)
        self.update_value("HasVisualFire", self.HasVisualFire)
        self.update_value("Invulnerable", self.Invulnerable)
        self.update_value("Motion", self.Motion)
        self.update_value("NoGravity", self.NoGravity)
        self.update_value("OnGround", self.OnGround)
        self.update_value("Passengers", self.Passengers)
        self.update_value("PortalCooldown", self.PortalCooldown)
        self.update_value("Pos", self.Pos)
        self.update_value("Rotation", self.Rotation)
        self.update_value("Silent", self.Silent)
        self.update_value("Tags", self.Tags)
        self.update_value("TicksFrozen", self.TicksFrozen)
        self.update_value("UUID", self.UUID)

    def set_default(self):
        """
        将部分数据设定为默认值。
        """
        self.Air = 300
        self.CustomName = None
        self.CustomNameVisible = False
        self.FallDistance = 0
        self.Fire = -20
        self.Glowing = False
        self.HasVisualFire = False
        self.Invulnerable = False
        self.Motion = (0, 0, 0)
        self.NoGravity = False
        self.OnGround = False
        self.Passengers = None
        self.PortalCooldown = 300
        self.Pos = (0, 0, 0)
        self.Rotation = (0, 0)
        self.Silent = False
        self.Tags = None
        self.TicksFrozen = None
        self.UUID = None
        self.update_self_value()

    def update_value(self, key, value):
        """
        更新，或者添加新的属性。
        :param key:
        :param value:
        :return:
        """
        self.tag_dict[key] = value

    def to_sting(self):
        """
        将自身的属性写成nbt值。
        其中，如果属性为 None, 则默认忽略。所以可以通过有限的设定属性，来获得有限的nbt。
        :return:
        """
        pass




