import random

from src.entities.fish import Fish

class FishesManager:
    MAX_FISHES = 10

    show_animals = True
    delay_min_s = 0.25
    delay_max_s = 3.0
    min_speed = 2
    max_speed = 3
    timer_last_fish = 0.0
    delay_next_fish = None

    fishes = []

    def __init__(self, show_animals, delay_min_s, delay_max_s, min_speed, max_speed):
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
        if len(self.fishes) < FishesManager.MAX_FISHES and delay_since_last_fish >= self.delay_next_fish:
            fish = Fish(min_speed=self.min_speed, max_speed=self.max_speed)
            self.fishes.append(fish)
            self.timer_last_fish = timer
            self.set_delay_next_fish()

    def display_fishes(self, screen):
        copy_fish = []
        for p in self.fishes:
            p.move()
            if not(p.x > screen.get_width() + p.width or p.x < -p.width or p.y > screen.get_height() + p.height or p.y < -p.height) :
                copy_fish.append(p)
            screen.blit(p.img, (int(p.x), int(p.y)))
        self.fishes = copy_fish

    def manage_fishes(self, timer, screen):
        if self.show_animals:
            self.display_fishes(screen)
            self.generate_fishes(timer)

