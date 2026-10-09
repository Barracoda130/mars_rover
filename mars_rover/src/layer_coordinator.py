
from enum import Enum

from mars_rover.src.common.enums import RoverInstruction
from mars_rover.src.input_layer.exceptions import EndOfInstructionsException
from mars_rover.src.input_layer.input_parser import FileInputParser, ConsoleInputParser
from mars_rover.src.input_layer.pygame_input_parser import PygameInputParser
from mars_rover.src.logic_layer.plateau import Plateau
from mars_rover.src.output_layer.output_data import OutputData
from mars_rover.src.output_layer.output_writer import ConsoleOutputWriter
from mars_rover.src.output_layer.pygame_output_writer import PygameOutputWriter
from mars_rover.src.common.enums import ProgramState

class LayerCoordinator:
    def __init__(self, input_file_path: str):
        # self._input_layer = FileInputParser(input_file_path)
        self._input_layer = ConsoleInputParser()
        self._plateau = Plateau()
        # self._output_layer = PygameOutputWriter()
        self._output_layer = ConsoleOutputWriter()

        self._state = ProgramState.INITIALIZING

    def _setup(self) -> ProgramState:
        self._input_layer.setup()
        self._output_layer.setup()
        return ProgramState.GET_PLATEAU_SIZE

    def _cleanup(self):
        self._input_layer.cleanup()
        self._output_layer.cleanup()
        
    def _get_plateau_size(self) -> ProgramState:
        plateau_size = self._input_layer.get_plateau_size()
        self._plateau.set_dimensions(plateau_size)
        return ProgramState.GET_ROVER_START

    def _get_rover_start(self) -> ProgramState:
        rover_start = self._input_layer.get_next_rover_start()
        if rover_start is None:
            return ProgramState.EXIT
        
        try: 
            self._plateau.add_rover(rover_start)
        except Exception as e:
            self._input_layer.logic_error_raised(e)
            
        return ProgramState.GET_ROVER_INSTRUCTION

    def _get_rover_instruction(self) -> ProgramState:
        instruction = self._input_layer.get_next_rover_instruction()
        if instruction is None:
            return ProgramState.GET_ROVER_START
        
        try:
            self._plateau.move_rover(instruction)
        except Exception as e:
            self._input_layer.logic_error_raised(e)
            
        return ProgramState.GET_ROVER_INSTRUCTION


    def _run(self):
        while True:
            match self._state:
                case ProgramState.INITIALIZING:
                    self._state = self._setup()
                case ProgramState.GET_PLATEAU_SIZE:
                    self._state = self._get_plateau_size()
                case ProgramState.GET_ROVER_START:
                    self._state = self._get_rover_start()
                case ProgramState.GET_ROVER_INSTRUCTION:
                    self._state = self._get_rover_instruction()
                case ProgramState.ERROR:
                    break
                case ProgramState.EXIT:
                    break
                
            self._output_layer.write(self._plateau.to_output_data(), self._state)
            
        self._output_layer.write(self._plateau.to_output_data(), self._state)

    def run(self):
        try:
            self._run()
        finally:
            self._cleanup()

