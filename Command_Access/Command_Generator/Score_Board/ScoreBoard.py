

class ScoreBoardGenerator(object):
    """
    计分板相关指令生成器。
    TODO 详细了解计分板后，再完善
    """
    def __init__(self, index_name, criterion, display_name):
        self.index_name = index_name
        self.criterion = criterion
        self.display_name = display_name

    def get_name(self):
        return self.index_name

    def get_display_name(self):
        return self.display_name

    def get_criterion(self):
        return self.criterion


