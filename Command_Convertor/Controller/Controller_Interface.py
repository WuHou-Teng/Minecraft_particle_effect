

class Controller(object):
    """
    所有 Controller类的函数接口。
    所有 Controller本质上都是在转换器将粒子矩阵转换前，对粒子信息的处理。
    因此，都是输入粒子信息，然后返回处理后的粒子信息，当然也可以返回 None, 意味着此后的处理链无需继续进行。跳过这个粒子。
    """
    def __init__(self):
        pass

    def process(self, particle):
        """
        对所有 Controller最终功能的封装。概述为：输入粒子，修改粒子参数，然后输出粒子。
        :param particle: 粒子信息，标准格式为：
        x, y, z, d_x, d_y, d_z, speed, count, force_normal, Color(R, G, B),   color_transfer(R,G,B), particle_type
        1, 1, 1, 0,   0,   0,   0,     1,     f/n,          0.05-1, 0-1, 0-1, 0.05-1, 0-1, 0-1,      0(Undefined)
        :return:
            particle: 经过处理后的粒子信息
        """
        pass

    def to_string(self):
        """
        将 Controller所拥有的功能概述为一句话。
        :return:
            string: 自身功能，例如，<粒子控制器: 根据颜色修改粒子类型。>
        """
        pass

    def to_string_full(self):
        """
        对 Controller所拥有的功能的详细描述。
        :return:
            string: 自身功能详细描述，例如，<粒子控制器: 根据颜色修改粒子类型。(1,1,1):end_rod, (0.001,0,0):end_chest>
        """
        pass
