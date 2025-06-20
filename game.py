# game.py
import pygame
import sys
import os
import random
import json

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from resources import resource_path
from player import Player
from obstacles import Obstacle, Enemy
from powerups import PowerUp
from plasma import PlasmaBall
from coin import Coin
from highscore import HighScore
from pause_menu import PauseMenu
from highscore_entry import HighScoreEntryScreen
from highscore_display import HighScoreDisplayScreen
from end_screen import EndScreen

FPS = 60
SKINS_JSON = os.path.join(os.path.dirname(__file__), "skins.json")

# Farben
SKY_BLUE = (135, 206, 235)
WHITE    = (255, 255, 255)
BLACK    = (0, 0, 0)
GREEN    = (50, 205, 50)

# Schriftarten (werden in _load_assets gesetzt)
FONT_SYS_36 = None
FONT_SYS_48 = None
FONT_SYS_72 = None

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # Display muss bereits gesetzt sein, z.B. in main.py
        self.screen  = pygame.display.get_surface()
        self.clock   = pygame.time.Clock()
        self.running = True

        self.score        = 0
        self.stage        = 1
        self.real_spawns  = 0
        self.prev_on_ground = True  # für Landerkennung

        self._load_assets()
        self._load_persistent_coins()
        self._setup_initial_state()

    def _load_assets(self):
        # Hintergrundmusik
        bgm_path = resource_path(os.path.join("sounds", "bg_music.mp3"))
        if os.path.exists(bgm_path):
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)

        # Jump‑Sound
        jump_path = resource_path(os.path.join("sounds", "jump.wav"))
        self.jump_sound = pygame.mixer.Sound(jump_path) if os.path.exists(jump_path) else None

        # Plasma‑Shot‑Sound
        plasma_shot_path = resource_path(os.path.join("sounds", "plasma_shot.wav"))
        self.plasma_sound = pygame.mixer.Sound(plasma_shot_path) if os.path.exists(plasma_shot_path) else None

        # Stomp/Land‑Sound
        stomp_path = resource_path(os.path.join("sounds", "stomp.wav"))
        self.stomp_sound = pygame.mixer.Sound(stomp_path) if os.path.exists(stomp_path) else None

        # Coin‑Icon fürs HUD
        coin_icon_path = resource_path(os.path.join("sprites", "coin.png"))
        if os.path.exists(coin_icon_path):
            raw = pygame.image.load(coin_icon_path).convert_alpha()
            self.coin_icon = pygame.transform.scale(raw, (24, 24))
        else:
            self.coin_icon = None

        # Fonts
        global FONT_SYS_36, FONT_SYS_48, FONT_SYS_72
        FONT_SYS_36 = pygame.font.SysFont(None, 36)
        FONT_SYS_48 = pygame.font.SysFont(None, 48)
        FONT_SYS_72 = pygame.font.SysFont(None, 72)

    def _load_persistent_coins(self):
        self.persistent_coins = 0
        if os.path.exists(SKINS_JSON):
            with open(SKINS_JSON, "r") as f:
                data = json.load(f)
                self.persistent_coins = data.get("coins", 0)

    def _save_persistent_coins(self):
        data = {}
        if os.path.exists(SKINS_JSON):
            with open(SKINS_JSON, "r") as f:
                data = json.load(f)
        data["coins"] = self.persistent_coins
        with open(SKINS_JSON, "w") as f:
            json.dump(data, f)

    def _setup_initial_state(self):
        self.pause_menu        = PauseMenu(self.screen, FONT_SYS_48)
        self.highscore_manager = HighScore()
        self.player            = Player()
        self.player.coins      = self.persistent_coins

        self.obstacles              = pygame.sprite.Group()
        self.enemies                = pygame.sprite.Group()
        self.powerups               = pygame.sprite.Group()
        self.coins                  = pygame.sprite.Group()
        self.plasmas                = pygame.sprite.Group()
        self.all_scrollable_sprites = pygame.sprite.Group()
        self.clouds                 = self._create_clouds()

        now                = pygame.time.get_ticks()
        self.enemy_delay   = 2000
        self.obs_delay     = 3000
        self.pu_delay      = 8000
        self.coin_delay    = 5000
        self.last_enemy    = now
        self.last_obstacle= now
        self.last_pu       = now
        self.last_coin     = now

        self.max_enemies   = 3
        self.max_obstacles = 5

        # Startobjekte
        self._add_to_world(Obstacle(300, SCREEN_HEIGHT - 50, 200, 50))
        self._spawn_enemy()

    def _create_clouds(self):
        return [
            [random.randint(0, SCREEN_WIDTH),
             random.randint(50, SCREEN_HEIGHT // 2),
             random.randint(20, 40),
             random.uniform(0.5, 1.5)]
            for _ in range(6)
        ]

    def run(self):
        while self.running:
            dt     = self.clock.tick(FPS)
            action = self._handle_events()
            if action:
                return action
            self._update(dt)
            self._draw()
        return self._show_game_over_screen()

    def _handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "QUIT"
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "QUIT"
                if ev.key == pygame.K_SPACE and (self.player.on_ground or self.player.can_fly):
                    self.player.jump()
                    if self.jump_sound:
                        self.jump_sound.play()
                elif ev.key == pygame.K_p:
                    res = self.pause_menu.run()
                    if res:
                        return res
                elif ev.key == pygame.K_r:
                    return "RESTART"
                elif ev.key == pygame.K_e and self.player.plasma_ammo > 0:
                    x = self.player.rect.centerx + 20
                    y = self.player.rect.centery
                    ball = PlasmaBall(x, y)
                    self.plasmas.add(ball)
                    self.all_scrollable_sprites.add(ball)
                    self.player.plasma_ammo -= 1
                    if self.plasma_sound:
                        self.plasma_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop()

        return None

    def _update(self, dt):
        now = pygame.time.get_ticks()
        was_on_ground = self.player.on_ground

        self.player.update(self.obstacles)
        # Bodenlandung erkennen
        if not was_on_ground and self.player.on_ground:
            if self.stomp_sound:
                self.stomp_sound.play()

        self._scroll_screen()
        self._update_clouds()
        self.all_scrollable_sprites.update()
        self._handle_spawning(now)
        self._handle_collisions(now)

        new_stage = min(self.score // 3000 + 1, 5)
        if new_stage != self.stage:
            self.stage = new_stage

        if self.player.lives <= 0:
            self.running = False

    def _scroll_screen(self):
        cx = self.player.rect.centerx
        if cx > SCREEN_WIDTH / 2:
            shift = cx - (SCREEN_WIDTH / 2)
            self.player.rect.centerx = SCREEN_WIDTH / 2
            for spr in self.all_scrollable_sprites:
                spr.rect.x -= shift
            for c in self.clouds:
                c[0] -= shift * 0.5

    def _update_clouds(self):
        for c in self.clouds:
            c[0] -= c[3]
            if c[0] < -c[2]:
                c[0] = SCREEN_WIDTH + c[2]
                c[1] = random.randint(50, SCREEN_HEIGHT // 2)

    def _handle_spawning(self, now):
        if now - self.last_enemy > self.enemy_delay:
            self.last_enemy = now
            self._spawn_enemy()
        if now - self.last_obstacle > self.obs_delay:
            self.last_obstacle = now
            self._spawn_obstacle()
        if now - self.last_pu > self.pu_delay:
            self.last_pu = now
            self._spawn_powerup()
        if now - self.last_coin > self.coin_delay:
            self.last_coin = now
            x = SCREEN_WIDTH + random.randint(0, 300)
            y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 70)
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_scrollable_sprites.add(coin)

    def _spawn_enemy(self):
        self.real_spawns += 1
        is_boss = (self.real_spawns % 30 == 0)
        if not is_boss and len(self.enemies) >= self.max_enemies:
            return
        typ = random.choice([1, 2, 3])
        x   = SCREEN_WIDTH + random.randint(0, 300)
        en  = Enemy(x, SCREEN_HEIGHT - 50, typ, is_boss=is_boss)
        if not en.is_boss:
            en.speed *= 2 ** (self.stage - 1)
        self._add_to_world(en)

    def _spawn_obstacle(self):
        if len(self.obstacles) < self.max_obstacles:
            w = random.randint(100, 200)
            h = random.randint(30, 50)
            x = SCREEN_WIDTH + random.randint(0, 300)
            y = SCREEN_HEIGHT - 50 - h
            self._add_to_world(Obstacle(x, y, w, h))

    def _spawn_powerup(self):
        typ = random.choice(["fly", "shield", "life", "highjump", "plasma"])
        x   = SCREEN_WIDTH + random.randint(0, 300)
        y   = SCREEN_HEIGHT - 100
        pu  = PowerUp(x, y, typ)
        self._add_to_world(pu)

    def _handle_collisions(self, now):
        # PowerUps
        for pu in pygame.sprite.spritecollide(self.player, self.powerups, True):
            pu.apply_effect(self.player, now)

        # Plasma vs. Gegner
        hits = pygame.sprite.groupcollide(self.plasmas, self.enemies, True, False)
        for ball, ens in hits.items():
            for en in ens:
                pts = 500 if en.is_boss else 100
                self.score += pts
                en.kill()

        # Kopf‑Stomp auf Gegner & Stomp-Sound
        for en in pygame.sprite.spritecollide(self.player, self.enemies, False):
            is_stomp = (
                self.player.velocity_y > 0 and
                (self.player.rect.bottom - en.rect.top) < 20
            )
            if is_stomp:
                if self.stomp_sound:
                    self.stomp_sound.play()
                en.kill()
                self.player.velocity_y = -15
                self.player.on_ground  = False
                self.score += 500 if en.is_boss else 100
                continue
            if self.player.has_shield:
                en.kill()
                self.score += 500 if en.is_boss else 100
                continue
            if en.is_boss:
                self.player.handle_damage()
                self.player.handle_damage()
            else:
                self.player.handle_damage()
            en.kill()

    def _draw(self):
        self.screen.fill(SKY_BLUE)
        for x, y, r, _ in self.clouds:
            pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), r)
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.all_scrollable_sprites.draw(self.screen)
        self.player.draw(self.screen)
        self._draw_hud()
        pygame.display.flip()

    def _draw_hud(self):
        score_txt  = FONT_SYS_36.render(f"Score: {self.score}", True, BLACK)
        lives_txt  = FONT_SYS_36.render(f"Lives: {self.player.lives}", True, BLACK)
        stage_txt  = FONT_SYS_36.render(f"Stage: {self.stage}", True, BLACK)
        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(lives_txt, (10, 50))
        self.screen.blit(stage_txt, (10, 90))

        # Coins
        if self.coin_icon:
            self.screen.blit(self.coin_icon, (SCREEN_WIDTH - 100, 10))
            coins_txt = FONT_SYS_36.render(f"x {self.player.coins}", True, BLACK)
            self.screen.blit(coins_txt, (SCREEN_WIDTH - 70, 10))
        else:
            coins_txt = FONT_SYS_36.render(f"Coins: {self.player.coins}", True, BLACK)
            self.screen.blit(coins_txt, (SCREEN_WIDTH - 200, 10))

        # PowerUp‑Status
        fly_txt    = FONT_SYS_36.render(f"Fly: {'ON' if self.player.can_fly else 'OFF'}", True, BLACK)
        shield_txt = FONT_SYS_36.render(f"Shield: {'ON' if self.player.has_shield else 'OFF'}", True, BLACK)
        hj_txt     = FONT_SYS_36.render(f"HighJump: {'ON' if self.player.highjump_enabled else 'OFF'}", True, BLACK)
        plasma_txt = FONT_SYS_36.render(f"P-Amo: {self.player.plasma_ammo}", True, (0,150,255))

        self.screen.blit(fly_txt,    (10, 130))
        self.screen.blit(shield_txt, (10, 170))
        self.screen.blit(hj_txt,     (10, 210))
        self.screen.blit(plasma_txt, (10, 250))

    def _add_to_world(self, sprite):
        if isinstance(sprite, Obstacle):
            self.obstacles.add(sprite)
        elif isinstance(sprite, Enemy):
            self.enemies.add(sprite)
        elif isinstance(sprite, PowerUp):
            self.powerups.add(sprite)
        elif isinstance(sprite, Coin):
            self.coins.add(sprite)
        elif isinstance(sprite, PlasmaBall):
            self.plasmas.add(sprite)
        self.all_scrollable_sprites.add(sprite)

    def _show_game_over_screen(self):
        entry   = HighScoreEntryScreen(self.screen, self.score, self.highscore_manager)
        entry.run()
        display = HighScoreDisplayScreen(self.screen, self.highscore_manager)
        display.run()
        end = EndScreen(self.screen, FONT_SYS_48)
        return end.run()
