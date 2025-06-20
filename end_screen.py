import pygame
import sys

class EndScreen:
    def __init__(self, screen, font):
        self.screen   = screen
        self.font     = font
        self.options  = ["Play Again", "Exit"]
        self.selected = 0
        self.actions  = ["RESTART", "QUIT"]

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
                    elif ev.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif ev.key == pygame.K_RETURN:
                        return self.actions[self.selected]
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mx, my = ev.pos
                    for i, opt in enumerate(self.options):
                        txt = self.font.render(opt, True, (255,255,255))
                        r   = txt.get_rect(center=(self.screen.get_width()//2, 300 + i*60))
                        if r.collidepoint((mx, my)):
                            return self.actions[i]

            self.draw()
            clock.tick(30)

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(
            title,
            (self.screen.get_width()//2 - title.get_width()//2, 150)
        )
        for i, opt in enumerate(self.options):
            color = (255,255,0) if i == self.selected else (200,200,200)
            txt   = self.font.render(opt, True, color)
            r     = txt.get_rect(center=(self.screen.get_width()//2, 300 + i*60))
            self.screen.blit(txt, r)
        pygame.display.flip()
