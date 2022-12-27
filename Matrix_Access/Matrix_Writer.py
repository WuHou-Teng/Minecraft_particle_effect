
import os


class MatrixWriter(object):
    """
    该类用于新建矩阵文件，并写入。
    """
    def __init__(self):
        self.cwd = os.getcwd()
        self.matrix_source_folder = self.cwd + ".\\Matrix_Files"

    def new_matrix_file(self, matrix_file_name, matrix_content):
        with open(os.path.join(self.matrix_source_folder, matrix_file_name) + '.csv', mode="w+") as mf:
            for particles in matrix_content:
                part_str = ""
                for info in particles:
                    part_str += str(info).strip()

