import random

import numpy as np

from configs import cfg
from env.action_space import ActionMap

from .typed import ShipFragments


class Player:
    MAX_SPEED: float = 10.0
    ROTATION_SPEED: float = 4.0
    ACCELERATION: float = 0.15
    FRICTION: float = 0.99

    RADIUS: int = 8

    RESPAWN_DELAY: int = 90

    def __init__(self, x: float, y: float) -> None:
        self.start_x: float = x
        self.start_y: float = y

        self.x: float = x
        self.y: float = y

        self.angle: float = 0
        self.velocity_x: float = 0
        self.velocity_y: float = 0

        self.is_accelerating: bool = False

        self.is_alive: bool = True
        self.lives: int = cfg.game.max_lives
        self.fragments: list[ShipFragments] = []

        self.respawn_timer: int = 0
        self.respawn_delay: int = 90

    def update(self, action: ActionMap, width: int, height: int) -> None:
        if not self.is_alive:
            self._update_explosion()

            if self.lives > 0:
                self.respawn_timer += 1
                if self.respawn_timer >= self.respawn_delay:
                    self.respawn()
            return

        if action.rotate_left:
            self.angle -= self.ROTATION_SPEED

        if action.rotate_right:
            self.angle += self.ROTATION_SPEED

        elif action.thrust:
            self.is_accelerating = True
            radians = float(np.radians(self.angle))
            self.velocity_x += float(np.sin(radians)) * self.ACCELERATION
            self.velocity_y += float(np.cos(radians)) * self.ACCELERATION

            speed = float(np.hypot(self.velocity_x, self.velocity_y))

            if speed > self.MAX_SPEED:
                scale = self.MAX_SPEED / speed

                self.velocity_x *= scale
                self.velocity_y *= scale
        else:
            self.is_accelerating = False

        self.x += self.velocity_x
        self.y -= self.velocity_y

        self.velocity_x *= self.FRICTION
        self.velocity_y *= self.FRICTION

        self.wrap_around(width, height)

    def trigger_explosion(self) -> None:
        self.is_alive = False
        self.lives -= 1
        self.respawn_timer = 0
        self.is_accelerating = False

        ship_lines = [
            ((0, -12), (7, 10)),
            ((7, 10), (0, 5)),
            ((0, 5), (-7, 10)),
            ((-7, 10), (0, -12)),
        ]

        radians = float(np.radians(self.angle))
        cos_a = float(np.cos(radians))
        sin_a = float(np.sin(radians))

        for p1, p2 in ship_lines:
            x1 = self.x + (p1[0] * cos_a + p1[1] * sin_a)
            y1 = self.y - (p1[0] * -sin_a + p1[1] * cos_a)
            x2 = self.x + (p2[0] * cos_a + p2[1] * sin_a)
            y2 = self.y - (p2[0] * -sin_a + p2[1] * cos_a)

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            dx = center_x - self.x
            dy = center_y - self.y
            dist = float(np.hypot(dx, dy)) + 0.1

            self.fragments.append(
                {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "vel_x": (dx / dist) * random.uniform(0.3, 0.8)
                    + (self.velocity_x * 0.2),
                    "vel_y": (dy / dist) * random.uniform(0.3, 0.8)
                    + (self.velocity_y * 0.2),
                    "alpha": 255,
                }
            )

    def respawn(self) -> None:
        self.x = self.start_x
        self.y = self.start_y
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.fragments.clear()
        self.is_alive = True

    def _update_explosion(self) -> None:
        for frag in self.fragments:
            frag["x1"] += frag["vel_x"]
            frag["y1"] += frag["vel_y"]
            frag["x2"] += frag["vel_x"]
            frag["y2"] += frag["vel_y"]
            frag["alpha"] = max(0, frag["alpha"] - 4)

    def wrap_around(self, width: int, height: int) -> None:
        if self.x < -self.RADIUS:
            self.x = width + self.RADIUS
        elif self.x > width + self.RADIUS:
            self.x = -self.RADIUS
        if self.y < -self.RADIUS:
            self.y = height + self.RADIUS
        elif self.y > height + self.RADIUS:
            self.y = -self.RADIUS
