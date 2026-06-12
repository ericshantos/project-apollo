from __future__ import annotations

import random
from typing import Literal, cast

import numpy as np
import pygame

from configs import cfg

from .saucer import Saucer
from .typed import AsteroidParticle


class Asteroid:
    LARGE_SPEED: float = 1.5
    MEDIUM_SPEED: float = 2.8
    SMALL_SPEED: float = 4.2

    MAX_RADIUS: float = 70.0

    MAX_SPEED: float = SMALL_SPEED

    ASTEROID_POINTS: dict[int, int] = {1: 3, 2: 2, 3: 1}

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        size: Literal[1, 2, 3] = 3,
        x: float | None = None,
        y: float | None = None,
    ) -> None:
        self.size = size
        self.radius: float

        if self.size == 3:
            self.radius = 70
        elif self.size == 2:
            self.radius = 25
        else:
            self.radius = 8

        self.is_alive: bool = True
        self.particles: list[AsteroidParticle] = []

        self.velocity_x: float
        self.velocity_y: float

        if x is None or y is None:
            self.x, self.y = self._generate_edge_position(screen_width, screen_height)
            self.velocity_x, self.velocity_y = self._generate_inward_velocity(
                screen_width, screen_height
            )
        else:
            self.x = x
            self.y = y
            angle = random.uniform(0, np.pi * 2)

            speed_multiplier = {
                3: self.LARGE_SPEED,
                2: self.MEDIUM_SPEED,
                1: self.SMALL_SPEED,
            }[self.size]

            self.velocity_x = np.cos(angle) * speed_multiplier
            self.velocity_y = np.sin(angle) * speed_multiplier

        base_points = [
            (0.0, -1.0),
            (0.5, -0.8),
            (1.0, -0.3),
            (0.8, 0.2),
            (1.0, 0.6),
            (0.4, 1.0),
            (-0.2, 0.8),
            (-0.6, 1.0),
            (-1.0, 0.4),
            (-0.8, -0.3),
            (-1.0, -0.7),
            (-0.4, -0.8),
        ]

        self.points: list[tuple[float, float]] = []
        for px, py in base_points:
            jitter_x = random.uniform(-0.12, 0.12)
            jitter_y = random.uniform(-0.12, 0.12)
            self.points.append(
                ((px + jitter_x) * self.radius, (py + jitter_y) * self.radius)
            )

        self.saucer: Saucer | None = None
        self.last_saucer_spawn = pygame.time.get_ticks()
        self.saucer_spawn_interval = 15000

    def _generate_edge_position(self, width: int, height: int) -> tuple[float, float]:
        edge = random.choice(["LEFT", "RIGHT", "TOP", "BOTTOM"])
        if edge == "LEFT":
            return -self.radius, random.uniform(0, height)
        elif edge == "RIGHT":
            return width + self.radius, random.uniform(0, height)
        elif edge == "TOP":
            return random.uniform(0, width), -self.radius
        else:
            return random.uniform(0, width), height + self.radius

    def _generate_inward_velocity(self, width: int, height: int) -> tuple[float, float]:
        target_x = random.uniform(width * 0.2, width * 0.8)
        target_y = random.uniform(height * 0.2, height * 0.8)
        dx, dy = target_x - self.x, target_y - self.y
        distance: float = float(np.hypot(dx, dy))

        base_speed = random.uniform(1.0, self.MAX_SPEED)
        return (dx / distance) * base_speed, (dy / distance) * base_speed

    def trigger_explosion(self) -> None:
        self.is_alive = False
        for _ in range(random.randint(8, 15)):
            angle = random.uniform(0, np.pi * 2)
            speed = random.uniform(1.0, 3.5)
            self.particles.append(
                {
                    "x": self.x,
                    "y": self.y,
                    "vel_x": np.cos(angle) * speed,
                    "vel_y": np.sin(angle) * speed,
                    "alpha": 255,
                }
            )

    def update(self, width: int, height: int) -> None:
        if not self.is_alive:
            for p in self.particles:
                p["x"] += p["vel_x"]
                p["y"] += p["vel_y"]
                p["alpha"] = max(0, p["alpha"] - 6)
            return

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.wrap_around(width, height)

    def wrap_around(self, width: int, height: int) -> None:
        if self.x < -self.radius:
            self.x = width + self.radius
        elif self.x > width + self.radius:
            self.x = -self.radius
        if self.y < -self.radius:
            self.y = height + self.radius
        elif self.y > height + self.radius:
            self.y = -self.radius

    def split(self) -> list[Asteroid]:
        if self.size == 1:
            return []

        return [
            Asteroid(
                screen_width=cfg.screen.width,
                screen_height=cfg.screen.height,
                size=cast(Literal[1, 2, 3], self.size - 1),
                x=self.x,
                y=self.y,
            )
            for _ in range(2)
        ]
