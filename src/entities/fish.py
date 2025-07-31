import random

import pygame

from src.entities.entities import Entities
from src.orientation import Orientation


class Fish(Entities):
    _IMG_PATH = "../ressources/Fish.png"
    _IMG = [None] * len(list(Orientation))

    def draw_entite(self):
        surface = pygame.Surface((80, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (200, 120, 60), (20, 5, 60, 30))
        pygame.draw.polygon(surface, (200, 120, 60), [(20, 20), (2, 10), (2, 30)])
        pygame.draw.circle(surface, (20, 20, 20), (62, 20), 3)  # œil
        return surface

    def move(self):
        if self.orientation == Orientation.RIGHT:
            self.x = self.x + self.speed
        elif self.orientation == Orientation.LEFT:
            self.x = self.x - self.speed
        elif self.orientation == Orientation.UP:
            self.y = self.y - self.speed
        else:
            self.y = self.y + self.speed

    def __init__(self, min_speed=2, max_speed=3):
        _direction = list(Orientation)
        self.orientation = random.choice(_direction)

        if Fish._IMG[self.orientation.value] is None :
            Fish._IMG[self.orientation.value] = self.load_image_safe(Fish._IMG_PATH, self.orientation)

        self.img = Fish._IMG[self.orientation.value]
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        window = pygame.display.get_surface()

        if self.orientation == Orientation.RIGHT:
            self.x = -self.width
            self.y = random.randint(0, window.get_height() + self.height)
        elif self.orientation == Orientation.LEFT:
            self.x =window.get_width() + self.width
            self.y = random.randint(0, window.get_height() + self.height)
        elif self.orientation == Orientation.UP:
            self.x = random.randint(0 - self.width, window.get_width() + self.width)
            self.y = window.get_height() + self.height
        else:
            self.x = random.randint(0 - self.width, window.get_width() + self.width)
            self.y = 0 - self.height

        self.speed = random.randint(min_speed, max_speed)