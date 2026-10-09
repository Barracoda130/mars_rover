

from mars_rover.src.common.position import Position
from mars_rover.src.common.size import PlateauSize


class MarsRoverException(Exception):
    """Base class for exceptions in this module."""
    pass

class RoverLeftPlateauException(MarsRoverException):
    def __init__(self, 
                 plateau_size: PlateauSize, 
                 position: Position):
        self.position = position
        self.plateau_size = plateau_size
        super().__init__(f"Invalid move: Rover at position {position} is outside the plateau size {plateau_size}")