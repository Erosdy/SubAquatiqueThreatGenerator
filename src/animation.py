import pygame

from src.entities.bubble import Bubble
from src.entities.fish import Fish

MAX_FISHES = 500
MAX_BUBBLES = 500

def run(background_color, color_a, color_b, color_change_start, color_transition_duration,
        growth_duration, max_radius, shape_type, initial_radius, fullscreen,
        growth_mode, exp_base, exp_switch, exp_a, exp_b, exp_k,
        use_gradient_bg, gradient_color_start, gradient_color_end, show_animals,
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
    FPS = 150

    running = True
    fishes = []
    bubbles = []
    timer = 0
    timer_last_fish = -1
    timer_last_bubble = -1
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


        delay_since_last_fish = timer - timer_last_fish
        if len(fishes) < MAX_FISHES and delay_since_last_fish >= poisson_delay_min_s:
            fish = Fish()
            fishes.append(fish)
            timer_last_fish = timer

        delay_since_last_bubble = timer - timer_last_bubble
        if len(bubbles) < MAX_BUBBLES and delay_since_last_bubble >= bulle_delay_min_s:
            bubble = Bubble()
            bubbles.append(bubble)
            timer_last_bubble = timer

        if show_animals:
            copy_fish = []
            for p in fishes:
                p.move()
                if not(p.x > screen.get_width() + p.width or p.x < -p.width or p.y > screen.get_height() + p.height or p.y < -p.height) :
                    copy_fish.append(p)
                screen.blit(p.img, (int(p.x), int(p.y)))
            fishes = copy_fish

            copy_bubbles = []
            for p in bubbles:
                p.move()
                if not(p.y < -p.height):
                    copy_bubbles.append(p)
                screen.blit(p.img, (int(p.x), int(p.y)))
            bubbles = copy_bubbles



        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()