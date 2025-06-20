# skin_screen.py
import pygame
import sys
import os
import json
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SKINS

class SkinScreen:
    def __init__(self, screen):
        self.screen = screen

        # Basis-Pfad zum sprites-Ordner
        self.sprites_dir = os.path.join(os.path.dirname(__file__), "sprites")

        # skins.json laden oder initialisieren
        fn = os.path.join(os.path.dirname(__file__), "skins.json")
        if os.path.exists(fn):
            with open(fn, "r") as f:
                data = json.load(f)
        else:
            data = {"current_skin": "default", "owned_skins": ["default"], "coins": 0}
        self.owned   = set(data.get("owned_skins", ["default"]))
        self.current = data.get("current_skin", "default")
        self.coins   = data.get("coins", 0)

        # Alle Skins aus config (default→Lama, cat→Katze, demon→Demon)
        self.skins = SKINS

        # Layout-Berechnung für Kacheln
        tile_w, tile_h = 180, 180
        padding = 30
        total_w = len(self.skins) * (tile_w + padding) - padding
        start_x = SCREEN_WIDTH // 2 - total_w // 2
        y_top   = SCREEN_HEIGHT // 2 - tile_h // 2

        self.tiles = []
        for i, (key, name, cost) in enumerate(self.skins):
            x = start_x + i * (tile_w + padding)
            tile_rect   = pygame.Rect(x, y_top, tile_w, tile_h)
            buy_rect    = pygame.Rect(x + 10, y_top + tile_h - 50, 80, 40)
            select_rect = pygame.Rect(x + tile_w - 90, y_top + tile_h - 50, 80, 40)
            self.tiles.append({
                "key": key, "name": name, "cost": cost,
                "tile_rect": tile_rect,
                "buy_rect": buy_rect,
                "select_rect": select_rect,
            })

        # Zurück-Button
        self.btn_back = pygame.Rect(10, 10, 100, 40)

    def run(self):
        clock = pygame.time.Clock()
        font_title  = pygame.font.SysFont(None, 48)
        font_button = pygame.font.SysFont(None, 28)

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self._save_and_exit()
                    return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mx, my = ev.pos
                    if self.btn_back.collidepoint(mx, my):
                        self._save_and_exit()
                        return
                    for tile in self.tiles:
                        key, cost = tile["key"], tile["cost"]
                        if key in self.owned:
                            if tile["select_rect"].collidepoint(mx, my):
                                self.current = key
                                self._save_and_exit()
                                return
                        else:
                            if tile["buy_rect"].collidepoint(mx, my) and self.coins >= cost:
                                self.coins -= cost
                                self.owned.add(key)
                                self.current = key
                                self._write_json()
            self._draw(font_title, font_button)
            clock.tick(30)

    def _write_json(self):
        data = {
            "current_skin": self.current,
            "owned_skins": list(self.owned),
            "coins": self.coins
        }
        fn = os.path.join(os.path.dirname(__file__), "skins.json")
        with open(fn, "w") as f:
            json.dump(data, f)

    def _save_and_exit(self):
        self._write_json()

    def _load_skin_image(self, key, max_w, max_h):
        """Lädt das Bild für Skin `key`, skaliert auf max_w×max_h oder gibt None zurück."""
        filename = f"player_{key}.png"
        path = os.path.join(self.sprites_dir, filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (max_w, max_h))
            except Exception as e:
                print(f"[SkinScreen] Fehler beim Laden von {path}: {e}")
                return None
        else:
            print(f"[SkinScreen] Bild nicht gefunden: {path}")
            return None

    def _draw(self, font_title, font_button):
        self.screen.fill((30, 30, 30))

        # Titel
        title = font_title.render("Skins kaufen / auswählen", True, (255,255,255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))

        # Münzen-Anzeige
        coins_txt = font_button.render(f"Deine Münzen: {self.coins}", True, (255,215,0))
        self.screen.blit(coins_txt, (SCREEN_WIDTH - coins_txt.get_width() - 20, 20))

        # Zeichne jede Skin-Kachel
        for tile in self.tiles:
            key, name, cost = tile["key"], tile["name"], tile["cost"]
            kr = tile["tile_rect"]
            # Hintergrund
            pygame.draw.rect(self.screen, (60,60,60), kr)

            # Skin-Bild
            img = self._load_skin_image(key, kr.width-20, kr.height-80)
            if img:
                self.screen.blit(img, (kr.x+10, kr.y+10))
            else:
                # Graues Feld als Fallback
                pygame.draw.rect(
                    self.screen, (100,100,100),
                    (kr.x+10, kr.y+10, kr.width-20, kr.height-80)
                )

            # Name
            name_surf = font_button.render(name, True, (255,255,255))
            self.screen.blit(name_surf, (kr.x+10, kr.y + kr.height - 70))

            if key in self.owned:
                # Auswählen-Button
                pygame.draw.rect(self.screen, (50,200,50), tile["select_rect"])
                sel_txt = font_button.render("Auswählen", True, (0,0,0))
                self.screen.blit(sel_txt, (tile["select_rect"].x+5, tile["select_rect"].y+10))
                # Rahmen um aktiven Skin
                if key == self.current:
                    pygame.draw.rect(self.screen, (0,255,0), kr, 3)
            else:
                # Kaufen-Button
                pygame.draw.rect(self.screen, (200,200,0), tile["buy_rect"])
                buy_txt = font_button.render("Kaufen", True, (0,0,0))
                self.screen.blit(buy_txt, (tile["buy_rect"].x+5, tile["buy_rect"].y+10))
                price_txt = font_button.render(f"{cost}c", True, (255,215,0))
                self.screen.blit(price_txt, (tile["buy_rect"].x+90, tile["buy_rect"].y+10))

        # Zurück-Button
        pygame.draw.rect(self.screen, (150,50,50), self.btn_back)
        back_txt = font_button.render("Zurück", True, (255,255,255))
        self.screen.blit(back_txt, (self.btn_back.x+5, self.btn_back.y+5))

        pygame.display.flip()
