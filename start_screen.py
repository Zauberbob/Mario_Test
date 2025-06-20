# start_screen.py
import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
from highscore_viewer import HighScoreViewer
from skin_screen import SkinScreen

class StartScreen:
    def __init__(self):
        pygame.init()
        # Fester Modus 800×600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Game – START")

        # Hintergrund laden oder Fallback
        bg_path = os.path.join("backgrounds", "start_screen.png")
        if os.path.exists(bg_path):
            bg = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((0, 100, 255))

        # Fonts
        self.title_font = pygame.font.SysFont(None, 72)
        self.btn_font   = pygame.font.SysFont(None, 48)

        # Center-Koordinaten für Buttons
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        # "SPIELEN"-Button
        self.start_img = pygame.Surface((200, 80), pygame.SRCALPHA)
        self.start_img.fill((50, 150, 250))
        txt = self.btn_font.render("SPIELEN", True, (255, 255, 255))
        self.start_img.blit(txt, txt.get_rect(center=(100, 40)))
        self.start_rect = self.start_img.get_rect(center=(cx, cy - 70))

        # "RANGLISTE"-Button
        self.hs_img = pygame.Surface((200, 80), pygame.SRCALPHA)
        self.hs_img.fill((150, 150, 50))
        txt2 = self.btn_font.render("RANGLISTE", True, (255, 255, 255))
        self.hs_img.blit(txt2, txt2.get_rect(center=(100, 40)))
        self.hs_rect = self.hs_img.get_rect(center=(cx, cy + 10))

        # "SKINS"-Button
        self.skin_img = pygame.Surface((200, 80), pygame.SRCALPHA)
        self.skin_img.fill((100, 150, 100))
        txt3 = self.btn_font.render("SKINS", True, (255, 255, 255))
        self.skin_img.blit(txt3, txt3.get_rect(center=(100, 40)))
        self.skin_rect = self.skin_img.get_rect(center=(cx, cy + 90))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # ESC to quit
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    return 'QUIT'

                # ENTER to start game
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                    return Game()

                # Mouse clicks
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mx, my = ev.pos
                    if self.start_rect.collidepoint(mx, my):
                        return Game()
                    if self.hs_rect.collidepoint(mx, my):
                        HighScoreViewer(self.screen).run()
                        pygame.event.clear()
                        self.screen.blit(self.background, (0, 0))
                        pygame.display.flip()
                        pygame.time.wait(100)
                        break
                    if self.skin_rect.collidepoint(mx, my):
                        SkinScreen(self.screen).run()
                        pygame.event.clear()
                        self.screen.blit(self.background, (0, 0))
                        pygame.display.flip()
                        pygame.time.wait(100)
                        break

            # Draw background and UI
            self.screen.blit(self.background, (0, 0))

            # Title in der Mitte
            title_surf = self.title_font.render("Jump Champion", True, (255, 0, 0))
            title_x = SCREEN_WIDTH // 2 - title_surf.get_width() // 2
            self.screen.blit(title_surf, (title_x, 50))

            # Buttons with hover
            mx, my = pygame.mouse.get_pos()
            for img, rect in [
                (self.start_img, self.start_rect),
                (self.hs_img,    self.hs_rect),
                (self.skin_img,  self.skin_rect)
            ]:
                if rect.collidepoint(mx, my):
                    bigger = pygame.transform.scale(
                        img,
                        (int(img.get_width() * 1.05), int(img.get_height() * 1.05))
                    )
                    br = bigger.get_rect(center=rect.center)
                    self.screen.blit(bigger, br.topleft)
                else:
                    self.screen.blit(img, rect.topleft)

            pygame.display.flip()
            clock.tick(60)
