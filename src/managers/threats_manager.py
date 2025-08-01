from src.entities.threat import Threat
from src.managers.entity_manager import EntityManager


class ThreatsManager(EntityManager):
    last_etat = None
    radius = 0
    max_radius = 0
    color = None
    color_begin = None
    color_end = None
    growth_mode = None
    end_growth = None
    start_degrowth = None
    shape_type = None

    def __init__(self, color_begin, color_end, max_radius, shape_type, initial_radius, growth_mode,
                 end_growth, start_degrowth, animation_duration):
        super().__init__(1)
        self.entities = [Threat(shape=shape_type, radius=initial_radius, max_radius=max_radius, color=color_begin, mode=growth_mode,
                                end_growth=end_growth, start_degrowth=start_degrowth, animation_duration=animation_duration)]

        self.color_begin = color_begin
        self.color_end = color_end
        self.initial_radius = initial_radius
        self.growth_mode = growth_mode
        self.end_growth = end_growth
        self.start_degrowth = start_degrowth
        self.animation_duration = animation_duration
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
