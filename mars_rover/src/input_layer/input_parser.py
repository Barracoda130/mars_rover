
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Generator, override
from mars_rover.src.common.exceptions import RoverLeftPlateauException
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

    def setup(self) -> None:
        pass
        
    def cleanup(self) -> None:
        pass
    
    def logic_error_raised(self, exception: Exception) -> None:
        raise exception


    @staticmethod
    def _parse_plateau_size(data: str) -> PlateauSize:
        dimensions = data.split()
        if len(dimensions) != 2:
            raise InvalidPlateauInputException(f"Invalid size: expected 'X Y', received '{data}'")
        
        try:
            x = int(dimensions[0])
            y = int(dimensions[1])
        except ValueError:
            raise InvalidPlateauInputException(f"Invalid size: expected integers, received '{data}'")
        return PlateauSize(x, y)
    
    @staticmethod
    def _parse_rover_start(data: str) -> RoverData:
        parts = data.split()
        if len(parts) != 3:
            raise InvalidRoverInputException(f"Invalid start position: expected 'X Y D', received '{data}'")
        
        try:
            x = int(parts[0])
            y = int(parts[1])
        except ValueError:
            raise InvalidRoverInputException(f"Invalid start position: expected integers for X and Y, received '{data}'")
        
        direction_str = parts[2]
        try:
            direction = CompassDirection(direction_str.upper())
        except ValueError:
            raise InvalidRoverInputException(f"Invalid start position: expected a valid direction (N, E, S, W), received '{direction_str}'")
        
        return RoverData(Position(x, y), direction)

    @staticmethod
    def _parse_rover_instruction(data: str) -> RoverInstruction:
        try:
            return RoverInstruction(data.upper())

        except ValueError:
            raise InvalidMovementInputException(f"Invalid movement instruction: expected 'M', 'L', or 'R', received '{data}'")


class ConsoleInputParser(InputParser):
    def __init__(self):
        pass
    
    @override
    def get_plateau_size(self) -> PlateauSize:
        while True:
            data = input("Enter plateau size (X Y): ")
            try:
                return self._parse_plateau_size(data)
            except InvalidPlateauInputException as e:
                print(f"{e}. Please try again.")
            
    
    @override
    def get_rovers_starts(self) -> Generator[RoverData, None, None]:
        while True:
            data = input("Enter rover start position (X Y D) or 'done' to finish: ")
            if data.lower() == 'done':
                break
            
            try:
                yield self._parse_rover_start(data)
            except InvalidRoverInputException as e:
                print(f"{e}. Please try again.")
            
    @override
    def get_rover_instructions(self) -> Generator[RoverInstruction, None, None]:
        while True:
            data = input("Enter rover instruction (M, L, R) or 'done' to finish: ")
            if data.lower() == 'done':
                break
            
            try:
                yield self._parse_rover_instruction(data)
            except InvalidMovementInputException as e:
                print(f"{e}. Please try again.")
  
    @override
    def logic_error_raised(self, exception: Exception) -> None:
        if isinstance(exception, RoverLeftPlateauException):
            print(f"Logic error occurred: {exception}. Please try again.")
        else:
            raise exception


class FileInputParser(InputParser):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._file = None
       
        
    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def ensure_file_open(self) -> TextIOWrapper:
        if self._file is None:
            raise InvalidInputException("File not opened. Use 'with' statement or call setup() to open the file.")

        return self._file
    
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
    def setup(self) -> None:
        self._file = open(self._file_path, 'r')
    
    @override
    def cleanup(self) -> None:
        if self._file:
            self._file.close()
        self._file = None

    @override
    def get_plateau_size(self) -> PlateauSize:
        file = self.ensure_file_open()
        
        line = file.readline().strip()

        return self._parse_plateau_size(line)
    @override
    def get_rover_instructions(self) -> Generator[RoverInstruction, None, None]:
        while instruction := self._get_next_rover_instruction():
            yield instruction
    
    @override     
    def get_rovers_starts(self) -> Generator[RoverData, None, None]:
        while start := self._get_next_rover_start():
            yield start
        