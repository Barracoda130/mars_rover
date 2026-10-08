

from mars_rover.src.input_layer.input_parser import InputParser, CommandLineInputParser, FileInputParser
from tests.src.input_layer.constants import *
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.common.position import Position
from mars_rover.src.common.enums import CompassDirection, RoverInstruction
import pytest

@pytest.fixture
def valid_file_input_parser():
    return FileInputParser(VALID_INPUT_FILE_PATH)




@pytest.mark.skip
def test_file_input_parser_parse_plateau_size_valid_inputs():
    assert FileInputParser._parse_plateau_size("5 5") == PlateauSize(5, 5)
    assert FileInputParser._parse_plateau_size("10 20") == PlateauSize(10, 20)

@pytest.mark.skip
def test_file_input_parser_parse_plateau_size_invalid_inputs():
    with pytest.raises(Exception):
        FileInputParser._parse_plateau_size("5")
    with pytest.raises(Exception):
        FileInputParser._parse_plateau_size("5 5 5")
    with pytest.raises(Exception):
        FileInputParser._parse_plateau_size("five five")
        
@pytest.mark.skip
def test_file_input_parser_parse_rover_start_valid_inputs():
    position, direction = FileInputParser._parse_rover_start("1 2 N")
    assert position == Position(1, 2)
    assert direction == CompassDirection.NORTH
    
@pytest.mark.skip
def test_file_input_parser_parse_rover_start_invalid_inputs():
    with pytest.raises(Exception):
        FileInputParser._parse_rover_start("1 2")
    with pytest.raises(Exception):
        FileInputParser._parse_rover_start("1 2 N E")
    with pytest.raises(Exception):
        FileInputParser._parse_rover_start("one two N")
        
@pytest.mark.skip
def test_file_input_parser_parse_rover_instructions_valid_inputs():
    instructions = FileInputParser._parse_rover_instructions("LMLMLMLMM")
    assert instructions == [RoverInstruction.TURN_LEFT, RoverInstruction.MOVE_FORWARD, RoverInstruction.TURN_LEFT, RoverInstruction.MOVE_FORWARD, RoverInstruction.TURN_LEFT, RoverInstruction.MOVE_FORWARD, RoverInstruction.TURN_LEFT, RoverInstruction.MOVE_FORWARD, RoverInstruction.MOVE_FORWARD]

    instructions = FileInputParser._parse_rover_instructions("RMR")
    assert instructions == [RoverInstruction.TURN_RIGHT, RoverInstruction.MOVE_FORWARD, RoverInstruction.TURN_RIGHT]

@pytest.mark.skip
def test_file_input_parser_parse_rover_instructions_invalid_inputs():
    with pytest.raises(Exception):
        FileInputParser._parse_rover_instructions("LMX")
    with pytest.raises(Exception):
        FileInputParser._parse_rover_instructions("123")
    with pytest.raises(Exception):
        FileInputParser._parse_rover_instructions("L M R")

@pytest.mark.skip
def test_file_input_parser_parse_file(valid_file_input_parser):
    parser = valid_file_input_parser
    parser._parse_file()
    
    assert parser.get_plateau_size() == PlateauSize(5, 5)
    assert parser.get_next_rover_position() == Position(1, 2)
    assert parser.get_next_rover_direction() == CompassDirection.NORTH
    
    instruction_line = "LMLMLMLMM"
    for character in instruction_line:
        assert parser.get_next_rover_instruction() == RoverInstruction(character)
        
    assert parser.get_next_rover_position() == Position(3, 3)
    assert parser.get_next_rover_direction() == CompassDirection.EAST
    instruction_line = "MMRMMRMRRM"
    for character in instruction_line:
        assert parser.get_next_rover_instruction() == RoverInstruction(character)

def test_get_next_rover_start(valid_file_input_parser):
    with valid_file_input_parser as parser:
        parser.get_plateau_size()
        
        rover_start = parser._get_next_rover_start()
        assert rover_start.position == Position(1, 2)
        assert rover_start.direction == CompassDirection.NORTH

        instruction_line = "LMLMLMLMM"
        for character in zip(parser.get_rover_instructions(), instruction_line):
            assert character[0] == RoverInstruction(character[1])
    