from src.entities.threat import Threat
from src.managers.entity_manager import EntityManager


class ThreatsManager(EntityManager):
    last_etat = None
    color_transition_frames = 0
    color_change_start_frames = 0
    radius = 0
    max_radius = 0
    color = None
    color_a = None
    color_b = None
    growth_mode = None
    exp_a = None
    exp_b = None
    shape_type = None

    def __init__(self, color_a, color_b, max_radius, shape_type, initial_radius, growth_mode,
                 exp_a, exp_b, use_gradient_bg, gradient_color_start, gradient_color_end):
        super().__init__(1)
        self.entities = [Threat(shape=shape_type, radius=initial_radius, max_radius=max_radius, color=color_a, mode=growth_mode, a=exp_a, b=exp_b)]

        self.color_a = color_a
        self.color_b = color_b
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

    def reset(self):
        for entity in self.entities:
            entity.reset()

    def display_entities(self):
        for threat in self.entities:
            threat.move()
            threat.display_entity()

    def manage_entities(self, timer):
        self.display_entities()
