from enum import Enum
import pygame

from src.growth_equation import compute_growth


class Etat(Enum):
    IDLE = 0
    GROWING = 1
    PAUSED = 2
    SHRINKING = 3


class ThreatsManager:
    etat = Etat.IDLE
    last_etat = None
    local_timer = 0
    pause_timer = 0
    color_transition_frames = 0
    color_change_start_frames = 0
    pause_frames = 0
    total_frames = 0
    pause_counter = 0
    radius = 0
    max_radius = 0
    color = None
    color_a = None
    color_b = None
    growth_mode = None
    exp_base = None
    exp_switch = None
    exp_a = None
    shape_type = None

    def __init__(self, fps, color_a, color_b, color_change_start, color_transition_duration,
        growth_duration, max_radius, shape_type, initial_radius, growth_mode, exp_base,
        exp_switch, exp_a, exp_b, exp_k, use_gradient_bg, gradient_color_start, gradient_color_end):
        self.color_a = color_a
        self.color_b = color_b
        self.total_frames = int(growth_duration * fps)
        self.color_change_start_frames = int(color_change_start * fps)
        self.color_transition_frames = int(color_transition_duration * fps)
        self.pause_frames = int(1 * fps)
        self.initial_radius = initial_radius
        self.growth_mode = growth_mode
        self.exp_base = exp_base
        self.exp_switch = exp_switch
        self.exp_a = exp_a
        self.exp_b = exp_b
        self.exp_k = exp_k
        self.use_gradient_bg = use_gradient_bg
        self.gradient_color_start = gradient_color_start
        self.gradient_color_end = gradient_color_end
        self.max_radius = max_radius
        self.shape_type = shape_type
        self.reset()

    def play_or_pause(self):
        if self.etat == Etat.IDLE:
            self.etat = self.last_etat
        else:
            self.last_etat = self.etat
            self.etat = Etat.IDLE

    def reset(self):
        self.last_etat = Etat.GROWING
        self.etat = Etat.IDLE
        self.color = self.color_a
        self.radius = self.initial_radius
        self.pause_counter = 0
        self.local_timer = 0

    def manage_threats(self, screen):
        if self.etat == Etat.SHRINKING:
            self.local_timer -= 1
        elif self.etat != Etat.IDLE:
            self.local_timer += 1

        if self.etat == Etat.GROWING:
            if self.radius < self.max_radius:
                progress = self.local_timer / self.total_frames
                growth_factor = compute_growth(progress, self.growth_mode, self.exp_base, self.exp_switch, self.exp_a, self.exp_b, self.exp_k)
                self.radius = self.initial_radius + (self.max_radius - self.initial_radius) * growth_factor
            else:
                self.radius = self.max_radius
                self.etat = Etat.PAUSED
            if self.local_timer < self.color_change_start_frames:
                self.color = self.color_a
            elif self.local_timer < (self.color_change_start_frames + self.color_transition_frames):
                t = (self.local_timer - self.color_change_start_frames) / self.color_transition_frames
                self.color = tuple(int(self.color_a[i] + (self.color_b[i] - self.color_a[i]) * t) for i in range(3))
            else:
                self.color = self.color_b
        elif self.etat == Etat.PAUSED:
            self.pause_counter += 1
            if self.pause_counter >= self.pause_frames:
                self.etat = Etat.SHRINKING
                self.local_timer = self.total_frames
        elif self.etat == Etat.SHRINKING:
            if self.radius > self.initial_radius:
                progress = self.local_timer / self.total_frames
                growth_factor = compute_growth(progress, self.growth_mode, self.exp_base, self.exp_switch, self.exp_a, self.exp_b, self.exp_k)
                self.radius = self.initial_radius + (self.max_radius - self.initial_radius) * growth_factor
            else:
                self.radius = self.initial_radius
                self.etat = Etat.IDLE
            if self.local_timer >= self.color_change_start_frames:
                self.color = self.color_b
            elif self.local_timer >= self.color_change_start_frames - self.color_transition_frames:
                t = (self.color_change_start_frames - self.local_timer) /self. color_transition_frames
                t = max(0.0, min(t, 1.0))
                self.color = tuple(int(self.color_b[i] + (self.color_a[i] - self.color_b[i]) * t) for i in range(3))
            else:
                self.color = self.color_a

        # Dessin de la forme
        if self.etat != Etat.IDLE:
            center = screen.get_rect().center   # ← au lieu d'utiliser screen_size
            if self.shape_type == "circle":
                pygame.draw.circle(screen, self.color, center, int(self.radius))
            elif self.shape_type == "square":
                side = int(self.radius) * 2
                rect = pygame.Rect(0, 0, side, side)
                rect.center = center
                pygame.draw.rect(screen, self.color, rect)

