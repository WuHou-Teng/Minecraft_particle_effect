from Command_Access.Command_Generator.Score_Board.ScoreBoard import ScoreBoardGenerator
from util.Box import Box


class ScoreBoardBox(Box):

    def __init__(self):
        super().__init__()
        self.scoreboard_dict = {}

    def add_scoreboard(self, scoreboard):
        """
        添加scoreboard实例
        :param scoreboard: 添加新的scoreboard实例。Controller
        """
        self.scoreboard_dict[scoreboard.get_name()] = scoreboard
        return scoreboard.get_name

    def get_scoreboard(self, index_name):
        """
        返回具有相应index_name的scoreboard
        :param index_name: 创建scoreboard时，定义的名字。
        """
        if index_name in self.scoreboard_dict.keys():
            return self.scoreboard_dict.get(index_name)
        else:
            return None

    def get_scoreboard_list(self):
        """
        返回盒子中包含的所有scoreboard的index_name
        """
        return list(self.scoreboard_dict.keys())

    def get_object_list(self):
        return self.get_scoreboard_list()

    def add_object(self, new_object):
        return self.add_scoreboard(new_object)

    def get_object(self, index_name):
        return self.get_scoreboard(index_name)

    def new_scoreboard(self, name, criterion, display_name):
        self.add_scoreboard(ScoreBoardGenerator(name, criterion, display_name))

