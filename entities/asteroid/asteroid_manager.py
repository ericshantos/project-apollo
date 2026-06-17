import random

import numpy as np
import pygame

from .asteroid import Asteroid


class AsteroidManager:
    MAX_ASTEROIDS: int = 26

    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.width = screen_width
        self.height = screen_height

        self.asteroids: list[Asteroid] = []

    def spawn_wave(
        self, quantity: int, player_x: float, player_y: float, min_distance: int = 400
    ) -> None:
        self.asteroids.clear()

        while len(self.asteroids) < quantity:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            dx = x - player_x
            dy = y - player_y

            distance: float = float(np.hypot(dx, dy))

            if distance < min_distance:
                continue

            self.asteroids.append(
                Asteroid(screen_width=self.width, screen_height=self.height, x=x, y=y)
            )

    def update(self) -> None:
        for asteroid in self.asteroids:
            asteroid.update(self.width, self.height)

    def draw(self, surface: pygame.Surface) -> None:
        for asteroid in self.asteroids:
            asteroid.draw(surface)

    def split(self, asteroid: Asteroid) -> list[Asteroid]:
        if asteroid.size == 1:
            return []

        available_slots = self.MAX_ASTEROIDS - len(self.asteroids)

        quantity = min(2, available_slots)

        return asteroid.create_children(quantity)

    def remove(self, asteroid: Asteroid) -> None:
        if asteroid not in self.asteroids:
            return

        self.asteroids.remove(asteroid)

        children = self.split(asteroid)

        self.asteroids.extend(children)

    @property
    def count(self) -> int:
        return len(self.asteroids)

    @property
    def is_empty(self) -> bool:
        return self.count == 0
