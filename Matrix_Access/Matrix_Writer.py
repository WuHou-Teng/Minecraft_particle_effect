import os


class MatrixWriter(object):
    """
    该类用于新建矩阵文件，或者写入已有矩阵文件
    """

    def __init__(self, matrix_file):
        self.cwd = os.getcwd()
        # 粒子矩阵文件名称或绝对地址。如果仅仅提供了名称，程序会自动前往默认文件夹寻找。
        self.mat_file = matrix_file
        # 载入默认路径
        self.default_path = []
        self.load_matrix_file_path()
        self.mat_file = self.matrix_file_found(self.mat_file)

    def set_mat_file(self, new_mat_file):
        self.mat_file = self.matrix_file_found(new_mat_file)

    def load_matrix_file_path(self):
        with open("./default_matrix_address.txt", "r", encoding="UTF-8") as dm_address:
            new_addresses = dm_address.readlines()
            for lines in new_addresses:
                if not lines.startswith("#"):
                    self.default_path.append(lines.strip())

    def matrix_file_found(self, mat_file):
        # 如果输入的地址本就是正确的，则直接返回。
        if os.path.exists(mat_file):
            return mat_file
        for path in self.default_path:
            if os.path.exists(os.path.join(path, mat_file)):
                return os.path.join(path, mat_file)
            if os.path.exists(os.path.join(path, mat_file) + ".csv"):
                return os.path.join(path, mat_file)
        return None

    def new_matrix_file(self, matrix_content, matrix_file=None, mode="w+"):
        """
        根据提供的矩阵内容，和文件地址，将矩阵内容写入到相应的文件中去
        :param matrix_content: 粒子矩阵内容，是多维列表的形式
        :param matrix_file: 目标文件地址或者目标文件名称
        :param mode: 打开文件的模式。
        :return:
        """
        if matrix_file is not None:
            if matrix_file != self.mat_file:
                self.mat_file = self.matrix_file_found(matrix_file)
        with open(matrix_file, mode, encoding="utf-8") as mf:
            for particles in matrix_content:
                part_str = ""
                for info in particles:
                    part_str += str(info).strip()
                    part_str += ","
                print(part_str.strip(","))
                mf.write(part_str.strip(",") + "\n")

    def renew_matrix_file(self,  matrix_content, matrix_file=None):
        self.new_matrix_file(matrix_content, matrix_file)

    def add_to_matrix_file(self, matrix_content, matrix_file=None):
        self.new_matrix_file(matrix_content, matrix_file, "a")


# 测试文件写入
# if __name__ == "__main__":
#     writer = MatrixWriter()
#     writer.add_to_matrix_file("cube", [[3, 4, 3, 0, 0, 0, 0, 1, "f", 0, 0, 0, 0, 0, 0, 27],
#                                        [3, 4, 3, 0, 0, 0, 0, 1, "r", 0, 0, 0, 0, 0, 0, 27]])
    # writer.add_to_matrix_file("cube", "abcabc")
