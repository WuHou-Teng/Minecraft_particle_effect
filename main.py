# -*- coding:utf-8 -*-
import os
import math
from Command_Access.DataPack_IO.Particle_Effect_Function_Generator import *


if __name__ == "__main__":

    print(os.getcwd())
    # 环境准备
    datapack_folder = (
        "C:\\Wuhou\\play\\minecraft\\1.18.2\\1.18.2Particle\\.minecraft\\saves\\Particle_Test\\datapacks"
    )
    datapack_name = "first_test"
    datapack_address = os.path.join(datapack_folder, datapack_name)
    new_effect_name = "first_test_effect"
    new_function_name = "first_test_function"

    # 矩阵源准备
    matrix_folder = (
        "C:\\Wuhou\\study\\python_test\\Mc_Effect\\Mc_Partical_effect_Repo\\Matrix_Files"
    )
    group = "Square_effect"
    matrix_name = "cube.csv"
    matrix_file = os.path.join(matrix_folder, matrix_name)

    # __________________运行____________________
    # 初始化生成器
    f_gen = PEFuncGenerator(datapack_address, new_effect_name)
    # 载入粒子矩阵
    cube_matrix_access = f_gen.open_new_matrix(matrix_file)
    # 将粒子矩阵添加到生成器的粒子访问器盒子里面。
    f_gen.matrix_access_box.add_matrix_accesser(
        cube_matrix_access
    )


    # 构建控制器
    # 体积缩放
    f_gen.controller_box.add_controller(
        f_gen.controller_box.new_scale_controller(
            "scale1", 1, 1, 1,
            f_gen.matrix_access_box.get_matrix_accesser(matrix_name).geom_centre
        )
    )
    # 延时添加
    f_gen.controller_box.add_controller(
        f_gen.controller_box.new_delay_count_shift_controller(
            index_name="delay_count1",
            delay_type=ABSOLUTE,
            tick_add=1,
            particle_count_step=16
        )
    )
    # 旋转效果
    f_gen.controller_box.add_controller(
        f_gen.controller_box.new_rotate_controller(
            index_name="rotate1",
            x_angle=10,
            y_angle=0,
            z_angle=-10,
            rotate_centre=f_gen.matrix_access_box.get_matrix_accesser(matrix_name).geom_centre
        )
    )

    # 平移效果
    f_gen.controller_box.add_controller(
        f_gen.controller_box.new_shift_controller(
            index_name="shift1",
            x_shift=3,
            y_shift=0,
            z_shift=3
        )
    )

    # 添加控制器到控制器调用进程
    f_gen.controller_applier.add_controller_to_apply_list(
        f_gen.controller_box.get_controller("scale1")
    ).add_controller_to_apply_list(
        f_gen.controller_box.get_controller("delay_count1")
    ).add_controller_to_apply_list(
        f_gen.controller_box.get_controller("rotate1")
    ).add_controller_to_apply_list(
        f_gen.controller_box.get_controller("shift1")
    )

    # 对粒子矩阵调用控制器:
    new_mat_name = "cube2.csv"
    f_gen.apply_controller_processing_and_save(
        matrix_access=cube_matrix_access,
        new_mat_file_address=new_mat_name,
        override=True,  # 这里填True会覆盖原本的cube2.csv
        override_original=True  # 这里填False是修改不影响cube_matrix_access
    )
    # f_gen.controller_box.get_controller("delay_count1").clear_record()

    # 反复调用：
    for i in range(71):
        new_mat_name = f_gen.apply_controller_processing_and_save(
            matrix_access=cube_matrix_access,
            new_mat_file_address=new_mat_name,
            override=False,  # 这里填False就不会覆盖原来的cube2.csv
            override_original=True  # 这里填True，就可以将每次修改的结果保留到cube_matrix_access，进入下一轮转换。
        )
        # 延时相关计时器得清理记录，这里写的不好，回头用process_matrix替代
        # f_gen.controller_box.get_controller("delay_count1").clear_record()

    # 调用完了后打开新的矩阵访问器
    new_mat_file = f_gen.open_new_matrix(new_mat_name)

    # 设定强制采用的粒子类型
    f_gen.set_force_particle(Particles_Java.end_rod)

    # 启用延时函数
    f_gen.use_timer = True

    # 最后调用此函数将矩阵转化为mcfunction
    f_gen.generator(new_function_name, new_mat_file, function_override=True)



