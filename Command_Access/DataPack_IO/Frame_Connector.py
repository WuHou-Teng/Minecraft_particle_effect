from Command_Access.Command_Generator.Executes.Execute_Builder import ExecuteBuilder


class FrameConnector(object):
    """
    用于将两帧或者多帧之间相互关联。
    """
    def __init__(self):
        self.execute_header = ExecuteBuilder()
