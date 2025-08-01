from enum import Enum

import pygame

from src.entities.entity import Entity
from src.growth_equation import compute_growth, GrowthMode


class State(Enum):
    IDLE = 0
    GROWING = 1
    PAUSED = 2
    SHRINKING = 3


class Shape(Enum):
    CIRCLE = "circle"
    SQUARE = "square"


class Threat(Entity):
    ANIMATION_TIME = 600
    initial_color = (0, 0, 0)
    color = (0, 0, 0)
    initial_radius = 1
    radius = 1
    max_radius = 500
    shape = Shape.CIRCLE
    last_state = None
    state = State.IDLE
    local_timer = 0
    mode: GrowthMode = GrowthMode.LINEAR
    a = 0.3
    b = 0.7

    def __init__(self, shape: Shape = Shape.CIRCLE, radius=10, max_radius=500, color=(0, 0, 0), mode=GrowthMode.LINEAR,
                a=0.3, b=0.7):
        self.initial_color = color
        self.initial_radius = radius
        self.a = a
        self.b = b
        self.mode = mode
        self.shape = shape
        self.width = max_radius * 2
        self.height = max_radius * 2
        self.max_radius = max_radius
        self.img = self.draw_entite()
        screen = pygame.display.get_surface()
        self.x = screen.get_width() // 2 - self.radius
        self.y = screen.get_height() // 2 - self.radius
        self.reset()

    def display_entity(self) -> None:
        screen = pygame.display.get_surface()
        img = pygame.transform.scale(self.img, (int(self.width), int(self.height)))
        screen.blit(img, (int(self.x), int(self.y)))

    def draw_entite(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        center = surface.get_rect().center
        if self.shape == Shape.CIRCLE:
            pygame.draw.circle(surface, self.color, center, int(self.max_radius // 2))
            return surface
        else:
            rect = pygame.Rect(left=0, top=0, width=self.width, height=self.height)
            rect.center = center
            pygame.draw.rect(surface, self.color, rect)
            return surface

    def reset(self):
        self.local_timer = 0
        self.radius = self.initial_radius
        self.color = self.initial_color
        self.last_state = State.GROWING
        self.state = State.IDLE

    def pause(self):
        if self.state == State.IDLE:
            self.state = self.last_state
        else:
            self.last_state = self.state
            self.state = State.IDLE

    def move(self):
        if self.state != State.IDLE:
            self.local_timer += 1

        self.radius = self.initial_radius + self.max_radius * compute_growth(self.local_timer / self.ANIMATION_TIME, self.mode, self.a,
                                                       self.b)
        self.width = self.radius * 2
        self.height = self.radius * 2
        screen = pygame.display.get_surface()
        self.x = screen.get_width() // 2 - self.width // 2
        self.y = screen.get_height() // 2 - self.height // 2
