

from enum import Enum, auto
from typing import Any


class InstructionType(Enum):
    ROVER_START = auto()
    PLATEAU_SIZE = auto()
    ROVER_INSTRUCTION = auto()
    QUIT = auto()
    NEXT_ROVER = auto()
    NONE = auto()

class InputInstruction:
    def __init__(self,
                 type_: InstructionType,
                 data: Any):
        self.type = type_
        self.data = data