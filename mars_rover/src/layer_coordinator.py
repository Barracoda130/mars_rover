
from mars_rover.src.input_layer.exceptions import EndOfInstructionsException
from mars_rover.src.input_layer.input_parser import FileInputParser, ConsoleInputParser
from mars_rover.src.logic_layer.plateau import Plateau
from mars_rover.src.output_layer.output_data import OutputData
from mars_rover.src.output_layer.output_writer import ConsoleOutputWriter

class LayerCoordinator:
    def __init__(self, input_file_path: str):
        # self._input_layer = FileInputParser(input_file_path)
        self._input_layer = ConsoleInputParser()
        self._plateau = Plateau()
        self._output_layer = ConsoleOutputWriter()
        
    def run(self):
        self._input_layer.setup()
        try:
            plateau_size = self._input_layer.get_plateau_size()
            self._plateau.set_dimensions(plateau_size)
            
            
            for rover_start in self._input_layer.get_rovers_starts():
                self._plateau.add_rover(rover_start)
                
                for instruction in self._input_layer.get_rover_instructions():
                    try:
                        self._plateau.move_rover(instruction)
                    except Exception as e:
                        # Throw the exception to the input layer.
                        # This will either handle it gracefully or re-raise it to the user.
                        self._input_layer.logic_error_raised(e)
                
            self._output_layer.write(self._plateau.to_output_data())
        finally:
            self._input_layer.cleanup()

