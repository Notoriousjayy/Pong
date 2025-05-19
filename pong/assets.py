# pong/assets.py

import pygame
from pathlib import Path

def load_sfx():
    pygame.mixer.init()
    sfx = {}

    project_root = Path(__file__).resolve().parent.parent
    sounds_dir   = project_root / "sounds"

    # Multi‐variant
    sfx["hit"]    = [pygame.mixer.Sound(str(sounds_dir / f"hit{i}.ogg"))    for i in range(5)]
    sfx["bounce"] = [pygame.mixer.Sound(str(sounds_dir / f"bounce{i}.ogg")) for i in range(5)]

    # Single‐variant (try both name0.ogg and name.ogg)
    for name in (
        "hit_slow","hit_medium","hit_fast","hit_veryfast",
        "bounce_synth","score_goal","up","down"
    ):
        # preferred: name0.ogg
        p0 = sounds_dir / f"{name}0.ogg"
        # fallback: name.ogg
        p1 = sounds_dir / f"{name}.ogg"

        if p0.exists():
            path = p0
        elif p1.exists():
            path = p1
        else:
            raise FileNotFoundError(f"Could not find sound file for '{name}' (tried '{p0.name}' and '{p1.name}')")

        sfx[name] = [pygame.mixer.Sound(str(path))]

    return sfx
