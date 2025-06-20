# config.py

# Fenstergröße
SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 800

# Verfügbare Skins: (key, Anzeige‑Name, Preis)
SKINS = [
    ("default",   "Lama",            0),
    ("cat",       "Katze",         20),
    ("demon",     "Demon",         30),
    ("stickman",  "Strichmännchen", 40),  # neu hinzugefügt
]
# Füge hinter den vorhandenen PowerUps "plasma" hinzu
POWERUP_TYPES = [
    ("fly",      "Fliegen",    10),
    ("shield",   "Schild",     10),
    ("life",     "Extra Leben",10),
    ("highjump", "HighJump",   10),
    ("plasma",   "Plasma",     15),  # neu
]
