# player.py
import pygame
import os
import json
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from resources import resource_path

# Fallback‑Farben für Skins
FALLBACK_COLORS = {
    "default":   (200, 50, 50),
    "cat":       (150, 75, 200),
    "demon":     (100,   0, 150),
    "stickman":  (0,     0,   0),
}

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._load_skin()
        # Position & Bewegung
        self.rect        = self.image.get_rect(midbottom=(100, SCREEN_HEIGHT - 50))
        self.speed_x     = 0
        self.velocity_y  = 0
        self.on_ground   = False
        # Lebens‑ und PowerUp‑Status
        self.lives           = 5
        self.coins           = 0
        self.can_fly         = False
        self.fly_ends        = 0
        self.has_shield      = False
        self.shield_ends     = 0
        self.highjump_enabled = False
        self.highjump_ends   = 0
        # Plasma‑Munition
        self.plasma_ammo     = 0

    def _load_skin(self):
        """Lädt den in skins.json gespeicherten Skin oder fällt zurück auf Default."""
        # Standard‑Daten
        data = {"current_skin": "default"}
        fn = os.path.join(os.path.dirname(__file__), "skins.json")
        if os.path.exists(fn):
            with open(fn, "r") as f:
                data = json.load(f)
        key = data.get("current_skin", "default")
        # Versuche Bild zu laden
        img_path = resource_path(os.path.join("sprites", f"player_{key}.png"))
        if os.path.exists(img_path):
            try:
                img = pygame.image.load(img_path).convert_alpha()
            except Exception:
                img = self._make_fallback(key)
        else:
            img = self._make_fallback(key)
        # Einheitliche Größe
        self.image = pygame.transform.scale(img, (40, 40))

    def _make_fallback(self, key):
        """Erstellt ein farbiges Quadrat, wenn Skin‑Bild fehlt."""
        size = 40
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        color = FALLBACK_COLORS.get(key, FALLBACK_COLORS["default"])
        surf.fill(color)
        return surf

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0

    def jump(self):
        """Springen oder Highjump, falls aktiviert."""
        if self.on_ground or self.can_fly:
            if self.highjump_enabled:
                # Berechne Sprungkraft so, dass du fast bis oben fliegst
                h = SCREEN_HEIGHT - 50 - 10
                # v = sqrt(2*g*h), mit g≈1
                self.velocity_y = -int(math.sqrt(2 * 1 * h))
            else:
                self.velocity_y = -25
            self.on_ground = False

    def update(self, obstacles):
        now = pygame.time.get_ticks()
        # PowerUps ablaufen lassen
        if self.can_fly and now > self.fly_ends:
            self.can_fly = False
        if self.has_shield and now > self.shield_ends:
            self.has_shield = False
        if self.highjump_enabled and now > self.highjump_ends:
            self.highjump_enabled = False

        # Flugmodus
        if self.can_fly:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.rect.y += 5
            self.rect.x += self.speed_x
            # Kollision horizontal
            for o in pygame.sprite.spritecollide(self, obstacles, False):
                if self.speed_x > 0:
                    self.rect.right = o.rect.left
                elif self.speed_x < 0:
                    self.rect.left = o.rect.right
            # Begrenzung im Fenster
            self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            return

        # Normalmodus: Horizontal
        self.rect.x += self.speed_x
        for o in pygame.sprite.spritecollide(self, obstacles, False):
            if self.speed_x > 0:
                self.rect.right = o.rect.left
            elif self.speed_x < 0:
                self.rect.left = o.rect.right

        # Gravitation
        self.velocity_y = min(self.velocity_y + 1, 20)
        self.rect.y += self.velocity_y
        # Vertikale Kollision
        for o in pygame.sprite.spritecollide(self, obstacles, False):
            if self.velocity_y > 0:
                self.rect.bottom = o.rect.top
                self.on_ground   = True
                self.velocity_y  = 0
            elif self.velocity_y < 0:
                self.rect.top    = o.rect.bottom
                self.velocity_y  = 0

        # Bodenbegrenzung
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground   = True
            self.velocity_y  = 0

    def handle_damage(self):
        """Verbraucht Schild oder zieht Leben ab."""
        if self.has_shield:
            self.has_shield = False
            return True
        self.lives -= 1
        return False

    def draw(self, screen):
        """Zeichnet den Spieler und ggf. die Schild‑Umrandung."""
        screen.blit(self.image, self.rect)
        if self.has_shield:
            pygame.draw.ellipse(screen, (255,255,0), self.rect.inflate(10,10), 3)
