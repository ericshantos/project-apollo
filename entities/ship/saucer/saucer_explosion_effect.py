import random

import numpy as np
import pygame

from .typed import Particle


class SaucerExplosionEffect:
    def __init__(self) -> None:
        self.particles: list[Particle] = []
        self.is_active = False

    def trigger(
        self,
        x: float,
        y: float,
    ) -> None:
        self.particles.clear()
        self.is_active = True

        for _ in range(random.randint(15, 25)):
            angle = random.uniform(
                0,
                2 * np.pi,
            )

            speed = random.uniform(
                1.0,
                4.0,
            )

            self.particles.append(
                {
                    "x": x,
                    "y": y,
                    "vx": float(np.cos(angle) * speed),
                    "vy": float(np.sin(angle) * speed),
                    "lifetime": random.randint(
                        30,
                        50,
                    ),
                    "alpha": 255,
                }
            )

    def update(self) -> None:
        for particle in list(self.particles):
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]

            particle["lifetime"] -= 1

            particle["alpha"] = max(0, int(particle["lifetime"] / 50 * 255))

            if particle["lifetime"] <= 0:
                self.particles.remove(particle)

        self.is_active = len(self.particles) > 0

    def draw(
        self,
        surface: pygame.Surface,
    ) -> None:
        for particle in self.particles:
            p_surface = pygame.Surface(
                (4, 4),
                pygame.SRCALPHA,
            )

            pygame.draw.circle(
                p_surface,
                (
                    255,
                    255,
                    255,
                    particle["alpha"],
                ),
                (2, 2),
                2,
            )

            surface.blit(
                p_surface,
                (
                    int(particle["x"]),
                    int(particle["y"]),
                ),
            )

    def reset(self) -> None:
        self.particles.clear()
        self.is_active = False
