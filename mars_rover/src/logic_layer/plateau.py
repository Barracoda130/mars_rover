

from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.common.position import Position
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.logic_layer.rover import Rover
from mars_rover.src.common.rover_data import RoverData
from mars_rover.src.output_layer.output_data import OutputData

class Plateau:
    def __init__(self):
        self._rovers: list[Rover] = []
        self._current_rover = None
        self._size = PlateauSize(0, 0)
        
    def set_dimensions(self, size: PlateauSize):
        self._size = size
        
    def add_rover(self, rover_start: RoverData):
        self._current_rover = Rover(rover_start.position, 
                                    rover_start.direction)
        
    def move_rover(self, instruction: RoverInstruction):
        if self._current_rover is None:
            raise Exception("No rover has been added to the plateau.")
        self._current_rover.act(instruction)
        
    def save_rover(self):
        if self._current_rover is None:
            raise Exception("No rover has been added to the plateau.")
        self._rovers.append(self._current_rover)
        self._current_rover = None
        
    def __repr__(self):
        return f"Plateau(size={self._size}, rovers={self._rovers})"

    def to_output_data(self):
        rovers = [rover.to_output_data() for rover in self._rovers]
        rovers.append(self._current_rover.to_output_data()) if self._current_rover else None
        return OutputData(
            plateau_size=self._size,
            rovers=rovers
        )