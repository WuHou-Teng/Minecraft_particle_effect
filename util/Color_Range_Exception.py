from util.Exception_DIY import ExceptionBase


class ColorRangeException(ExceptionBase):

    def __init__(self, area, situation="end或start值异常"):
        super(ColorRangeException, self).__init__(area, situation)
        self.reason = "颜色区间，end内元素数值应该大于等于start内元素, 且数值位于0到1之间，其中红色通道最低值不低于0.001"

    def info(self):
        return super().info() + "\n Reason: " + self.reason
