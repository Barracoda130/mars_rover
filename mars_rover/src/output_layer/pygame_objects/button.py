

from enum import Enum, auto
from typing import override

import pygame

from mars_rover.src.output_layer.pygame_objects.object import PygameObject

class ButtonType(Enum):
    PLATEAU_SIZE = auto()
    NEW_ROVER = auto()

class Button(PygameObject):
    def __init__(self, x: int, y: int, width: int, height: int, label: str):
        self.shape = pygame.Rect(x, y, width, height)
        self.label = label

    @override
    def is_clicked(self, click_position: tuple[int, int]) -> bool:
        return self.shape.collidepoint(click_position)

    @override
    def draw(self, canvas: pygame.Surface):
        pygame.draw.rect(canvas, "blue", self.shape)
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, True, "white")
        text_rect = text.get_rect(center=(self.shape.centerx, self.shape.centery))
        canvas.blit(text, text_rect)
        
    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(event.pos):
            print(f"Button '{self.label}' clicked at {event.pos}")


