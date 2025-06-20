import pygame
import sys
from highscore import HighScore
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class HighScoreViewer:
    def __init__(self, screen):
        self.screen = screen
        self.highscore_manager = HighScore()
        # Fonts
        self.font_title  = pygame.font.SysFont(None, 72)
        self.font_sub    = pygame.font.SysFont(None, 48)
        self.font_scores = pygame.font.SysFont(None, 36)
        self.btn_font    = pygame.font.SysFont(None, 56)
        # Zurück‑Button
        self.btn_rect = pygame.Rect(0, 0, 200, 60)
        self.btn_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if self.btn_rect.collidepoint(ev.pos):
                        return

            self.draw()
            clock.tick(30)

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Überschrift
        title = self.font_title.render("Jump Champion", True, (255, 0, 0))
        self.screen.blit(
            title,
            (SCREEN_WIDTH//2 - title.get_width()//2, 30)
        )

        # Untertitel
        subtitle = self.font_sub.render(
            "Diese Scores musst du besiegen, um Champion zu werden!",
            True,
            (255, 255, 255)
        )
        self.screen.blit(
            subtitle,
            (SCREEN_WIDTH//2 - subtitle.get_width()//2, 120)
        )

        # Score‑Liste
        scores = self.highscore_manager.get_scores()
        for i, entry in enumerate(scores):
            text = f"{i+1}. {entry['name']}: {entry['score']}"
            surf = self.font_scores.render(text, True, (255, 255, 255))
            self.screen.blit(
                surf,
                (SCREEN_WIDTH//2 - surf.get_width()//2, 180 + i * 50)
            )

        # Zurück‑Button
        btn_txt = self.btn_font.render("Zurück", True, (0, 0, 0))
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_rect)
        self.screen.blit(
            btn_txt,
            (self.btn_rect.centerx - btn_txt.get_width()//2,
             self.btn_rect.centery - btn_txt.get_height()//2)
        )

        pygame.display.flip()
