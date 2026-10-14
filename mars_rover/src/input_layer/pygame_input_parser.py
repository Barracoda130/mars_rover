
from mars_rover.src.common.exceptions import ProgramEndException
from mars_rover.src.common.instruction import InputInstruction, InstructionType
from mars_rover.src.common.position import Position
from mars_rover.src.common.rover_data import RoverData
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.input_layer.input_parser import InputParser

from typing import override
import pygame

from mars_rover.src.output_layer.pygame_objects.button import ButtonType

class PygameInputParser(InputParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gui_input_buffer: list[InputInstruction] = []

    def get_plateau_size(self) -> PlateauSize:
        return PlateauSize(20, 20)  # Placeholder value, implement logic to get plateau size from Pygame input

    def get_next_rover_start(self) -> RoverData|None:
        return RoverData(position=Position(1, 2), direction=CompassDirection.NORTH)  # Placeholder value, implement logic to get rover starts from Pygame input

    def get_next_rover_instruction(self) -> RoverInstruction|None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise ProgramEndException("User requested exit.")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    # callback()
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return RoverInstruction.MOVE_FORWARD
                elif event.key == pygame.K_a:
                    return RoverInstruction.TURN_LEFT
                elif event.key == pygame.K_d:
                    return RoverInstruction.TURN_RIGHT
                elif event.key == pygame.K_q:
                    return None  # Signal move onto next rover

        return RoverInstruction.STAY 
    
    def _rover_movement_instruction(self, event_type: int) -> InputInstruction:
        match event_type:
            case pygame.K_w:
                return InputInstruction(InstructionType.ROVER_INSTRUCTION, RoverInstruction.MOVE_FORWARD)
            case pygame.K_a:
                return InputInstruction(InstructionType.ROVER_INSTRUCTION, RoverInstruction.TURN_LEFT)
            case pygame.K_d:
                return InputInstruction(InstructionType.ROVER_INSTRUCTION, RoverInstruction.TURN_RIGHT)
            case pygame.K_q:
                return InputInstruction(InstructionType.NEXT_ROVER, None)
            case _:
                return InputInstruction(InstructionType.ROVER_INSTRUCTION, RoverInstruction.STAY)

    @override
    def logic_error_raised(self, exception: Exception) -> None:
        pass

    @override
    def get_next_instruction(self, expected_instruction_type: InstructionType) -> InputInstruction:
        if self._gui_input_buffer:
            return self._gui_input_buffer.pop(0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return InputInstruction(InstructionType.QUIT, None)
            elif event.type == pygame.KEYDOWN:
                return self._rover_movement_instruction(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    pygame.mouse.get_pos()
                    # callback()
                    pass
            
        return InputInstruction(InstructionType.ROVER_INSTRUCTION, self.get_next_rover_instruction())
    
    def gui_callback(self, button_type: ButtonType, data: str) -> None:
        if button_type == ButtonType.PLATEAU_SIZE:
            plateau_size = self._parse_plateau_size(data)
            self._gui_input_buffer.append(plateau_size)
        elif button_type == ButtonType.NEW_ROVER:
            rover_start = self._parse_rover_start(data)
            self._gui_input_buffer.append(rover_start)
        