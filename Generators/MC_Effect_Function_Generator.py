import os
from Command_Convertor.Homo_Convertor import HomoConverter


class McEffectFuncGenerator(object):
    """
    粒子特效文件夹生成器。
    """

    # 考虑到未来可能要把很多个基础特效组合起来，变成复合特效。
    def __init__(self, new_effect_name, data_pack_address, matrix_addresses_list, frame_time_interval):
        """
        初始化
        :param new_effect_name: 新特效名称
        :param data_pack_address: 数据包地址
        :param matrix_addresses_list: 要添加的特效空间坐标+颜色矩阵列表。
        """
        self.cwd = os.getcwd()
        # 数据包地址应当一直指向data文件夹内
        # 例如
        # E:\\play_game\\mc\\1.18.2KuaYueII 乙烯\\1.18.2KuaYueII\\.minecraft\\saves\\新的世界 (1)
        # \\datapacks\\partical_effect\\data
        self.data_pack_address = data_pack_address
        # 一个包含了所有需要转换的特效矩阵的列表，该列表来自
        self.matrix_addresses_list = matrix_addresses_list
        # 每帧之间的时间间隔（tick）（可调）
        # mc 一秒 = 20 tick
        self.frame_time_interval = frame_time_interval
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

    # 读取矩阵
    def read_mat(self, mat_file):
        """
        从相应的文件读取位置矩阵
        :param mat_file: 矩阵文件的位置
        :return:
            mat_array: 保存了整个矩阵的列表
        """
        mat_array = []
        with open(mat_file, "w+") as mat:
            mat_data = mat.readlines()
            for particles in mat_data:
                if len(particles) > 0 and particles[0] is not "#":
                    if len(particles.strip().split(',')) == 4:
                        mat_array.append(particles.strip().split(','))
            mat.close()
        return mat_array

# 创建过程：
# 首先添加新文件夹
# 然后添加functions文件夹
# 遍历矩阵列表，对每一个矩阵都视为一帧
# 然后添加新的function，这个新的function可能是单独的帧，也可能是别的function
# 最后写入相应的文件。
#