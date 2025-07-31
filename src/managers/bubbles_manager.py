import random

from src.entities.bubble import Bubble

class BubblesManager:
    MAX_BUBBLES = 3

    show_animals = True
    delay_min_s = 0.25
    delay_max_s = 3.0
    min_speed = 3
    max_speed = 8
    timer_last_bubble = 0.0
    delay_next_bubble = None

    bubbles = []

    def __init__(self, show_animals, delay_min_s, delay_max_s, min_speed, max_speed):
        self.show_animals = show_animals
        self.delay_min_s = delay_min_s
        self.delay_max_s = delay_max_s
        self.min_speed = min_speed
        self.max_speed = max_speed

        self.set_delay_next_bubble()

    def set_delay_next_bubble(self):
        self.delay_next_bubble = random.uniform(self.delay_min_s, self.delay_max_s)

    def generate_bubbles(self, timer):
        delay_since_last_bubble = timer - self.timer_last_bubble
        if len(self.bubbles) < BubblesManager.MAX_BUBBLES and delay_since_last_bubble >= self.delay_next_bubble:
            bubble = Bubble(min_speed=self.min_speed, max_speed=self.max_speed)
            self.bubbles.append(bubble)
            self.timer_last_bubble = timer
            self.set_delay_next_bubble()

    def display_bubbles(self, screen):
        copy_bubbles = []
        for p in self.bubbles:
            p.move()
            if not(p.x > screen.get_width() + p.width or p.x < -p.width or p.y > screen.get_height() + p.height or p.y < -p.height) :
                copy_bubbles.append(p)
            screen.blit(p.img, (int(p.x), int(p.y)))
        self.bubbles = copy_bubbles

    def manage_bubbles(self, timer, screen):
        if self.show_animals:
            self.display_bubbles(screen)
            self.generate_bubbles(timer)
