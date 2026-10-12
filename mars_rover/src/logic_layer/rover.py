

from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.common.position import Position
from mars_rover.src.common.rover_data import RoverData


class Rover:
    def __init__(self, position: Position, direction: CompassDirection):
        self.position = position
        self.direction = direction

    def act(self, instruction: RoverInstruction):
        match instruction:
            case RoverInstruction.MOVE_FORWARD:
                self._move()
            case RoverInstruction.TURN_LEFT:
                self._turn_left()
            case RoverInstruction.TURN_RIGHT:
                self._turn_right()
            case RoverInstruction.STAY:
                pass
            case _:
                raise ValueError(f"Invalid instruction: {instruction}")
            
    def _move(self):
        match self.direction:
            case CompassDirection.NORTH:
                self.position.y += 1
            case CompassDirection.EAST:
                self.position.x += 1
            case CompassDirection.SOUTH:
                self.position.y -= 1
            case CompassDirection.WEST:
                self.position.x -= 1
            case _:
                raise ValueError(f"Invalid direction: {self.direction}")
            
    def _turn_left(self):
        match self.direction:
            case CompassDirection.NORTH:
                self.direction = CompassDirection.WEST
            case CompassDirection.WEST:
                self.direction = CompassDirection.SOUTH
            case CompassDirection.SOUTH:
                self.direction = CompassDirection.EAST
            case CompassDirection.EAST:
                self.direction = CompassDirection.NORTH
            case _:
                raise ValueError(f"Invalid direction: {self.direction}")

    def _turn_right(self):
        match self.direction:
            case CompassDirection.NORTH:
                self.direction = CompassDirection.EAST
            case CompassDirection.EAST:
                self.direction = CompassDirection.SOUTH
            case CompassDirection.SOUTH:
                self.direction = CompassDirection.WEST
            case CompassDirection.WEST:
                self.direction = CompassDirection.NORTH
            case _:
                raise ValueError(f"Invalid direction: {self.direction}")

    def __repr__(self):
        return f"Rover(position={self.position}, direction={self.direction})"

    def to_output_data(self):
        return RoverData(position=self.position, direction=self.direction)
            
        