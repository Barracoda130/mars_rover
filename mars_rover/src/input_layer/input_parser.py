
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Generator, override
from mars_rover.src.common.position import Position
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.input_layer.exceptions import (
    EndOfInstructionsException,
    InvalidInputException, 
    InvalidPlateauInputException,
    InvalidRoverInputException,
    InvalidMovementInputException
)

from mars_rover.src.common.rover_data import RoverData

class InputParser(ABC):
    @abstractmethod
    def get_plateau_size(self) -> PlateauSize:
        ...

    @abstractmethod
    def get_rovers_starts(self) -> Generator[RoverData, None, None]:
        ...
        
    @abstractmethod
    def get_rover_instructions(self) -> Generator[RoverInstruction, None, None]:
        ...



    @staticmethod
    def _parse_plateau_size(data: str) -> PlateauSize:
        dimensions = data.split()
        if len(dimensions) != 2:
            raise InvalidPlateauInputException(f"Invalid size: expected 'X Y', received {data}")
        
        try:
            x = int(dimensions[0])
            y = int(dimensions[1])
        except ValueError:
            raise InvalidPlateauInputException(f"Invalid size: expected integers, received {data}")
        return PlateauSize(x, y)
    
    @staticmethod
    def _parse_rover_start(data: str) -> RoverData:
        parts = data.split()
        if len(parts) != 3:
            raise InvalidRoverInputException(f"Invalid start position: expected 'X Y D', received {data}")
        
        try:
            x = int(parts[0])
            y = int(parts[1])
        except ValueError:
            raise InvalidRoverInputException(f"Invalid start position: expected integers for X and Y, received {data}")
        
        direction_str = parts[2]
        try:
            direction = CompassDirection(direction_str)
        except ValueError:
            raise InvalidRoverInputException(f"Invalid start position: expected a valid direction (N, E, S, W), received {direction_str}")
        
        return RoverData(Position(x, y), direction)

    @staticmethod
    def _parse_rover_instruction(data: str) -> RoverInstruction:
        try:
            return RoverInstruction(data)

        except ValueError:
            raise InvalidMovementInputException(f"Invalid movement instruction: expected 'M', 'L', or 'R', received {data}")


class CommandLineInputParser(InputParser):
    pass
  



class FileInputParser(InputParser):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._file = None
       
        
    def __enter__(self):
        self._file = open(self._file_path, 'r')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._file:
            self._file.close()
        self._file = None

    def ensure_file_open(self) -> TextIOWrapper:
        if self._file is None:
            raise InvalidInputException("File not opened. Use 'with' statement to open the file.")

        return self._file

    @override
    def get_plateau_size(self) -> PlateauSize:
        file = self.ensure_file_open()
        
        line = file.readline().strip()

        return self._parse_plateau_size(line)
    
    def _get_next_rover_instruction(self) -> RoverInstruction|None:
        file = self.ensure_file_open()

        character = file.read(1)
        if character in ['', '\n']:
            return None
        
        return self._parse_rover_instruction(character)
    
    def _get_next_rover_start(self) -> RoverData|None:
        file = self.ensure_file_open()
        
        line = file.readline().strip()
        if not line:
            return None
        
        return self._parse_rover_start(line)

    @override
    def get_rover_instructions(self) -> Generator[RoverInstruction, None, None]:
        while instruction := self._get_next_rover_instruction():
            yield instruction
    
    @override     
    def get_rovers_starts(self) -> Generator[RoverData, None, None]:
        while start := self._get_next_rover_start():
            yield start
        