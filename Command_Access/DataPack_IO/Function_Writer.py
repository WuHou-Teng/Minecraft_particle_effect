import os


class FunctionWriter(object):
    """
    与ParticleEffectFuncGenerator不同，此类单纯是用于创建并写入mcfunction文件的。
    """
    DATA_FOLDER = "\\data\\"
    FUNC_FOLDER = "\\functions"
    FILE_SUFFIX = ".mcfunction"

    def __init__(self, data_pack_address, name_space):
        self.data_pack_address = data_pack_address
        self.name_space = self.DATA_FOLDER + name_space + self.FUNC_FOLDER
        self.full_address = self.data_pack_address + self.name_space

    def change_data_pack_to(self, data_pack_address):
        self.data_pack_address = data_pack_address
        self.full_address = self.data_pack_address + self.name_space

    def change_name_space_to(self, name_space):
        self.name_space = self.DATA_FOLDER + name_space + self.FUNC_FOLDER
        self.full_address = self.data_pack_address + self.name_space

    def func_address(self, func_name):
        """
        函数文件的完整地址
        :param func_name: 函数文件名称
        :return:
            函数文件的完整地址
        """
        return self.full_address + "\\" + func_name + self.FILE_SUFFIX

    def new_func(self, func_name):
        """
        创建新的.mcfunction文件
        :param func_name: 文件名
        :return:
            文件是否创建成功 。如果创建失败，则可能是func已存在。
        """
        func_address = self.func_address(func_name)
        if not os.path.exists(func_address):
            new_file = open(func_address, 'w')
            new_file.close()
            return func_address
        else:
            return False

    def write_func(self, func_name, func_content):
        """
        将内容写入指定函数。如果指定函数文件不存在，则直接创建一个。
        :param func_name: 要写入的函数文件名称
        :param func_content: 要写入的内容
        """
        with open(self.func_address(func_name), 'w') as func_file:
            for each_line in func_content:
                func_file.write(each_line)
            func_file.close()

    def add_func(self, func_name, func_content):
        """
        向原有的mcfunction添加指令
        :param func_name: 要写入的函数文件名称
        :param func_content: 要写入的内容
        """
        with open(self.func_address(func_name), 'a') as func_file:
            for each_line in func_content:
                func_file.write(each_line)
            func_file.close()







