import pygame
import os
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((180, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # Wenn das Hindernis vollständig links aus dem Bildschirm gelaufen ist,
        # entferne es aus seiner Gruppe.
        if self.rect.right < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, typ=1):
        super().__init__()
        fn = f"enemy{typ}.png"
        path = os.path.join("sprites", fn)
        if os.path.exists(path):
            self.image = pygame.image.load(path).convert_alpha()
        else:
            cmap = {1:(0,150,0),2:(150,0,150),3:(0,150,150)}
            c = cmap.get(typ,(0,255,0))
            self.image = pygame.Surface((50,50))
            self.image.fill(c)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = 550
        self.speed = random.choice([3,5,7])

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = 800 + self.rect.width + random.randint(0,300)