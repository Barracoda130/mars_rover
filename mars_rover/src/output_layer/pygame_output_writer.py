

from mars_rover.src.common.enums import ProgramState
from mars_rover.src.output_layer.output_data import OutputData
from mars_rover.src.output_layer.output_writer import OutputWriter
import pygame

class PygameOutputWriter(OutputWriter):
    def setup(self) -> None:
        pygame.init()
        self._canvas = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mars Rover Simulation")
    
    def cleanup(self) -> None:
        # Implement logic to clean up Pygame output
        pass
    
    def write(self, data: OutputData, program_state: ProgramState):
        # Implement logic to write output to Pygame window
        pygame.display.update()
