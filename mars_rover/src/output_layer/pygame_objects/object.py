


from abc import ABC, abstractmethod

import pygame


class PygameObject(ABC):

    @abstractmethod
    def is_clicked(self, click_position: tuple[int, int]) -> bool:
        ...
        
    @abstractmethod
    def draw(self, canvas: pygame.Surface) -> None:
        ...
        
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...