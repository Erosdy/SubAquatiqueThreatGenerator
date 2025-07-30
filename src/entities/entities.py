from abc import ABC, abstractmethod

import pygame

from src.orientation import Orientation


class Entities(ABC):
    x = 0
    y = 0
    width = 0
    height = 0
    speed = 0
    img = None

    @abstractmethod
    def draw_entite(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def load_image_safe(self, path, orientation):
        if orientation == Orientation.LEFT:
            angle = 180
        elif orientation == Orientation.UP:
            angle = 90
        elif orientation == Orientation.DOWN:
            angle = -90
        else:
            angle = 0
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.rotate(img, angle)
        except Exception:
            img = self.draw_entite()
            return pygame.transform.rotate(img, angle)