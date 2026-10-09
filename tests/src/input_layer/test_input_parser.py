

from mars_rover.src.input_layer.exceptions import InvalidInputException, InvalidMovementInputException, InvalidPlateauInputException, InvalidRoverInputException
from mars_rover.src.input_layer.input_parser import InputParser, CommandLineInputParser, FileInputParser
from tests.src.input_layer.constants import *
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.common.position import Position
from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.common.rover_data import RoverData
import pytest

@pytest.fixture
def valid_file_input_parser():
    return FileInputParser(VALID_INPUT_FILE_PATH)

@pytest.fixture
def invalid_file_input_parser():
    return FileInputParser(INVALID_INPUT_FILE_PATH)


def test_input_parser_parse_plateau_size_valid_inputs():
    assert FileInputParser._parse_plateau_size("5 5") == PlateauSize(5, 5)
    assert FileInputParser._parse_plateau_size("10 20") == PlateauSize(10, 20)

def test_input_parser_parse_plateau_size_invalid_inputs():
    with pytest.raises(InvalidPlateauInputException):
        FileInputParser._parse_plateau_size("5")
    with pytest.raises(InvalidPlateauInputException):
        FileInputParser._parse_plateau_size("5 5 5")
    with pytest.raises(InvalidPlateauInputException):
        FileInputParser._parse_plateau_size("five five")
        
def test_input_parser_parse_rover_start_valid_inputs():
    rover_data = FileInputParser._parse_rover_start("1 2 N")
    assert rover_data.position == Position(1, 2)
    assert rover_data.direction == CompassDirection.NORTH
    
def test_input_parser_parse_rover_start_invalid_inputs():
    with pytest.raises(InvalidRoverInputException):
        FileInputParser._parse_rover_start("1 2")
    with pytest.raises(InvalidRoverInputException):
        FileInputParser._parse_rover_start("1 2 N E")
    with pytest.raises(InvalidRoverInputException):
        FileInputParser._parse_rover_start("one two N")
        
def test_input_parser_parse_rover_instructions_valid_inputs():
    assert FileInputParser._parse_rover_instruction("L") == RoverInstruction.TURN_LEFT
    assert FileInputParser._parse_rover_instruction("R") == RoverInstruction.TURN_RIGHT
    assert FileInputParser._parse_rover_instruction("M") == RoverInstruction.MOVE_FORWARD


def test_input_parser_parse_rover_instructions_invalid_inputs():
    with pytest.raises(InvalidMovementInputException):
        FileInputParser._parse_rover_instruction("LM")
    with pytest.raises(InvalidMovementInputException):
        FileInputParser._parse_rover_instruction("1")
    with pytest.raises(InvalidMovementInputException):
        FileInputParser._parse_rover_instruction("L M R")

def test_file_input_parser_must_be_used_with_context_manager(valid_file_input_parser):
    with pytest.raises(InvalidInputException):
        parser = valid_file_input_parser
        plateau_size = parser.get_plateau_size()
        assert plateau_size == PlateauSize(5, 5)

def test_file_input_parser_get_plateau_size(valid_file_input_parser):
    with valid_file_input_parser as parser:
        plateau_size = parser.get_plateau_size()
        assert plateau_size == PlateauSize(5, 5)

def test_file_input_parser_get_plateau_size_invalid_file(invalid_file_input_parser):
    with pytest.raises(InvalidPlateauInputException):
        with invalid_file_input_parser as parser:
            parser.get_plateau_size()

def test_file_input_parser_get_rovers_starts(valid_file_input_parser):
    with valid_file_input_parser as parser:
        parser.get_plateau_size()
        starts = parser.get_rovers_starts()
        
        assert next(starts) == RoverData(Position(1, 2), CompassDirection.NORTH)
        list(parser.get_rover_instructions())
        assert next(starts) == RoverData(Position(3, 3), CompassDirection.EAST)
        
def test_file_input_parser_get_instructions_for_one_rover(valid_file_input_parser):
    with valid_file_input_parser as parser:
        parser.get_plateau_size()
        starts = parser.get_rovers_starts()
        next(starts)
        instructions = list(parser.get_rover_instructions())
        assert len(instructions) == 4
        assert instructions == [
            RoverInstruction.TURN_LEFT,
            RoverInstruction.MOVE_FORWARD,
            RoverInstruction.TURN_RIGHT,
            RoverInstruction.MOVE_FORWARD
        ]

def test_file_input_parser_full_file_read(valid_file_input_parser):
    with valid_file_input_parser as parser:
        plateau_size = parser.get_plateau_size()
        assert plateau_size == PlateauSize(5, 5)
        
        starts = parser.get_rovers_starts()
        first_rover_start = next(starts)
        assert first_rover_start == RoverData(Position(1, 2), CompassDirection.NORTH)
        
        first_rover_instructions = list(parser.get_rover_instructions())
        assert first_rover_instructions == [
            RoverInstruction.TURN_LEFT,
            RoverInstruction.MOVE_FORWARD,
            RoverInstruction.TURN_RIGHT,
            RoverInstruction.MOVE_FORWARD
        ]
        
        second_rover_start = next(starts)
        assert second_rover_start == RoverData(Position(3, 3), CompassDirection.EAST)
        
        second_rover_instructions = list(parser.get_rover_instructions())
        assert second_rover_instructions == [
            RoverInstruction.MOVE_FORWARD,
            RoverInstruction.TURN_RIGHT,
            RoverInstruction.MOVE_FORWARD,
            RoverInstruction.MOVE_FORWARD,
            RoverInstruction.TURN_LEFT
        ]
        
    

    