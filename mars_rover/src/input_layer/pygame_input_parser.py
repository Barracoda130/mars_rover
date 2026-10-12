
from mars_rover.src.common.position import Position
from mars_rover.src.common.rover_data import RoverData
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.input_layer.input_parser import InputParser

from typing import override
import pygame

class PygameInputParser(InputParser):
    
    @override
    def get_plateau_size(self) -> PlateauSize:
        return PlateauSize(5, 5)  # Placeholder value, implement logic to get plateau size from Pygame input

    @override
    def get_next_rover_start(self) -> RoverData|None:
        return RoverData(position=Position(1, 2), direction=CompassDirection.NORTH)  # Placeholder value, implement logic to get rover starts from Pygame input

    @override 
    def get_next_rover_instruction(self) -> RoverInstruction|None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return RoverInstruction.MOVE_FORWARD
                elif event.key == pygame.K_a:
                    return RoverInstruction.TURN_LEFT
                elif event.key == pygame.K_d:
                    return RoverInstruction.TURN_RIGHT

        return RoverInstruction.STAY 
                    
    