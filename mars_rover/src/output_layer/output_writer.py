

from mars_rover.src.output_layer.output_data import OutputData


class OutputWriter:
    pass

class ConsoleOutputWriter(OutputWriter):
    DIRECTION_TO_SYMBOL = {
        "N": "^",
        "E": ">",
        "S": "v",
        "W": "<"
    }
    
    def write(self, data: OutputData):
        for row_idx in range(data.plateau_size.height, 0, -1):
            print("+---" * data.plateau_size.width + "+")
            row = ""
            for col_idx in range(1, data.plateau_size.width + 1):
                rover_found = False
                for rover in data.rovers:
                    if rover.position.x == col_idx and rover.position.y == row_idx:
                        row += f"| {self.DIRECTION_TO_SYMBOL[rover.direction.value]} "
                        rover_found = True
                        break
                if not rover_found:
                    row += "|   "
                
            row += "|"
            print(row)

        print("+---" * data.plateau_size.width + "+")