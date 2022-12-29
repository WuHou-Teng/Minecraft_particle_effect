

class EffectBox(object):
    """
    # TODO 用来装载多种effect，或者隐藏effect的盒子，最终作为 Effect tag 放到需要的药水或者实体上，
    """
    def __init__(self):
        pass


class Effect(object):
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


class HiddenEffect(Effect):
    """
    这个类属于Effect的子类。参数基本相同。
    """
    def __init__(self):
        super().__init__()
        pass


