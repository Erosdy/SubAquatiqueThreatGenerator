import random

from src.entities.fish import Fish
from src.managers.entity_manager import EntityManager


class FishesManager(EntityManager):
    show_animals = True
    delay_min_s = 0.25
    delay_max_s = 3.0
    min_speed = 2
    max_speed = 3
    timer_last_fish = 0.0
    delay_next_fish = None

    def __init__(self, show_animals, delay_min_s, delay_max_s, min_speed, max_speed):
        super().__init__(10)
        self.show_animals = show_animals
        self.delay_min_s = delay_min_s
        self.delay_max_s = delay_max_s
        self.min_speed = min_speed
        self.max_speed = max_speed

        self.set_delay_next_fish()

    def set_delay_next_fish(self):
        self.delay_next_fish = random.uniform(self.delay_min_s, self.delay_max_s)

    def generate_fishes(self, timer):
        delay_since_last_fish = timer - self.timer_last_fish
        if len(self.entities) < self.max_entities and delay_since_last_fish >= self.delay_next_fish:
            fish = Fish(min_speed=self.min_speed, max_speed=self.max_speed)
            self.entities.append(fish)
            self.timer_last_fish = timer
            self.set_delay_next_fish()

    def display_entities(self):
        copy_fish = []
        for entity in self.entities:
            entity.move()
            if entity.is_in_screen():
                copy_fish.append(entity)
            entity.display_entity()
        self.entities = copy_fish

    def manage_entities(self, timer):
        if self.show_animals:
            self.display_entities()
            self.generate_fishes(timer)
