import random

from src.entities.bubble import Bubble
from src.managers.entity_manager import EntityManager


class BubblesManager(EntityManager):
    show_animals: bool = True
    delay_min_s: float = 0.25
    delay_max_s: float = 3.0
    min_speed: float = 3
    max_speed: float = 8
    timer_last_bubble: float = 0
    delay_next_bubble: float = None

    def __init__(self, show_animals, delay_min_s, delay_max_s, min_speed, max_speed):
        super().__init__(3)
        self.show_animals = show_animals
        self.delay_min_s = delay_min_s
        self.delay_max_s = delay_max_s
        self.min_speed = min_speed
        self.max_speed = max_speed

        self.set_delay_next_bubble()

    def set_delay_next_bubble(self):
        self.delay_next_bubble = random.uniform(self.delay_min_s, self.delay_max_s)

    def generate_bubbles(self, timer: float):
        delay_since_last_bubble = timer - self.timer_last_bubble
        if len(self.entities) < self.max_entities and delay_since_last_bubble >= self.delay_next_bubble:
            bubble = Bubble(min_speed=self.min_speed, max_speed=self.max_speed)
            self.entities.append(bubble)
            self.timer_last_bubble = timer
            self.set_delay_next_bubble()

    def display_entities(self):
        copy_bubbles = []
        for entity in self.entities:
            entity.move()
            if entity.is_in_screen():
                copy_bubbles.append(entity)
            entity.display_entity()

        self.entities = copy_bubbles

    def manage_entities(self, timer):
        if self.show_animals:
            self.display_entities()
            self.generate_bubbles(timer)
