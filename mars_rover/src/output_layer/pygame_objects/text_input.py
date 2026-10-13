

from time import time
from typing import override

import pygame

from mars_rover.src.output_layer.pygame_objects.object import PygameObject

class TextInput(PygameObject):
    _CURSOR_BLINK_INTERVAL_SECONDS = 0.5  # seconds
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self._active = False
        self._cursor_timer = time()
        
    @override
    def is_clicked(self, click_position: tuple[int, int]) -> bool:
        return self.rect.collidepoint(click_position)

    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        print(f"Handling event: {event}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._active = self.is_clicked(event.pos)
            print(f"TextInput clicked: {self._active} at {event.pos}")
        elif event.type == pygame.KEYDOWN and self._active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN and event.unicode.isprintable():
                self.text += event.unicode

    @override
    def draw(self, canvas: pygame.Surface) -> None:
        border_colour = "blue" if self._active else "black"
        pygame.draw.rect(canvas, "white", self.rect)
        pygame.draw.rect(canvas, border_colour, self.rect, 2)
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, True, "black")
        text_rect = text.get_rect(midleft=(self.rect.left + 8, self.rect.centery))
        self._draw_cursor(canvas)
        canvas.blit(text, text_rect)
        
    def _draw_cursor(self, canvas: pygame.Surface) -> None:
        if self._active:
            if time() - self._cursor_timer >= self._CURSOR_BLINK_INTERVAL_SECONDS * 2:
                # Reset timer and draw cursor
                self._cursor_timer = time()
            elif time() - self._cursor_timer >= self._CURSOR_BLINK_INTERVAL_SECONDS:
                return  # Don't draw the cursor (blink off)
            
                
            font = pygame.font.Font(None, 32)
            cursor_x = self.rect.left + 8 + font.size(self.text)[0]
            cursor_y = self.rect.top + (self.rect.height - font.get_height()) // 2
            pygame.draw.line(canvas, "black", (cursor_x, cursor_y), (cursor_x, cursor_y + font.get_height()), 2)