from util.Box import Box
from Matrix_Access.Matrix_Accesser import MatrixAccesser


class MatrixAccessBox(Box):

    def __init__(self):
        super().__init__()
        self.matrix_dict = {}

    def add_matrix_accesser(self, matrix_accesser):
        """
        添加Controller实例
        :param matrix_accesser: 添加新的 matrix_accesser实例。类型为 MatrixAccesser
        """
        self.matrix_dict[matrix_accesser.get_name()] = matrix_accesser
        return matrix_accesser.get_name()

    def get_matrix_accesser(self, index_name):
        """
        返回矩阵访问器中保存的矩阵文件名称。
        :param index_name: 矩阵访问器中保存的矩阵文件名称。
        """
        if index_name in self.matrix_dict.keys():
            return self.matrix_dict.get(index_name)
        else:
            return None

    def get_matrix_accesser_list(self):
        """
        返回盒子中包含的所有matrix_accesser 的 矩阵文件名称。
        """
        return list(self.matrix_dict.keys())

    def get_object_list(self):
        return self.get_matrix_accesser_list()

    def add_object(self, new_object):
        return self.add_matrix_accesser(new_object)

    def get_object(self, index_name):
        return self.get_matrix_accesser(index_name)

    def new_matrix_accesser(self, matrix_file_name):
        self.add_matrix_accesser(MatrixAccesser(matrix_file_name))


