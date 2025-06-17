import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Lade dein player.png oder Fallback
        path = os.path.join("sprites", "player.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
        else:
            img = pygame.Surface((50, 50), pygame.SRCALPHA)
            img.fill((200, 50, 50))
        # Skaliere auf 40×40
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect(midbottom=(100, 550))

        self.speed_x = 0
        self.velocity_y = 0
        self.on_ground = False

        self.lives = 5

        # PowerUp-Zustände
        self.can_fly = False
        self.fly_ends = 0
        self.has_shield = False
        self.shield_ends = 0

    def move_left(self):   self.speed_x = -5
    def move_right(self):  self.speed_x =  5
    def stop(self):        self.speed_x =  0

    def jump(self):
        # mit Flug-PowerUp jederzeit springen, sonst nur am Boden
        if self.on_ground or self.can_fly:
            self.velocity_y = -25
            self.on_ground = False

    def update(self, obstacles):
        now = pygame.time.get_ticks()
        # PowerUp ablaufen lassen
        if self.can_fly and now > self.fly_ends:
            self.can_fly = False
        if self.has_shield and now > self.shield_ends:
            self.has_shield = False

        # FLUG-MODUS
        if self.can_fly:
            keys = pygame.key.get_pressed()
            # vertikal steuern
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.rect.y += 5
            # horizontal wie gewohnt
            self.rect.x += self.speed_x
            # horizontale Kollision
            hits = pygame.sprite.spritecollide(self, obstacles, False)
            for o in hits:
                if self.speed_x > 0:
                    self.rect.right = o.rect.left
                elif self.speed_x < 0:
                    self.rect.left = o.rect.right
            # Bildschirmränder
            if self.rect.top < 0:      self.rect.top = 0
            if self.rect.bottom > 600: self.rect.bottom = 600
            if self.rect.left < 0:     self.rect.left = 0
            if self.rect.right > 800:  self.rect.right = 800
            return

        # NORMALER MODUS
        # 1) horizontal bewegen + Kollision
        self.rect.x += self.speed_x
        hits = pygame.sprite.spritecollide(self, obstacles, False)
        for o in hits:
            if self.speed_x > 0:
                self.rect.right = o.rect.left
            elif self.speed_x < 0:
                self.rect.left = o.rect.right

        # 2) Gravitation
        self.velocity_y += 1
        if self.velocity_y > 20:
            self.velocity_y = 20
        self.rect.y += self.velocity_y

        hits = pygame.sprite.spritecollide(self, obstacles, False)
        for o in hits:
            if self.velocity_y > 0:
                self.rect.bottom = o.rect.top
                self.on_ground = True
                self.velocity_y = 0
            elif self.velocity_y < 0:
                self.rect.top = o.rect.bottom
                self.velocity_y = 0

        # Bodenlimit
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.on_ground = True
            self.velocity_y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Schild-Umrandung
        if self.has_shield:
            pygame.draw.ellipse(screen, (255,255,0), self.rect.inflate(10,10), 3)