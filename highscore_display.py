import pygame
import sys

class HighScoreDisplayScreen:
    def __init__(self, screen, highscore_manager):
        self.screen = screen
        self.highscore_manager = highscore_manager
        self.font_big    = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.btn_font   = pygame.font.SysFont(None, 56)
        self.btn_rect   = pygame.Rect(0, 0, 200, 60)
        self.btn_rect.center = (self.screen.get_width() // 2, 550)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                    return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if self.btn_rect.collidepoint(ev.pos):
                        return

            self.draw()
            clock.tick(30)

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font_big.render("High Scores", True, (255, 0, 0))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 50))

        scores = self.highscore_manager.get_scores()
        for i, entry in enumerate(scores):
            txt = f"{i+1}. {entry['name']}: {entry['score']}"
            surf = self.font_medium.render(txt, True, (255, 255, 255))
            self.screen.blit(surf, (self.screen.get_width()//2 - surf.get_width()//2, 150 + i*60))

        btn_txt = self.btn_font.render("Weiter", True, (0, 0, 0))
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_rect)
        self.screen.blit(
            btn_txt,
            (self.btn_rect.centerx - btn_txt.get_width()//2,
             self.btn_rect.centery - btn_txt.get_height()//2)
        )

        pygame.display.flip()
