

from enum import Enum

class RoverInstruction(Enum):
    MOVE_FORWARD = "M"
    TURN_LEFT = "L"
    TURN_RIGHT = "R"
    
    
class CompassDirection(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"
    
    