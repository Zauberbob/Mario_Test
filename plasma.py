# plasma.py
import pygame
import os
from resources import resource_path

class PlasmaBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        path = resource_path(os.path.join("sprites", "plasma_ball.png"))
        if os.path.exists(path):
            raw = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(raw, (16, 16))
        else:
            surf = pygame.Surface((16,16), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0,150,255), (8,8), 8)
            self.image = surf

        self.rect  = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
