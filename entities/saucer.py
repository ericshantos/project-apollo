import random
from typing import Literal

import numpy as np
import pygame

from .bullet import Bullet
from .typed import SaucerParticle


class Saucer:
    COLOR: tuple[int, int, int] = (255, 255, 255)

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        size_type: Literal["large", "small"] = "large",
    ) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size_type = size_type

        self.scale: float = 2.0 if size_type == "large" else 1.0

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
        self.y: float = float(random.randint(120, screen_height - 120))

        self.speed_x: float = 2.5 * self.direction
        self.speed_y: float = 0.0

        self.last_dir_change: int = pygame.time.get_ticks()
        self.dir_change_interval: int = 1000
        self.is_alive: bool = True

        self.bullets: list[Bullet] = []
        self.last_shot_time: int = pygame.time.get_ticks()
        self.shoot_interval: int = 1200 if size_type == "small" else 2000

        self.particles: list[SaucerParticle] = []
        self.is_exploding: bool = False

    def trigger_explosion(self) -> None:
        self.is_alive = False
        self.is_exploding = True

        for _ in range(random.randint(15, 25)):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(1.0, 4.0)
            self.particles.append(
                {
                    "x": self.x,
                    "y": self.y,
                    "vx": float(np.cos(angle) * speed),
                    "vy": float(np.sin(angle) * speed),
                    "lifetime": random.randint(30, 50),
                    "alpha": 255,
                }
            )

    def move(
        self, player_x: float | None = None, player_y: float | None = None
    ) -> None:
        if not self.is_alive and not self.is_exploding and len(self.bullets) == 0:
            return

        if self.is_alive:
            self.x += self.speed_x
            now = pygame.time.get_ticks()

            if now - self.last_dir_change > self.dir_change_interval:
                self.speed_y = random.choice([-1.5, 0, 1.5])
                self.last_dir_change = now

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

            self._shoot_logic(now, player_x, player_y)

        if self.is_exploding:
            for p in list(self.particles):
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["lifetime"] -= 1
                p["alpha"] = max(0, int((p["lifetime"] / 50) * 255))

                if p["lifetime"] <= 0:
                    self.particles.remove(p)

            if len(self.particles) == 0:
                self.is_exploding = False

        for bullet in list(self.bullets):
            bullet.update(self.screen_width, self.screen_height)
            if bullet.lifetime >= bullet.max_lifetime:
                self.bullets.remove(bullet)

    def _shoot_logic(
        self, current_time: int, player_x: float | None, player_y: float | None
    ) -> None:
        if current_time - self.last_shot_time > self.shoot_interval:
            if player_x is not None and player_y is not None:
                if self.size_type == "large":
                    angle = random.uniform(0, 360)
                else:
                    dx = player_x - self.x
                    dy = self.y - player_y

                    angle = float(np.degrees(np.atan2(dx, dy)))

                    angle += random.uniform(-15, 15)

                new_bullet = Bullet(self.x, self.y, angle)
                new_bullet.speed = 7.0

                rad = float(np.radians(angle))
                new_bullet.velocity_x = float(np.sin(rad)) * new_bullet.speed
                new_bullet.velocity_y = float(np.cos(rad)) * new_bullet.speed

                self.bullets.append(new_bullet)
                self.last_shot_time = current_time

    def get_rect(self) -> pygame.Rect:
        width = 18 * self.scale
        height = 10 * self.scale

        return pygame.Rect(
            int(self.x - width / 2), int(self.y - height / 2), int(width), int(height)
        )
