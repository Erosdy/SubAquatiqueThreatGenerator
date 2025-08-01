from src.entities.threat import Threat, State
from src.managers.entity_manager import EntityManager


class ThreatsManager(EntityManager):
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
    exp_a = None
    exp_b = None
    shape_type = None
    pause = True

    def __init__(self, fps, color_a, color_b, color_change_start, color_transition_duration,
                 growth_duration, max_radius, shape_type, initial_radius, growth_mode,
                 exp_a, exp_b, use_gradient_bg, gradient_color_start, gradient_color_end):
        super().__init__(1)
        self.entities = [Threat(shape=shape_type, radius=initial_radius, max_radius=max_radius, color=color_a)]

        self.color_a = color_a
        self.color_b = color_b
        self.total_frames = int(growth_duration * fps)
        self.color_change_start_frames = int(color_change_start * fps)
        self.color_transition_frames = int(color_transition_duration * fps)
        self.pause_frames = int(1 * fps)
        self.initial_radius = initial_radius
        self.growth_mode = growth_mode
        self.exp_a = exp_a
        self.exp_b = exp_b
        self.use_gradient_bg = use_gradient_bg
        self.gradient_color_start = gradient_color_start
        self.gradient_color_end = gradient_color_end
        self.max_radius = max_radius
        self.shape_type = shape_type
        self.reset()

    def play_or_pause(self):
        self.pause = not self.pause
        for entity in self.entities:
            entity.pause()

    def reset(self):
        self.pause = True
        for entity in self.entities:
            entity.reset()

    def display_entities(self):
        if not self.pause:
            for threat in self.entities:
                threat.move()
                threat.display_entity()
                if threat.state == State.IDLE:
                    self.reset()

    def manage_entities(self, timer):
        self.display_entities()
