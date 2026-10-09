

from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.common.position import Position
from mars_rover.src.common.rover_data import RoverData


class Rover:
    def __init__(self, position: Position, direction: CompassDirection):
        self.position = position
        self.direction = direction

    def act(self, instruction: RoverInstruction):
        if instruction == RoverInstruction.MOVE_FORWARD:
            self._move()
        elif instruction == RoverInstruction.TURN_LEFT:
            self._turn_left()
        elif instruction == RoverInstruction.TURN_RIGHT:
            self._turn_right()
        else:
            raise ValueError(f"Invalid instruction: {instruction}")
            
    def _move(self):
        if self.direction == CompassDirection.NORTH:
            self.position.y += 1
        elif self.direction == CompassDirection.EAST:
            self.position.x += 1
        elif self.direction == CompassDirection.SOUTH:
            self.position.y -= 1
        elif self.direction == CompassDirection.WEST:
            self.position.x -= 1
        else:
            raise ValueError(f"Invalid direction: {self.direction}")
            
    def _turn_left(self):
        if self.direction == CompassDirection.NORTH:
            self.direction = CompassDirection.WEST
        elif self.direction == CompassDirection.WEST:
            self.direction = CompassDirection.SOUTH
        elif self.direction == CompassDirection.SOUTH:
            self.direction = CompassDirection.EAST
        elif self.direction == CompassDirection.EAST:
            self.direction = CompassDirection.NORTH
        else:
            raise ValueError(f"Invalid direction: {self.direction}")

    def _turn_right(self):
        if self.direction == CompassDirection.NORTH:
            self.direction = CompassDirection.EAST
        elif self.direction == CompassDirection.EAST:
            self.direction = CompassDirection.SOUTH
        elif self.direction == CompassDirection.SOUTH:
            self.direction = CompassDirection.WEST
        elif self.direction == CompassDirection.WEST:
            self.direction = CompassDirection.NORTH
        else:
            raise ValueError(f"Invalid direction: {self.direction}")

    def __repr__(self):
        return f"Rover(position={self.position}, direction={self.direction})"

    def to_output_data(self):
        return RoverData(position=self.position, direction=self.direction)
            
        