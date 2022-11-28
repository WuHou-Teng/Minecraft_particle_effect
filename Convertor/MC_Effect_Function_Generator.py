import os
from Convertor.Binary_Convertor import BinConverter


class McEffectGenerator(object):
    """
    粒子特效文件夹生成器。
    """

    def __init__(self, new_effect_name, data_pack_address, matrix_list_address):
        """
        初始化
        :param new_effect_name: 新特效名称
        :param data_pack_address: 数据包地址
        :param matrix_list_address: 要添加的特效空间坐标+颜色矩阵列表。
        """
        self.cwd = os.getcwd()
        # 数据包地址应当一直指向data文件夹内
        # 例如
        # E:\\play_game\\mc\\1.18.2KuaYueII 乙烯\\1.18.2KuaYueII\\.minecraft\\saves\\新的世界 (1)
        # \\datapacks\\partical_effect\\data
        self.data_pack_address = data_pack_address
        # 一个特效的矩阵文件列表地址
        self.matrix_list_address = matrix_list_address
        # 每帧之间的时间间隔（tick）（可调）
        # mc 一秒 = 20 tick
        self.frame_time_interval = 2
        # 新的特效名称
        self.effect_name = new_effect_name

    # 创建新的特效文件夹
    def new_effect_folder(self):
        effect_address = os.path.join(self.data_pack_address, self.effect_name)
        if not os.path.exists(effect_address):
            os.mkdir(effect_address)
        return effect_address

    # 创建对应的特效文件夹
    def new_effect_func_folder(self, effect_address):
        new_effect_functions_folder = os.path.join(effect_address, "functions")
        if not os.path.exists(new_effect_functions_folder):
            os.mkdir(new_effect_functions_folder)
        return new_effect_functions_folder

    # 创建新的.mcfunction文件
    def new_main_function(self, func_name):
        pass

    # 创建新的帧
    def new_frame(self):
        pass

    # 修改指向的特效名称
    def set_effect_name(self, new_effect_name):
        self.effect_name = new_effect_name


# 创建过程：
# 首先添加新文件夹
# 然后添加functions文件夹
# 遍历矩阵列表，对每一个矩阵都视为一帧
# 然后添加新的function，这个新的function可能是单独的帧，也可能是别的function
# 最后写入相应的文件。
#