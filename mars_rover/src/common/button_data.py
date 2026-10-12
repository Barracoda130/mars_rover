

from enum import Enum, auto
from typing import Any


class ButtonType(Enum):
    NEW_ROVER = auto()
    PLATEAU_SIZE = auto()
    NONE = auto()

    

class ButtonData:
    def __init__(self, type_: ButtonType, data: Any):
        self.type = type_
        self.data = data