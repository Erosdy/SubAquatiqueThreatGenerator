from abc import ABC, abstractmethod

from src.entities.entity import Entity


class EntityManager(ABC):
    max_entities: int = 1
    entities: list[Entity] = []

    def __init__(self, max_entities=1):
        self.max_entities = max_entities

    @abstractmethod
    def display_entities(self):
        pass

    @abstractmethod
    def manage_entities(self, timer):
        pass
