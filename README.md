# Minecraft_particle_effect
A Generator for creating minecraft partical effects from pictures or 3D models

对粒子特效有兴趣的小伙伴欢迎来我的群一起交流啊~， 如果会python或者Java程序编写就更好了！
我还缺一位mod制作者。有偿。欢迎来骚扰。

群：761553058

————————————————————————————————————————————————————————————————————
抱歉啦，这个项目目前还在研发阶段。且本人水平实在有限，所以只能一边学一边设计。
导致文件结构一直在发生变动，所以也没有写完善的readme和wiki。
只能大体上交代一下部分大概不会大改的文件结构：

• Command_Access【包含所有与mc指令】
    ○ Command_Convertor
        § Base_Convertor【转换器抽象类】
        § Color_Convertor【颜色(dust)转换器】
        § Color_Dict_Convertor【粒子--颜色转换器】(因粒子运动特性，考虑放弃)
        § Homo_Convertor【基本粒子转换器】
    ○ Const
        § Block_Java【JE的方块ID,暂时未用到】
        § Color【基础颜色的预定义】
        § Convertor_consts【Command_Conbertor要用到的常量】
        § Particle_Color_dictionary【粒子--颜色对应字典】(因粒子运动特性，考虑放弃)
        § Particle_BedRock【基岩版粒子ID集合】
        § Particle_Java 【JE版粒子ID集合】
    ○ DataPack_IO
        § Frame_Connector【帧连接器，用于制作动画】
        § Function_Writer【负责创建和写入mcfunction】
        § MC_Effect_Generator
        § Particle_Effect_Function_Generator
    ○ Execute_Generator
• Matrix_Access
    ○ Controllers【基础控制器】
        § Color_Control
            □ Color_Controller【颜色控制器抽象类】
            □ Color_Controller_Const【颜色控制器常量】
            □ Color_Filter_Amp【颜色滤镜/增幅器】
            □ Color_White_List 【颜色白/黑名单】
        § Location_Control
            □ Rotate_Controller【旋转控制器】
            □ Scale_Controller【缩放控制器】
            □ Shift_Controller【平移控制器】
        § Motion_Control
            □ Basis_Moving_Action
            □ Motion_Controller【移动控制器抽象类】
            □ Motion_Controller_Const【移动控制器基础类。】
    ○ Second_Level_Control
        § 【部分二阶控制器。是基础控制器在特定方面的封装拓展】
        § 【大部分还没写道。】
    ○ Self_Designed_Functions
    ○ Matrix_Files
• Source_Access
    ○ Const
        § Image_Process_Const【图片处理常量】
    ○ Image_Process
        § 【图像处理，包括色调，切割，旋转，采样等】
        § 【并最终将图像转换为粒子矩阵】
    ○ Model_Process
        § 【模型转换粒子矩阵要用到的类，还没开始写。】
    ○ OpCVReload【这个东西没用】
• Panel【GUI设计，目前还没开始】
• util【】

