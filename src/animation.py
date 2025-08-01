import pygame

from src.managers.bubbles_manager import BubblesManager
from src.managers.fishes_manager import FishesManager
from src.managers.threats_manager import ThreatsManager


def run(background_color, color_begin, color_end, max_radius, shape_type, initial_radius, fullscreen,
        growth_mode, end_growth, start_degrowth, animation_duration,show_animals,
        bulle_speed_min, bulle_speed_max,
        bulle_delay_min_s, bulle_delay_max_s,
        poisson_delay_min_s, poisson_delay_max_s,
        poisson_speed_min, poisson_speed_max):
    pygame.init()

    screen_size = (1920, 1280)
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode(screen_size, flags)
    pygame.display.set_caption("Croissance de forme symétrique")

    clock = pygame.time.Clock()
    FPS = 60

    fishes_manager = FishesManager(show_animals=show_animals, delay_min_s=poisson_delay_min_s,
                                   delay_max_s=poisson_delay_max_s, min_speed=poisson_speed_min,
                                   max_speed=poisson_speed_max)
    bubbles_manager = BubblesManager(show_animals=show_animals, delay_min_s=bulle_delay_min_s,
                                     delay_max_s=bulle_delay_max_s, min_speed=bulle_speed_min,
                                     max_speed=bulle_speed_max)
    threats_manager = ThreatsManager(color_begin=color_begin, color_end=color_end,
                                     max_radius=max_radius, initial_radius=initial_radius,
                                     shape_type=shape_type, growth_mode=growth_mode,
                                     end_growth=end_growth, start_degrowth=start_degrowth, animation_duration=animation_duration * FPS)

    running = True
    timer = 0
    while running:
        screen.fill(background_color)
        timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    continue
                elif event.key == pygame.K_r:
                    threats_manager.reset()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        fishes_manager.manage_entities(timer)
        bubbles_manager.manage_entities(timer)
        threats_manager.manage_entities(timer)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
