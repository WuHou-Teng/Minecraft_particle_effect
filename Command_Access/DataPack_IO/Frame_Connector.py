from Command_Access.Execute_Generator.Execute import ExecuteBuilder


class FrameConnector(object):
    """
    用于将两帧或者多帧之间相互关联。
    """
    def __init__(self):
        self.execute_header = ExecuteBuilder()
