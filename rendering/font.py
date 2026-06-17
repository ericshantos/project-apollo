from pathlib import Path

import pygame


class FontManager:
    FONT_PATH: Path = Path("assets/fonts/Hyperspace.otf")

    _cache = {}

    @classmethod
    def to_write(cls, size: int):
        if size not in cls._cache:
            cls._cache[size] = pygame.font.Font(cls.FONT_PATH, size)

        return cls._cache[size]
