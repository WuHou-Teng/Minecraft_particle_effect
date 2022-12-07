from util.Exception_DIY import ExceptionBase


class FilterAmpRatioException(ExceptionBase):

    def __init__(self, area, situation="filter ratio 值异常"):
        super(FilterAmpRatioException, self).__init__(area, situation)
        self.reason = "Filter ratio 的值应该在 -1到255之间。"

    def info(self):
        return super().info() + "\n Reason: " + self.reason
