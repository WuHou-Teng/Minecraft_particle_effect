from PIL import Image
# Settings:
# 打开图片
im = Image.open('E:\\work\\Interesting_things\\python_test\\Mc_Effect\\pics\\try2.png')
# 获取图片长宽
width, height = im.size[0], im.size[1]
# 下采样率
down_sample = 3
# 缩放体积
scale_rate = 0.1
# 新开一个mcfunction文件
f = open(r'particle_img.mcfunction', "w")
# xyz方向上的shift
x_shift, y_shift, z_shift = 0, round(height/down_sample*scale_rate), 0
# TODO 确定图片方向
direction = 'z'
# 粒子类型
particle_name = "minecraft:end_rod"
# xd yd zd speed amount pattern player
particle_value = "0 0 0 0 1 force"

# 进入大循环，遍历图片长宽
for w in range(0, round(width/down_sample)):
    for h in range(0, round(height/down_sample)):
        # 获得当前像素的数据
        imgdata = (im.getpixel((w * down_sample, h * down_sample)))
        # if imgdata[0] == 0:
        if imgdata[0] >= 0 and imgdata[0] <=30:  # 也就是说这个像素是黑色的，那么就是我们要表述的线条。
            # 如果方向为z，那么z的坐标就不动，x表示宽度，y表示高度，并且，
            if direction == 'z':
                cmd = f'particle {particle_name} ~{x_shift - w * scale_rate} ~{y_shift - h * scale_rate} ~{z_shift} {particle_value}'
                f.write(f'{cmd}\n')
            # 如果方向为y，那么y的坐标就不动，x表示宽度，z表示高度
            elif direction == 'y':
                cmd = f'particle {particle_name} {x_shift - w * scale_rate} {y_shift} {z_shift - h * scale_rate} {particle_value}'
                f.write(f'{cmd}\n')
            elif direction == 'x':
                cmd = f'particle {particle_name} {x_shift} {y_shift - h * scale_rate} {z_shift - w * scale_rate} {particle_value}'
                f.write(f'{cmd}\n')
f.close()
