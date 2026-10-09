
from mars_rover.src.input_layer.exceptions import EndOfInstructionsException
from mars_rover.src.input_layer.input_parser import FileInputParser
from mars_rover.src.logic_layer.plateau import Plateau
from mars_rover.src.output_layer.output_data import OutputData
from mars_rover.src.output_layer.output_writer import ConsoleOutputWriter

class LayerCoordinator:
    def __init__(self, input_file_path: str):
        self._input_layer = FileInputParser(input_file_path)
        self._plateau = Plateau()
        self._output_layer = ConsoleOutputWriter()
        
    def run(self):
        with self._input_layer as input_layer:
            plateau_size = input_layer.get_plateau_size()
            self._plateau.set_dimensions(plateau_size)
            
            # self._output_layer.write(self._plateau.to_output_data())
            
            for rover_start in input_layer.get_rovers_starts():
                self._plateau.add_rover(rover_start)
                # self._output_layer.write(self._plateau.to_output_data())
                
                for instruction in input_layer.get_rover_instructions():
                    self._plateau.move_rover(instruction)
                    # self._output_layer.write(self._plateau.to_output_data())
                
            self._output_layer.write(self._plateau.to_output_data())
            
