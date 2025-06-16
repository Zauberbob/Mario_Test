import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))     # Rechteckgröße
        self.image.fill((255, 0, 0))              # Rot gefärbt

        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.velocity_y = 0
        self.on_ground = False

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5

    def jump(self):
        self.velocity_y = -15
        self.on_ground = False

    def update(self):
        self.velocity_y += 1  # Gravitation
        self.rect.y += self.velocity_y

        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.on_ground = True
            self.velocity_y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
