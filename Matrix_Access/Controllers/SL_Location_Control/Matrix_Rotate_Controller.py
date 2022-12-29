import math
import numpy as np
from Matrix_Access.Controllers.Controller_Interface import ControllerBase


class MatrixRotateController(ControllerBase):

    def __init__(self, index_name=None, angle=0, u=0, v=0, w=0, rotate_centre=None):
        """
        :param angle: 默认输入为角度。
        :param u:
        :param v:
        :param w:
        :param rotate_centre:
        """
        super().__init__(index_name)
        self.angle = math.radians(angle)
        self.x_vector = u
        self.y_vector = v
        self.z_vector = w
        self.rotate_centre = rotate_centre if rotate_centre is not None else [0, 0, 0]
        # 根据输数据创建旋转矩阵。
        self.rotate_matrix = np.array([[math.cos(self.angle) + (1 - math.cos(self.angle)) * u ** 2,
                                        (1 - math.cos(self.angle)) * u * v - math.sin(self.angle) * w,
                                        (1 - math.cos(self.angle)) * u * w + math.sin(self.angle) * v],

                                       [(1 - math.cos(self.angle)) * u * v + math.sin(self.angle) * w,
                                        math.cos(self.angle) + (1 - math.cos(self.angle)) * v ** 2,
                                        (1 - math.cos(self.angle)) * v * w - math.sin(self.angle) * u],

                                       [(1 - math.cos(self.angle)) * u * w - math.sin(self.angle) * v,
                                        (1 - math.cos(self.angle)) * w * v + math.sin(self.angle) * u,
                                        math.cos(self.angle) + (1 - math.cos(self.angle)) * w ** 2]])

    def set_rotate_angle(self, angle):
        self.angle = math.radians(angle)
        self.update_matrix()

    def set_x_vector(self, u):
        self.x_vector = u
        self.update_matrix()

    def set_y_vector(self, v):
        self.y_vector = v
        self.update_matrix()

    def set_z_vector(self, w):
        self.z_vector = w
        self.update_matrix()

    def update_matrix(self):
        self.rotate_matrix = np.array(
            [[math.cos(self.angle) + (1 - math.cos(self.angle)) * self.x_vector ** 2,
              (1 - math.cos(self.angle)) * self.x_vector * self.y_vector - math.sin(self.angle) * self.z_vector,
              (1 - math.cos(self.angle)) * self.x_vector * self.z_vector + math.sin(self.angle) * self.y_vector],

             [(1 - math.cos(self.angle)) * self.x_vector * self.y_vector + math.sin(self.angle) * self.z_vector,
              math.cos(self.angle) + (1 - math.cos(self.angle)) * self.y_vector ** 2,
              (1 - math.cos(self.angle)) * self.y_vector * self.z_vector - math.sin(self.angle) * self.x_vector],

             [(1 - math.cos(self.angle)) * self.x_vector * self.z_vector - math.sin(self.angle) * self.y_vector,
              (1 - math.cos(self.angle)) * self.z_vector * self.y_vector + math.sin(self.angle) * self.x_vector,
              math.cos(self.angle) + (1 - math.cos(self.angle)) * self.z_vector ** 2]])

    def process(self, particle):
        nx = particle[0] - self.rotate_centre[0]
        ny = particle[1] - self.rotate_centre[1]
        nz = particle[2] - self.rotate_centre[2]
        point_matrix = np.transpose(np.array([[nx, ny, nz]]))
        new_point_matrix = np.dot(self.rotate_centre, point_matrix)
        particle[0] = round(new_point_matrix[0][0], 4) + self.rotate_centre[0]
        particle[1] = round(new_point_matrix[1][0], 4) + self.rotate_centre[1]
        particle[2] = round(new_point_matrix[2][0], 4) + self.rotate_centre[2]
        return particle

