

from mars_rover.src.common.rover_data import RoverData
from mars_rover.src.common.size import PlateauSize


class OutputData:
    def __init__(self,
                 plateau_size: PlateauSize,
                 rovers: list[RoverData]):
        self.plateau_size = plateau_size
        self.rovers = rovers