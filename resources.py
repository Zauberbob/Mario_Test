# resources.py
import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Liefert den absoluten Pfad zu einer Ressource,
    sowohl im Entwicklungs‑Modus als auch in einer PyInstaller‑EXE.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, relative_path)
