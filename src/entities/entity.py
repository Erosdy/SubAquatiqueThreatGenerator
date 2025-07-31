from abc import ABC, abstractmethod

import pygame


class Entity(ABC):
    x = 0
    y = 0
    angle = 0
    width = 0
    height = 0
    speed = 0
    img = None

    @abstractmethod
    def draw_entite(self) -> pygame.Surface:
        """
        Méthode appelée en backup si l'image de l'entité n'a pas plus être chargée.
        À redéfinir dans les entités afin de "dessiner" l'entité
        """
        pass

    @abstractmethod
    def move(self) -> None:
        pass

    def is_in_screen(self) -> bool:
        """renvoie True si au moins un pixel se trouve dans l'écran, False sinon"""
        screen = pygame.display.get_surface()
        return (screen.get_width() + self.width >= self.x >= -self.width and
                screen.get_height() + self.height >= self.y >= -self.height)

    def display_entity(self) -> None:
        """applique l'image (ou le dessin) de l'entité sur l'écran à sa position"""
        screen = pygame.display.get_surface()
        img = pygame.transform.rotate(self.img, self.angle)
        screen.blit(img, (int(self.x), int(self.y)))

    def load_image_safe(self, path) -> pygame.Surface:
        """si elle est trouvée, charge l'image de l'entité, la dessine sinon"""
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception:
            return self.draw_entite()
