import pygame
import sys

class HighScoreEntryScreen:
    def __init__(self, screen, score, highscore_manager):
        self.screen = screen
        self.score = score
        self.highscore_manager = highscore_manager
        self.clock = pygame.time.Clock()
        
        # Schriften
        self.font_big = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)

        # UI Elemente
        self.input_box = pygame.Rect(300, 460, 200, 50)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        
        # Zustand
        self.active = False
        self.text = ''

    def run(self):
        """Startet die Schleife für den Eingabebildschirm."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            # Namen speichern und Schleife beenden
                            name_to_save = self.text if self.text else "Anonymous"
                            self.highscore_manager.add_score(name_to_save, self.score)
                            return # Beendet die run-Methode und kehrt zurück
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
            
            self.draw()
            self.clock.tick(30)

    def draw(self):
        """Zeichnet alle Elemente des Bildschirms."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        t1 = self.font_big.render("GAME OVER", True, (255, 0, 0))
        t2 = self.font_medium.render(f"Score: {self.score}", True, (255, 255, 255))
        t3 = self.font_medium.render("Gib deinen Namen ein:", True, (255, 255, 255))

        self.screen.blit(t1, (self.screen.get_width() / 2 - t1.get_width() / 2, 250))
        self.screen.blit(t2, (self.screen.get_width() / 2 - t2.get_width() / 2, 330))
        self.screen.blit(t3, (self.screen.get_width() / 2 - t3.get_width() / 2, 410))

        txt_surface = self.font_medium.render(self.text, True, (255, 255, 255))
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)

        pygame.display.flip()