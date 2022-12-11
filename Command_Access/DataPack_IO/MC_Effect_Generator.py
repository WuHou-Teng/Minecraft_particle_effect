import os

# 这个文件负责整合一个特效所需的矩阵，并将其打包，递交给MC_Effect_Function_Generator.


class McEffectGenerator(object):

    def __init__(self, new_effect_name):
        self.new_effect_name = new_effect_name
        # 用于装在合成一个特效所需的所有矩阵文件
        self.effect_matrix_list = []
        # 每帧之间的时间间隔（tick）（可调）
        # mc 一秒 = 20 tick
        self.time_interval = 2

    def add_matrix(self, matrix_address):
        """
        添加单独的矩阵文件
        :param matrix_address:
        :return:
        """
        self.effect_matrix_list.append(matrix_address)
        self.effect_matrix_list.append(self.time_interval)

    def add_effect(self, effect_address):
        pass

    def clear_effect_list(self):
        self.effect_matrix_list.clear()

    def set_time_interval(self, new_interval):
        self.time_interval = new_interval

    # TODO 创建新的特效文件夹
    def new_effect_folder(self):
        effect_address = os.path.join(self.data_pack_address, self.effect_name)
        if not os.path.exists(effect_address):
            os.mkdir(effect_address)
        return effect_address
