

class ColorRangeException(Exception):

    def __init__(self, area):
        super(ColorRangeException, self).__init__()
        self.area = area
        self.info = "忽略颜色区间，end内元素数值应该大于等于begin内元素"

