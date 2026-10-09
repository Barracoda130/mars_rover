

from mars_rover.src.common.enums import CompassDirection, RoverInstruction
from mars_rover.src.common.position import Position
from mars_rover.src.common.rover_data import RoverData
from mars_rover.src.logic_layer.plateau import Plateau
from mars_rover.src.common.size import PlateauSize
import pytest


def test_initialisation():
    plateau = Plateau()
    assert plateau._size == PlateauSize(0, 0)
    assert plateau._rovers == []

    
def test_set_dimensions():
    plateau = Plateau()
    plateau.set_dimensions(PlateauSize(5, 5))
    assert plateau._size == PlateauSize(5, 5)
    
def test_add_rover():
    plateau = Plateau()
    plateau.add_rover(RoverData(Position(1, 2), CompassDirection.NORTH))
    assert len(plateau._rovers) == 1
    assert plateau._rovers[0].position == Position(1, 2)
    assert plateau._rovers[0].direction == CompassDirection.NORTH
    assert plateau._current_rover is not None
    assert plateau._current_rover.position == Position(1, 2)
    assert plateau._current_rover.direction == CompassDirection.NORTH

def test_move_rover():
    plateau = Plateau()
    plateau.add_rover(RoverData(Position(1, 2), CompassDirection.NORTH))
    plateau.move_rover(RoverInstruction.MOVE_FORWARD)
    assert plateau._current_rover is not None
    assert plateau._current_rover.position == Position(1, 3)
    assert plateau._current_rover.direction == CompassDirection.NORTH

def test_to_outpu_data():
    plateau = Plateau()
    plateau.set_dimensions(PlateauSize(5, 5))
    plateau.add_rover(RoverData(Position(1, 2), CompassDirection.NORTH))
    plateau.add_rover(RoverData(Position(3, 3), CompassDirection.EAST))
    output_data = plateau.to_output_data()
    
    assert output_data.plateau_size == PlateauSize(5, 5)
    assert len(output_data.rovers) == 2
    assert output_data.rovers[0].position == Position(1, 2)
    assert output_data.rovers[0].direction == CompassDirection.NORTH
    assert output_data.rovers[1].position == Position(3, 3)
    assert output_data.rovers[1].direction == CompassDirection.EAST