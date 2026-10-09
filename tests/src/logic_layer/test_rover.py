

from mars_rover.src.common.enums import CompassDirection
from mars_rover.src.common.position import Position
from mars_rover.src.logic_layer.rover import Rover
import pytest

@pytest.fixture
def rover():
    return Rover(position=Position(1, 2), 
                 direction=CompassDirection.NORTH)

def test_rover_initialisation():
    rover = Rover(position=Position(1, 2), 
                  direction=CompassDirection.NORTH)
    assert rover.position == Position(1, 2)
    assert rover.direction == CompassDirection.NORTH
    
def test_move(rover):
    rover._move()
    assert rover.position == Position(1, 3)
    assert rover.direction == CompassDirection.NORTH
    
def test_move_invalid_direction():
    rover = Rover(position=Position(1, 2), direction="invalid")
    with pytest.raises(ValueError):
        rover._move()

def test_turn_left(rover):
    rover._turn_left()
    assert rover.direction == CompassDirection.WEST
    assert rover.position == Position(1, 2)

def test_turn_left_invalid_direction():
    rover = Rover(position=Position(1, 2), direction="invalid")
    with pytest.raises(ValueError):
        rover._turn_left()

def test_turn_right(rover):
    rover._turn_right()
    assert rover.direction == CompassDirection.EAST
    assert rover.position == Position(1, 2)

def test_turn_right_invalid_direction():
    rover = Rover(position=Position(1, 2), direction="invalid")
    with pytest.raises(ValueError):
        rover._turn_right()
    
