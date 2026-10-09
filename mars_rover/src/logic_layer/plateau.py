

from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.common.exceptions import RoverLeftPlateauException
from mars_rover.src.common.position import Position
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.logic_layer.rover import Rover
from mars_rover.src.common.rover_data import RoverData
from mars_rover.src.output_layer.output_data import OutputData

class Plateau:
    def __init__(self):
        self._rovers: list[Rover] = []
        self._size = PlateauSize(0, 0)

    @property
    def _current_rover(self):
        return self._rovers[-1] if self._rovers else None
    
    @_current_rover.setter
    def _current_rover(self, rover: Rover):
        self._rovers[-1] = rover

    def _is_within_bounds(self, position: Position) -> bool:
        return (1 <= position.x <= self._size.width) and (1 <= position.y <= self._size.height)
        
    def set_dimensions(self, size: PlateauSize):
        self._size = size
        
    def add_rover(self, rover_start: RoverData):
        self._rovers.append(Rover(rover_start.position, 
                                  rover_start.direction))
        
    def move_rover(self, instruction: RoverInstruction):
        if self._current_rover is None:
            raise Exception("No rover has been added to the plateau.")
        
        rover_old_position = self._current_rover.position.copy()
        self._current_rover.act(instruction)
        
        if not self._is_within_bounds(self._current_rover.position):
            invalid_location = self._current_rover.position
            self._current_rover.position = rover_old_position
            raise RoverLeftPlateauException(self._size, invalid_location)
        
    def __repr__(self):
        return f"Plateau(size={self._size}, rovers={self._rovers})"

    def to_output_data(self):
        rovers = [rover.to_output_data() for rover in self._rovers]
        return OutputData(
            plateau_size=self._size,
            rovers=rovers
        )