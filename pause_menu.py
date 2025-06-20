# pause_menu.py
import pygame
import sys

class PauseMenu:
    def __init__(self, screen, font):
        self.screen    = screen
        self.font      = font
        # Optionen: Weiter, Musik an/aus, Neustart, Beenden
        self.options   = ["Weiter", "Musik: AN", "Neustart", "Beenden"]
        self.selected  = 0
        # Aktionen parallel zu Optionen
        self.actions   = [None, "TOGGLE_MUSIC", "RESTART", "QUIT"]

        # Musik‑Status initial ermitteln
        self.music_on = pygame.mixer.music.get_busy()
        self._update_music_label()

    def _update_music_label(self):
        label = "AN" if self.music_on else "AUS"
        self.options[1] = f"Musik: {label}"

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Vorbereitung: Rects für Maus‑Interaktion
            menu_rects = []
            for i, opt in enumerate(self.options):
                txt = self.font.render(opt, True, (255,255,255))
                r = txt.get_rect(center=(self.screen.get_width()//2, 200 + i * 60))
                menu_rects.append((r, i))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Tastatursteuerung
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif ev.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif ev.key == pygame.K_RETURN:
                        return self._activate(self.selected)

                # Maus‑Hover
                elif ev.type == pygame.MOUSEMOTION:
                    mx, my = ev.pos
                    for r, idx in menu_rects:
                        if r.collidepoint(mx, my):
                            self.selected = idx

                # Maus‑Klick
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mx, my = ev.pos
                    for r, idx in menu_rects:
                        if r.collidepoint(mx, my):
                            # Bei Musik‑Toggle: nur umschalten, nicht schließen
                            if self.actions[idx] == "TOGGLE_MUSIC":
                                self._toggle_music()
                                break  # raus aus dem for, aber bleibe im Menü
                            else:
                                return self._activate(idx)

            # Zeichnen
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            for i, opt in enumerate(self.options):
                color = (255, 255, 0) if i == self.selected else (255, 255, 255)
                txt_surf = self.font.render(opt, True, color)
                r = txt_surf.get_rect(center=(self.screen.get_width()//2, 200 + i * 60))
                self.screen.blit(txt_surf, r)

            pygame.display.flip()
            clock.tick(30)

    def _activate(self, idx):
        action = self.actions[idx]
        return action

    def _toggle_music(self):
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_on = False
        else:
            pygame.mixer.music.unpause()
            self.music_on = True
        self._update_music_label()
