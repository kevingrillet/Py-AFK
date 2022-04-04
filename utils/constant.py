# Constant file to be clean
from enum import auto

from utils.cls.superintenum import SuperIntEnum


class DebugLevel(SuperIntEnum):
    ALWAYS = auto()
    INFO = auto()
    CLASS = auto()
    FUNCTIONS = auto()
    DEBUG = auto()


PACKAGE_NAME = "com.lilithgame.hgame.gp"
PACKAGE_NAME_TEST = "com.lilithgames.hgame.gp.id"
