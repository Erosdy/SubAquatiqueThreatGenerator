import random

from src.entities.entities import Entities
import pygame

from src.orientation import Orientation


class Bubble(Entities):
    _IMG_PATH = "../ressources/Bubble.png"
    _IMG = None

    def draw_entite(self):
        surface = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(surface, (220, 220, 255, 200), (18, 18), 16)
        pygame.draw.circle(surface, (255, 255, 255, 220), (12, 12), 4)
        return surface

    def move(self):
        self.y = self.y - self.speed

    def __init__(self, min_speed=3, max_speed=8):
        if Bubble._IMG is None:
            Bubble._IMG = self.load_image_safe(Bubble._IMG_PATH, Orientation.UP)

        self.img = Bubble._IMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        window = pygame.display.get_surface()

        self.x = random.randint(0 - self.width, window.get_width() + self.width)
        self.y = random.randint(0 - self.height, window.get_height() + self.height)

        self.speed = random.randint(min_speed, max_speed)