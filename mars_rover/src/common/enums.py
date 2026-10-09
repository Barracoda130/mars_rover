

from enum import Enum, auto

class RoverInstruction(Enum):
    MOVE_FORWARD = "M"
    TURN_LEFT = "L"
    TURN_RIGHT = "R"
    STAY = "."
    
    
class CompassDirection(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"
    
class ProgramState(Enum):
    INITIALIZING = auto()
    GET_PLATEAU_SIZE = auto()
    GET_ROVER_START = auto()
    GET_ROVER_INSTRUCTION = auto()
    ERROR = auto()
    EXIT = auto() 