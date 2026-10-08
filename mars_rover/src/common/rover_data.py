

from mars_rover.src.common.enums import CompassDirection
from mars_rover.src.common.position import Position


class RoverData:
    def __init__(self,
                 position: Position,
                 direction: CompassDirection):
        self.position = position
        self.direction = direction