import matplotlib.pyplot as plt
from PIL import Image
import os

image_name = "try3.jpg"
address = "E:\work\Interesting_things\python_test\Mc_Effect\pics"
img = Image.open(os.path.join(address, image_name))
# img.convert("L").show()
imagedata = img.getpixel((10, 10))
print(imagedata)
imagedata = img.convert("L").getpixel((10, 10))
print(imagedata)

# Image.Image.point()
img.convert("1", dither=0).show()
img.convert("1").show()

# plt.subplot(1, 3, 1)
# plt.imshow(img.convert(mode="1", dither=0))
# plt.subplot(1, 3, 2)
# plt.imshow(img.convert(mode="1", dither=1))
# plt.subplot(1, 3, 3)
# plt.imshow(img.convert(mode="1", dither=2))
# plt.show()
