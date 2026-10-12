

import pygame


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, label: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label

    def is_clicked(self, click_position: tuple[int, int]) -> bool:
        click_x, click_y = click_position
        return (self.x <= click_x <= self.x + self.width) and (self.y <= click_y <= self.y + self.height)
    
    def draw(self, canvas):
        pygame.draw.rect(canvas, "blue", (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, True, "white")
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        canvas.blit(text, text_rect)


class TextInput:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN and event.unicode.isprintable():
                self.text += event.unicode

    def draw(self, canvas) -> None:
        border_colour = "blue" if self.active else "black"
        pygame.draw.rect(canvas, "white", self.rect)
        pygame.draw.rect(canvas, border_colour, self.rect, 2)
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, True, "black")
        text_rect = text.get_rect(midleft=(self.rect.left + 8, self.rect.centery))
        canvas.blit(text, text_rect)