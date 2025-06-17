import pygame
import sys
import os
import random
from player import Player
from obstacles import Obstacle, Enemy
from powerups import PowerUp
from highscore import HighScore  # Importiere die Highscore-Klasse

class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Weiter", "Neustart", "Beenden"]
        self.selected = 0

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    if ev.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    if ev.key == pygame.K_RETURN:
                        return ["continue", "restart", "quit"][self.selected]

            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            for i, opt in enumerate(self.options):
                col = (255, 255, 0) if i == self.selected else (255, 255, 255)
                txt = self.font.render(opt, True, col)
                r = txt.get_rect(center=(400, 250 + i * 60))
                self.screen.blit(txt, r)

            pygame.display.flip()
            clock.tick(30)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Super Mario Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_sounds()
        self.pause_menu = PauseMenu(self.screen, pygame.font.SysFont(None, 48))

        # Highscore-Manager initialisieren
        self.highscore_manager = HighScore()

        self.player = Player()
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.clouds = [
            [random.randint(0, 800), random.randint(50, 200),
             random.randint(20, 40), random.uniform(0.5, 1.5)]
            for _ in range(6)
        ]

        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

        self.enemy_delay = 2000
        self.obs_delay = 3000
        self.pu_delay = 8000
        self.last_enemy = pygame.time.get_ticks()
        self.last_obstacle = pygame.time.get_ticks()
        self.last_pu = pygame.time.get_ticks()

        self.max_enemies = 3
        self.max_obstacles = 5

        # Starte mit einer Plattform + erstem Gegner
        self.obstacles.add(Obstacle(300, 550, 200, 50))
        self.spawn_enemy()
        self.world_shift = 0

    def load_sounds(self):
        mp = os.path.join("sounds", "bg_music.mp3")
        if os.path.exists(mp):
            pygame.mixer.music.load(mp)
            pygame.mixer.music.play(-1)
        jp = os.path.join("sounds", "jump.wav")
        self.jump_sound = pygame.mixer.Sound(jp) if os.path.exists(jp) else None

    def spawn_enemy(self):
        if len(self.enemies) < self.max_enemies:
            typ = random.choice([1, 2, 3])
            x = 800 + random.randint(0, 300)
            self.enemies.add(Enemy(x, 0, typ))

    def spawn_obstacle(self):
        if len(self.obstacles) < self.max_obstacles:
            w = random.randint(100, 200)
            h = random.randint(30, 50)
            x = 800 + random.randint(0, 300)
            y = 550 - h
            self.obstacles.add(Obstacle(x, y, w, h))

    def spawn_powerup(self):
        typ = random.choice(["fly", "shield", "life"])
        x = 800 + random.randint(0, 300)
        y = 500
        self.powerups.add(PowerUp(x, y, typ))

    def run(self):
        while self.running:
            dt = self.clock.tick(60)
            self.events()
            self.update(dt)
            self.draw()
        self.game_over()

    def events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()

        if keys[pygame.K_SPACE] and (self.player.on_ground or self.player.can_fly):
            self.player.jump()
            if self.jump_sound:
                self.jump_sound.play()

        # Pause-Funktionalität
        if keys[pygame.K_p]:
            action = self.pause_menu.run()
            if action == "continue":
                return
            elif action == "restart":
                self.__init__()
                return
            elif action == "quit":
                pygame.quit()
                sys.exit()

        if keys[pygame.K_r]:
            self.__init__()
            return

    def update(self, dt):
        now = pygame.time.get_ticks()

        self.player.update(self.obstacles)

        if self.player.rect.x > 400:
            shift = self.player.rect.x - 400
            self.player.rect.x = 400
            for spr in (*self.obstacles, *self.enemies, *self.powerups):
                spr.rect.x -= shift
            for c in self.clouds:
                c[0] -= shift * 0.5

        self.enemies.update()
        self.obstacles.update()
        self.powerups.update()

        for c in self.clouds:
            c[0] -= c[3]
            if c[0] < -c[2]:
                c[0] = 800 + c[2]
                c[1] = random.randint(50, 200)

        if now - self.last_enemy > self.enemy_delay:
            self.last_enemy = now
            self.spawn_enemy()
        if now - self.last_obstacle > self.obs_delay:
            self.last_obstacle = now
            self.spawn_obstacle()
        if now - self.last_pu > self.pu_delay:
            self.last_pu = now
            self.spawn_powerup()

        for pu in pygame.sprite.spritecollide(self.player, self.powerups, True):
            if pu.typ == "fly":
                self.player.can_fly = True
                self.player.fly_ends = now + 10000
            elif pu.typ == "shield":
                self.player.has_shield = True
                self.player.shield_ends = now + 10000
            else:  # life
                self.player.lives += 1

        for en in pygame.sprite.spritecollide(self.player, self.enemies, False):
            if self.player.velocity_y > 0 and (self.player.rect.bottom - en.rect.top) < 20:
                en.kill()
                self.score += 100
                self.player.velocity_y = -15
                self.player.on_ground = False
            else:
                if self.player.has_shield:
                    en.kill()
                    self.score += 100
                else:
                    en.kill()
                    self.player.lives -= 1
                    self.player.rect.x -= 50
                    if self.player.lives <= 0:
                        self.running = False

    def draw(self):
        self.screen.fill((135, 206, 235))  # Heller Himmel
        for x, y, r, _ in self.clouds:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), r)
        pygame.draw.rect(self.screen, (50, 205, 50), (0, 550, 800, 50))  # Boden

        self.obstacles.draw(self.screen)
        self.enemies.draw(self.screen)
        self.powerups.draw(self.screen)
        self.player.draw(self.screen)

        # Punkte und Statusinformationen
        self.screen.blit(self.font.render(f"Score:  {self.score}", True, (0, 0, 0)), (10, 10))
        self.screen.blit(self.font.render(f"Lives:  {self.player.lives}", True, (0, 0, 0)), (10, 50))
        self.screen.blit(self.font.render(f"Fly:     {'ON' if self.player.can_fly else 'OFF'}", True, (0, 0, 0)), (10, 90))
        self.screen.blit(self.font.render(f"Shield: {'ON' if self.player.has_shield else 'OFF'}", True, (0, 0, 0)), (10, 130))

        pygame.display.flip()  # Aktualisiere die Anzeige