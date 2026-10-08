

class Size:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __eq__(self, other) -> bool:
        if not isinstance(other, Size):
            return NotImplemented
        return self.width == other.width and self.height == other.height

    def __str__(self) -> str:
        return f"({self.width}, {self.height})"

class PlateauSize(Size):
    pass