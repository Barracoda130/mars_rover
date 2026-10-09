

from mars_rover.src.common.enums import CompassDirection
from mars_rover.src.common.position import Position


class RoverData:
    def __init__(self,
                 position: Position,
                 direction: CompassDirection):
        self.position = position
        self.direction = direction

    def __eq__(self, other) -> bool:
        if not isinstance(other, RoverData):
            return NotImplemented
        return self.position == other.position and self.direction == other.direction