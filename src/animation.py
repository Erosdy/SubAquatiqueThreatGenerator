import pygame

from src.managers.bubbles_manager import BubblesManager
from src.managers.fishes_manager import FishesManager



def run(background_color, color_a, color_b, color_change_start, color_transition_duration,
        growth_duration, max_radius, shape_type, initial_radius, fullscreen,
        growth_mode, exp_base, exp_switch, exp_a, exp_b, exp_k,
        use_gradient_bg, gradient_color_start, gradient_color_end, show_animals,
        bulle_speed_min, bulle_speed_max,
        bulle_delay_min_s, bulle_delay_max_s,
        poisson_delay_min_s, poisson_delay_max_s,
        poisson_speed_min, poisson_speed_max):

    pygame.init()

    fishes_manager = FishesManager(show_animals=show_animals, delay_min_s=poisson_delay_min_s, delay_max_s=poisson_delay_max_s,min_speed=poisson_speed_min, max_speed=poisson_speed_max)
    bubbles_manager = BubblesManager(show_animals=show_animals, delay_min_s=bulle_delay_min_s, delay_max_s=bulle_delay_max_s,min_speed=bulle_speed_min, max_speed=bulle_speed_max)

    screen_size = (1920, 1280)
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode(screen_size, flags)
    pygame.display.set_caption("Croissance de forme symétrique")

    clock = pygame.time.Clock()
    FPS = 150

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
                    continue
                elif event.key == pygame.K_ESCAPE:
                    running = False


        fishes_manager.manage_fishes(timer, screen)
        bubbles_manager.manage_bubbles(timer, screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()