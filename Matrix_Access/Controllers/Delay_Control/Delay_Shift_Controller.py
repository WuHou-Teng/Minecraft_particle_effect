from Matrix_Access.Controllers.Delay_Control.Delay_Base_Controller import DelayBaseController
from Matrix_Access.Matrix_Const import *
from Matrix_Access.Particles import MCParticle


class DelayShiftController(DelayBaseController):
    """
    单纯的对输入的粒子增加或者减少相应的延时。
    """
    def __init__(self, index_name, delay_type=ABSOLUTE, tick_add=0):
        self.tick_add = tick_add
        self.first_particle = True
        super().__init__(index_name, delay_type)

    def process(self, particle):
        """
        增加或减少粒子延时
        :param particle:
        :return:
        """
        assert type(particle) is MCParticle
        if self.delay_type is ADDITIONAL:
            # 如果计时方式为累加，只需要在第一个数字上增减即可。
            # 该过程是否会出现负数无关紧要，因为最终转换都会转换为绝对时间轴，如果出现负数，则直接设定为0
            if self.first_particle:
                particle.delay += self.tick_add
                self.first_particle = False
            return particle
        elif self.delay_type is ABSOLUTE:
            # 绝对时间轴，则依次加上即可。
            particle.delay += self.tick_add
            if particle.delay < 0:
                particle.delay = 0
            return particle

    def clear_record(self):
        self.first_particle = True


class DelayCountShiftController(DelayShiftController):
    """
    根据处理粒子的数量逐渐增加延时。
    """
    def __init__(self, index_name, delay_type=ABSOLUTE, tick_add=0, particle_count_step=1):
        self.particle_count_step = particle_count_step
        self.current_particle_index = -1
        self.last_delay = 0
        self.tick_actual_add = tick_add * particle_count_step
        self.tick_shift = -1 * self.tick_actual_add
        super().__init__(index_name, delay_type, tick_add)

    def process(self, particle):
        self.current_particle_index += 1
        assert type(particle) is MCParticle
        if self.delay_type is ADDITIONAL:
            # 如果计时方式为累加，只需要在第一个数字上增减即可。
            # 该过程是否会出现负数无关紧要，因为最终转换都会转换为绝对时间轴，如果出现负数，则直接设定为0
            if self.current_particle_index == self.particle_count_step:
                particle.delay += self.tick_add
                self.last_delay = particle.delay
                self.current_particle_index = 0

            return particle
        elif self.delay_type is ABSOLUTE:
            # 绝对时间轴，则依次加上即可。
            if self.current_particle_index == self.particle_count_step:
                self.current_particle_index = 0
                self.tick_shift += self.tick_add

            particle.delay = particle.delay + self.tick_actual_add + self.tick_shift
            if particle.delay - self.last_delay > self.tick_add:
                self.tick_shift -= self.tick_add
                particle.delay -= self.tick_add
            self.last_delay = particle.delay
            # print(f"添加的数字: {self.tick_actual_add + self.tick_shift}")

            if particle.delay < 0:
                particle.delay = 0

            return particle

    def process_matrix(self, matrix_accesser):
        pass

    def clear_record(self):
        self.history_particle_index = 0
        self.current_particle_index = 0
