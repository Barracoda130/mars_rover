

from mars_rover.src.common.button_data import ButtonData, ButtonType
from mars_rover.src.common.enums import CompassDirection
from mars_rover.src.common.position import Position
from mars_rover.src.common.size import PlateauSize
from mars_rover.src.output_layer.pygame_objects.button import Button
from mars_rover.src.output_layer.pygame_objects.text_input import TextInput
from mars_rover.src.output_layer.output_data import OutputData
from mars_rover.src.output_layer.output_writer import OutputWriter
from mars_rover.src.common.exceptions import MarsRoverException
import pygame


class PygameOutputWriter(OutputWriter):
    _ROVER_ROTATION_ANGLES = {
        CompassDirection.NORTH: 0,
        CompassDirection.EAST: -90,
        CompassDirection.SOUTH: 180,
        CompassDirection.WEST: 90
    }
    
    _SCREEN_WIDTH = 800
    _SCREEN_HEIGHT = 600
    
    _CREATE_PLATEAU_BUTTON = Button(x=int(_SCREEN_WIDTH/2 - 110), 
                                    y=int(_SCREEN_HEIGHT/2 + 55), 
                                    width=220, 
                                    height=50, 
                                    label="Create Plateau")
    def __init__(self):
        self._previous_output_data = OutputData(plateau_size=PlateauSize(0, 0), rovers=[])
        self._canvas = None
        self._plateau_size_input = TextInput(
            int(self._SCREEN_WIDTH / 2 - 110),
            int(self._SCREEN_HEIGHT / 2 - 30),
            220,
            50,
        )
        self._plateau_size_error = ""
        
        
    def setup(self) -> None:
        pygame.init()
        self._canvas = pygame.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        pygame.display.set_caption("Mars Rover Simulation")

    def get_canvas(self) -> pygame.Surface:
        if self._canvas is None:
            raise MarsRoverException("Pygame must be initialized before calling this method.")
        return self._canvas

    def _create_plateau_button_clicked(self, click_position: tuple[int, int]) -> ButtonData:
        if self._CREATE_PLATEAU_BUTTON.is_clicked(click_position):
            dimensions = self._plateau_size_input.text.split()
            if len(dimensions) != 2:
                self._plateau_size_error = "Enter width and height, for example: 5 5"
                return ButtonData(ButtonType.NONE, None)

            try:
                width, height = (int(dimension) for dimension in dimensions)
            except ValueError:
                self._plateau_size_error = "Width and height must be whole numbers"
                return ButtonData(ButtonType.NONE, None)

            if width <= 0 or height <= 0:
                self._plateau_size_error = "Width and height must be greater than zero"
                return ButtonData(ButtonType.NONE, None)

            self._plateau_size_error = ""
            return ButtonData(ButtonType.PLATEAU_SIZE, PlateauSize(width, height))

        return ButtonData(ButtonType.NONE, None)

    def handle_event(self, event: pygame.event.Event) -> None:
        self._plateau_size_input.handle_event(event)
    
    def _plateau_grid_clicked(self, click_position: tuple[int, int]) -> ButtonData:
        # Implement logic to determine if a grid cell was clicked and return the appropriate ButtonData
        # For now, just return NONE
        return ButtonData(ButtonType.NONE, None)

    def button_click_callback(self, click_position: tuple[int, int]) -> ButtonData:
        if self._previous_output_data.plateau_size.width <= 0 or self._previous_output_data.plateau_size.height <= 0:
            if self._CREATE_PLATEAU_BUTTON.is_clicked(click_position):
                return ButtonData(ButtonType.PLATEAU_SIZE, Position(1, 1))
        
        return self._plateau_grid_clicked(click_position)
    
    def _write_create_plateau_screen(self) -> None:
        canvas = self.get_canvas()
        canvas.fill("white")
        font = pygame.font.Font(None, 32)
        
        label = font.render("Plateau size (width height):", True, "black")
        label_rect = label.get_rect(centerx=self._SCREEN_WIDTH // 2, bottom=self._plateau_size_input.rect.top - 10)
        canvas.blit(label, label_rect)
        
        self._plateau_size_input.draw(canvas)
        self._CREATE_PLATEAU_BUTTON.draw(canvas)

        for event in pygame.event.get():
            self._plateau_size_input.handle_event(event)
            self._CREATE_PLATEAU_BUTTON.handle_event(event)

        if self._plateau_size_error:
            error_font = pygame.font.Font(None, 24)
            error = error_font.render(self._plateau_size_error, True, "red")
            error_rect = error.get_rect(centerx=self._SCREEN_WIDTH // 2, top=self._CREATE_PLATEAU_BUTTON.y + 65)
            canvas.blit(error, error_rect)
            
        pygame.display.update()
    

    def write(self, data: OutputData):
        
        canvas = self.get_canvas()
        canvas.fill("grey51")
        
        if data.plateau_size.width <= 0 or data.plateau_size.height <= 0:
            self._write_create_plateau_screen()
        else:
            self._write_plateau_grid(data)
        
    def _write_plateau_grid(self, data: OutputData) -> None:
        canvas = self.get_canvas()
        
        top_start = 50
        left_start = 50
        
        grid_width = 700
        grid_height = 500

        square_size = min(grid_width/data.plateau_size.width, grid_height/data.plateau_size.height)
        
        # if self._previous_output_data.plateau_size != data.plateau_size:
        for i in range(data.plateau_size.height + 1):
            pygame.draw.line(canvas, "black", (left_start, top_start + i * square_size), (left_start + data.plateau_size.width * square_size, top_start + i * square_size))
        for i in range(data.plateau_size.width + 1):
            pygame.draw.line(canvas, "black", (left_start + i * square_size, top_start), (left_start + i * square_size, top_start + data.plateau_size.height * square_size))
        
        # if self._previous_output_data.rovers != data.rovers:
        rover_img = pygame.image.load("data/rover.png")
        rover_scaled = pygame.transform.scale(rover_img, (square_size, square_size))
        for rover in data.rovers:
            rover_x = left_start + (rover.position.x - 1) * square_size
            rover_y = top_start + (data.plateau_size.height - rover.position.y) * square_size
            rover_rotated = pygame.transform.rotate(rover_scaled, self._ROVER_ROTATION_ANGLES[rover.direction])
            canvas.blit(rover_rotated, (rover_x, rover_y))
            
        self._previous_output_data = data
        pygame.display.update()
