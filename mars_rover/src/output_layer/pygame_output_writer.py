

from mars_rover.src.common.enums import CompassDirection
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.output_layer.output_data import OutputData
from mars_rover.src.output_layer.output_writer import OutputWriter
from mars_rover.src.common.exceptions import MarsRoverException
import pygame

class PygameOutputWriter(OutputWriter):
    _ROVER_ROTATION_ANGLES = {
        CompassDirection.NORTH: 0,
        CompassDirection.EAST: -90,
        CompassDirection.SOUTH: 180,
        CompassDirection.WEST: 90
    }
    
    def __init__(self):
        self._previous_output_data = OutputData(plateau_size=PlateauSize(0, 0), rovers=[])
        self._canvas = None
        
    def setup(self) -> None:
        pygame.init()
        self._canvas = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mars Rover Simulation")

    
    
    def write(self, data: OutputData):
        if self._canvas is None:
            raise MarsRoverException("Must call setup before write")

        self._canvas.fill("white")
        
        if data.plateau_size.width <= 0 or data.plateau_size.height <= 0:
            return
        
        top_start = 50
        left_start = 50
        
        grid_width = 700
        grid_height = 500

        square_size = min(grid_width/data.plateau_size.width, grid_height/data.plateau_size.height)
        
        # if self._previous_output_data.plateau_size != data.plateau_size:
        for i in range(data.plateau_size.height + 1):
            pygame.draw.line(self._canvas, "black", (left_start, top_start + i * square_size), (left_start + data.plateau_size.width * square_size, top_start + i * square_size))
        for i in range(data.plateau_size.width + 1):
            pygame.draw.line(self._canvas, "black", (left_start + i * square_size, top_start), (left_start + i * square_size, top_start + data.plateau_size.height * square_size))
        
        # if self._previous_output_data.rovers != data.rovers:
        rover_img = pygame.image.load("data/rover.png")
        rover_scaled = pygame.transform.scale(rover_img, (square_size, square_size))
        for rover in data.rovers:
            rover_x = left_start + (rover.position.x - 1) * square_size
            rover_y = top_start + (data.plateau_size.height - rover.position.y) * square_size
            rover_rotated = pygame.transform.rotate(rover_scaled, self._ROVER_ROTATION_ANGLES[rover.direction])
            self._canvas.blit(rover_rotated, (rover_x, rover_y))
            
        self._previous_output_data = data
        pygame.display.update()
