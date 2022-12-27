import os
from math import pi

from Command_Access.Command_Convertor.Base_Convertor import Convertor
from Command_Access.Const import Particles_Java
from Command_Access.Const.Convertor_consts import *
from Command_Access.DataPack_IO.Function_Writer import FunctionWriter
from Command_Access.Execute_Generator.Execute_consts import *


class ColorConvertor(Convertor):
    """

    """
    def __init__(self):
        super().__init__()

        self.particle = Particles_Java.dust

