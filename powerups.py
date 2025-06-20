# powerups.py
import pygame
import os
from resources import resource_path

POWERUP_SPRITES = {
    "fly":      "powerup_fly.png",
    "shield":   "powerup_shield.png",
    "life":     "powerup_life.png",
    "highjump": "powerup_highjump.png",
    "plasma":   "powerup_plasma.png",
}

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, typ):
        super().__init__()
        self.typ = typ

        fn = POWERUP_SPRITES.get(typ)
        path = resource_path(os.path.join("sprites", fn)) if fn else None

        if fn and os.path.exists(path):
            self.image = pygame.image.load(path).convert_alpha()
        else:
            r = 20
            surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            color_map = {
                "fly":      (0, 200, 255),
                "shield":   (255, 255, 0),
                "life":     (255,   0, 255),
                "highjump": (0, 255,   0),
                "plasma":   (0, 150, 255),
            }
            color = color_map.get(typ, (200, 200, 200))
            pygame.draw.circle(surf, color, (r, r), r)
            self.image = surf

        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def apply_effect(self, player, current_time):
        if self.typ == "fly":
            player.can_fly        = True
            player.fly_ends       = current_time + 5000
        elif self.typ == "shield":
            player.has_shield     = True
            player.shield_ends    = current_time + 5000
        elif self.typ == "life":
            player.lives         += 1
        elif self.typ == "highjump":
            player.highjump_enabled = True
            player.highjump_ends    = current_time + 5000
        elif self.typ == "plasma":
            player.plasma_ammo   = 5
