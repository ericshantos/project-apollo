import random
from typing import Literal

import numpy as np
import pygame

from ..destroyed import Destroyable
from ..ship import Shooter
from .saucer_explosion_effect import SaucerExplosionEffect


class Saucer(Shooter, Destroyable):
    MAX_BULLETS: int = 1

    _SAUCER_POINT: dict[str, int] = {
        "large": 200,
        "small": 1000,
    }

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        size_type: Literal["large", "small"] = "large",
        aim_error: float = 45.0,
    ) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size_type = size_type

        self.aim_error = aim_error

        self.scale: float = 2.0 if size_type == "large" else 1.0

        self.color: tuple[int, int, int] = (255, 255, 255)

        self.raw_points: list[tuple[float, float]] = [
            (-9, 0),
            (-3, -3),
            (-2, -6),
            (2, -6),
            (3, -3),
            (9, 0),
            (3, 4),
            (-3, 4),
            (-9, 0),
            (9, 0),
            (3, -3),
            (-3, -3),
            (-9, 0),
        ]
        self.shape_points: list[tuple[float, float]] = [
            (x * self.scale, y * self.scale) for x, y in self.raw_points
        ]

        self.direction: Literal[-1, 1] = random.choice([-1, 1])
        self.x: float = -20.0 if self.direction == 1 else float(screen_width + 20)
        self.y: float = float(random.randint(50, screen_height - 50))

        if self.size_type == "large":
            self.speed_x = 2.0 * self.direction
        else:
            self.speed_x = 3.5 * self.direction

        self.speed_y: float = random.choice([-2.0, 2.0])

        self.last_dir_change: int = pygame.time.get_ticks()
        self.dir_change_interval: int = random.randint(2000, 4000)
        self.is_alive: bool = True

        self.explosion: SaucerExplosionEffect = SaucerExplosionEffect()

        self.is_exploding: bool = False

        super().__init__()

    def move(
        self, player_x: float | None = None, player_y: float | None = None
    ) -> None:
        if not self.is_alive and not self.is_exploding and self.bullet_manager.is_empty:
            return

        if self.is_alive:
            self.x += self.speed_x
            now = pygame.time.get_ticks()

            if now - self.last_dir_change > self.dir_change_interval:
                self.speed_y = random.choice([-2.0, 2.0])

                self.last_dir_change = now
                self.dir_change_interval = random.randint(2000, 4000)

            self.y += self.speed_y

            if self.y < 60:
                self.y = 60
                self.speed_y = 1.5
            elif self.y > self.screen_height - 60:
                self.y = self.screen_height - 60
                self.speed_y = -1.5

            if (self.direction == 1 and self.x > self.screen_width + 30) or (
                self.direction == -1 and self.x < -30
            ):
                self.is_alive = False

            if self.is_alive and self.can_shoot():
                self.shoot(player_x, player_y)

        if self.is_exploding:
            self.explosion.update()

            if not self.explosion.is_active:
                self.is_exploding = False

        self.bullet_manager.update(self.screen_width, self.screen_height)

    def die(self) -> None:
        if not self.is_alive:
            return

        self.is_alive = False
        self.is_exploding = True

        self.explosion.trigger(self.x, self.y)

    def shoot(self, player_x: int | None, player_y: int | None) -> None:
        if not self.is_alive:
            return

        if player_x is None or player_y is None:
            return

        if self.bullet_manager.count >= self.MAX_BULLETS:
            return

        if self.size_type == "large":
            angle = random.uniform(0, 360)

        else:
            dx = player_x - self.x
            dy = player_y - self.y

            angle = float(np.degrees(np.arctan2(dx, dy)))

            angle += random.gauss(0, self.aim_error)

        self.bullet_manager.shoot(self.x, self.y, angle)

    def draw(self, surface: pygame.Surface) -> None:
        self.bullet_manager.draw(surface)

        if self.is_exploding:
            self.explosion.draw(surface)

        if not self.is_alive:
            return

        transformed_points = [
            (px + self.x, py + self.y) for px, py in self.shape_points
        ]
        pygame.draw.aalines(surface, self.color, True, transformed_points)

    @property
    def radius(self) -> float:
        return 12 * self.scale

    @classmethod
    def points(cls, size_type: str) -> int:
        return cls._SAUCER_POINT.get(size_type, 0)

    @property
    def can_be_removed(self) -> bool:
        return (
            not self.is_alive and not self.is_exploding and self.bullet_manager.is_empty
        )
