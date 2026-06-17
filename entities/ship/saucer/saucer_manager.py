import random

import pygame

from .saucer import Saucer


class SaucerManager:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.width = screen_width
        self.height = screen_height

        self.saucer: Saucer | None = None

    def _difficulty_level(self, score: int) -> int:
        if score < 5000:
            return 0

        if score < 10000:
            return 1

        if score < 20000:
            return 2

        return 3

    def _small_saucer_probability(self, score: int) -> float:
        level = self._difficulty_level(score)

        match level:
            case 0:
                return 0.2

            case 1:
                return 0.5

            case 2:
                return 0.75

            case _:
                return 0.9

    def spawn_interval(self, score: int) -> int:
        level = self._difficulty_level(score)

        match level:
            case 0:
                return 900

            case 1:
                return 700

            case 2:
                return 500

            case _:
                return 350

    def _aim_error(self, score: int) -> float:
        level = self._difficulty_level(score)

        match level:
            case 0:
                return 50

            case 1:
                return 30

            case 2:
                return 15

            case _:
                return 5

    def spawn(self, score: int) -> None:
        chance_small = self._small_saucer_probability(score)

        size_type = "small" if random.random() < chance_small else "large"

        aim_error = self._aim_error(score)

        self.saucer = Saucer(
            screen_width=self.width,
            screen_height=self.height,
            size_type=size_type,
            aim_error=aim_error,
        )

    def update(self, player_x: float, player_y: float) -> None:
        if self.saucer:
            self.saucer.move(player_x, player_y)

        if self.saucer and self.saucer.can_be_removed:
            self.saucer = None

    def draw(self, surface: pygame.Surface) -> None:
        if self.saucer:
            self.saucer.draw(surface)
