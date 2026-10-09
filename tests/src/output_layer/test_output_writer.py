

from mars_rover.src.common.enums import CompassDirection
from mars_rover.src.common.position import Position
from mars_rover.src.common.rover_data import RoverData
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.output_layer.output_data import OutputData
from mars_rover.src.output_layer.output_writer import ConsoleOutputWriter

def test_console_output_writer_write(capsys):
    output_data = OutputData(
        plateau_size=PlateauSize(5, 5),
        rovers=[
            RoverData(position=Position(1, 2), 
                      direction=CompassDirection.NORTH),
            RoverData(position=Position(3, 3),
                      direction=CompassDirection.EAST)
        ]
    )
    
    writer = ConsoleOutputWriter()
    writer.write(output_data)
    captured = capsys.readouterr()
    expected_output = (
        "+---+---+---+---+---+\n"
        "|   |   |   |   |   |\n"
        "+---+---+---+---+---+\n"
        "|   |   |   |   |   |\n"
        "+---+---+---+---+---+\n"
        "|   |   | > |   |   |\n"
        "+---+---+---+---+---+\n"
        "| ^ |   |   |   |   |\n"
        "+---+---+---+---+---+\n"
        "|   |   |   |   |   |\n"
        "+---+---+---+---+---+\n"
    )
    assert captured.out == expected_output