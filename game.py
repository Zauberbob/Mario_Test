import pygame
import sys
from player import Player
from obstacles import Obstacle, Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Super Mario Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.load_level()

        # Sound entfernt

    def load_level(self):
        obstacle = Obstacle(400, 500, 50, 50)
        self.obstacles.add(obstacle)
        enemy = Enemy(600, 500)
        self.enemies.add(enemy)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_SPACE] and self.player.on_ground:
            self.player.jump()
            # self.jump_sound.play()  # entfernt

    def update(self):
        self.player.update()
        self.obstacles.update()
        self.enemies.update()

        obstacle_hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        if obstacle_hits:
            self.player.rect.x -= 5

        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.enemies.draw(self.screen)
        pygame.display.flip()

class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Start Screen")

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 100, 255))  # Blau

        self.font = pygame.font.SysFont(None, 48)
        self.text = self.font.render("Drücke ENTER zum Starten", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 300))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.text, self.text_rect)
            pygame.display.flip()

        return Game()