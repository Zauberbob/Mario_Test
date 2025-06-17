import pygame
import sys
import os
from game import Game

class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Super Mario Game – START")

        # Hintergrund
        bg_path = os.path.join("backgrounds", "start_screen.png")
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path).convert()
        else:
            # Fallback: einfache Farbe
            self.background = pygame.Surface((800, 600))
            self.background.fill((0, 100, 255))

        # Start-Button
        btn_path = os.path.join("sprites", "start_button.png")
        if os.path.exists(btn_path):
            self.button_image = pygame.image.load(btn_path).convert_alpha()
        else:
            # Fallback: einfacher Rechteck-Button
            self.button_image = pygame.Surface((200, 80), pygame.SRCALPHA)
            self.button_image.fill((50, 150, 250))
            font = pygame.font.SysFont(None, 48)
            txt = font.render("START", True, (255,255,255))
            txt_r = txt.get_rect(center=(100,40))
            self.button_image.blit(txt, txt_r)

        # Position des Buttons (zentriert)
        self.button_rect = self.button_image.get_rect(center=(400, 350))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Starte per Enter
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                    return Game()

                # Starte per Mausklick auf den Button
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if self.button_rect.collidepoint(ev.pos):
                        return Game()

            # Zeichnen
            self.screen.blit(self.background, (0,0))

            # optional: Hover‐Effekt
            mx, my = pygame.mouse.get_pos()
            if self.button_rect.collidepoint((mx,my)):
                # hellere Version
                btn = pygame.transform.scale(self.button_image, (210, 88))
                br = btn.get_rect(center=self.button_rect.center)
                self.screen.blit(btn, br.topleft)
            else:
                self.screen.blit(self.button_image, self.button_rect.topleft)

            pygame.display.flip()
            clock.tick(60)