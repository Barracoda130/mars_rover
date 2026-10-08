

from mars_rover.src.common.exceptions import MarsRoverException

class InvalidInputException(MarsRoverException):
    pass

class InvalidPlateauInputException(InvalidInputException):
    pass

class InvalidRoverInputException(InvalidInputException):
    pass

class InvalidMovementInputException(InvalidInputException):
    pass

class EndOfInstructionsException(MarsRoverException):
    pass