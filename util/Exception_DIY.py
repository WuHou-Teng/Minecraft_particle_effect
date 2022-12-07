
class ExceptionBase(Exception):

    def __init__(self, area, situation):
        super(ExceptionBase, self).__init__()
        self.area = area
        self.situation = situation

    def info(self):
        return self.area + ": " + self.get_self_name() + ": " + self.situation

    # 返回自己的类名称
    def get_self_name(self):
        return str(type(self)).split('.')[1][:-3]