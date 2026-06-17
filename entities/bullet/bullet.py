import numpy as np
import pygame


class Bullet:
    RADIUS: int = 3
    MAX_LIFETIME: int = 60

    def __init__(self, x: float, y: float, angle: float) -> None:
        self.x: float = x
        self.y: float = y

        self.speed: float = 10.0

        radians: float = float(np.radians(angle))
        self.velocity_x: float = float(np.sin(radians) * self.speed)
        self.velocity_y: float = float(np.cos(radians) * self.speed)

        self.lifetime: int = 0
        self.max_lifetime: int = 60

    def update(self, width: int, height: int) -> None:
        self.x += self.velocity_x
        self.y -= self.velocity_y

        self.lifetime += 1

        self.wrap_around(width, height)

    def is_alive(self) -> bool:
        return self.lifetime < self.MAX_LIFETIME

    def wrap_around(self, width: int, height: int) -> None:
        if self.x < -self.RADIUS:
            self.x = width + self.RADIUS
        elif self.x > width + self.RADIUS:
            self.x = -self.RADIUS

        if self.y < -self.RADIUS:
            self.y = height + self.RADIUS
        elif self.y > height + self.RADIUS:
            self.y = -self.RADIUS

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen, (255, 255, 255), (int(self.x), int(self.y)), self.RADIUS
        )
