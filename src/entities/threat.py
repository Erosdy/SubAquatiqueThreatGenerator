from enum import Enum

import pygame

from src.entities.entity import Entity
from src.growth_equation import compute_growth, GrowthMode

class Shape(Enum):
    CIRCLE = "circle"
    SQUARE = "square"


class Threat(Entity):
    initial_color = (0, 0, 0)
    color = (0, 0, 0)
    initial_radius = 1
    radius = 0
    max_radius = 500
    shape = Shape.CIRCLE
    local_timer = 0
    mode: GrowthMode = GrowthMode.LINEAR
    animation_duration = 600
    end_growth = 0.3
    start_degrowth = 0.7

    def __init__(self, shape: Shape = Shape.CIRCLE, radius=10, max_radius=500, color=(0, 0, 0), mode=GrowthMode.LINEAR,
                 end_growth=0.3, start_degrowth=0.7, animation_duration=10):
        self.initial_color = color
        self.animation_duration = animation_duration
        self.end_growth = end_growth
        self.start_degrowth = start_degrowth
        self.mode = mode
        self.shape = shape
        self.initial_radius = radius
        self.radius = max_radius
        self.max_radius = max_radius
        self.adjuste_size()
        self.img = self.draw_entite()
        self.reset()

    def display_entity(self) -> None:
        screen = pygame.display.get_surface()
        img = pygame.transform.scale(self.img, (int(self.width), int(self.height)))
        screen.blit(img, (int(self.x), int(self.y)))

    def draw_entite(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        center = surface.get_rect().center
        if self.shape == Shape.CIRCLE:
            pygame.draw.circle(surface, self.color, center, int(self.max_radius))
            return surface
        else:
            rect = pygame.Rect(0, 0, self.width, self.height)
            pygame.draw.rect(surface, self.color, rect)
            return surface

    def reset(self):
        self.local_timer = 0
        self.radius = self.initial_radius
        self.color = self.initial_color
        self.adjuste_size()

    def adjuste_size(self):
        self.width = self.radius * 2
        self.height = self.radius * 2
        screen = pygame.display.get_surface()
        self.x = screen.get_width() // 2 - self.width // 2
        self.y = screen.get_height() // 2 - self.height // 2

    def move(self):
        self.local_timer += 1

        self.radius = self.initial_radius + self.max_radius * compute_growth(self.local_timer / self.animation_duration, self.mode, self.end_growth,
                                                                             self.start_degrowth)
        self.adjuste_size()
