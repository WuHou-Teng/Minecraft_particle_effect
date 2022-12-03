import os
from PIL import Image


class ImageAccess(object):

    def __init__(self):

        self.image_address = None
        self.img = None

    def load_image(self, image_address):
        self.image_address = image_address
        if self.img is not None:
            try:
                self.img.close()
            except:
                self.img = None
        if not os.path.exists(self.image_address):
            self.image_address = None
            return "需要访问的图片不存在"
        try:
            self.img = Image.open(self.image_address)
            self.img.close()
            return "图片读取成功，类型为" + os.path.basename(self.image_address).split(".")[-1]
        except:
            return "需要访问的图片格式不对，或者不存在"

    @property
    def i_width(self):
        return self.img.size[0]

    @property
    def i_height(self):
        return self.img.size[1]

    @property
    def binary(self):
        return self.img.convert("l")
