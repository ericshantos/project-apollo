import random

import numpy as np
import pygame

from configs import cfg
from env.action_space import ActionMap

from ..destroyed import Destroyable
from ..ship import Shooter
from .hyperspace_manager import HyperspaceManager
from .ship_explosion_effect import ShipExplosionEffect


class Player(Shooter, Destroyable):
    MAX_SPEED: float = 10.0
    ROTATION_SPEED: float = 4.0
    ACCELERATION: float = 0.15
    FRICTION: float = 0.99

    RADIUS: int = 8

    MAX_LIVES: int = cfg.game.max_lives

    RESPAWN_DELAY: int = 90

    def __init__(self, x: float, y: float) -> None:
        super().__init__()

        self.start_x: float = x
        self.start_y: float = y

        self.x: float = x
        self.y: float = y

        self.angle: float = 0
        self.velocity_x: float = 0
        self.velocity_y: float = 0

        self.is_accelerating: bool = False

        self.used_hyperspace_this_step: bool = False

        self.is_alive: bool = True
        self._lives: int = self.MAX_LIVES

        self.explosion: ShipExplosionEffect = ShipExplosionEffect()
        self.hyperspace_manager: HyperspaceManager = HyperspaceManager()

        self.respawn_timer: int = 0

    @property
    def lives(self) -> int:
        return self._lives

    @lives.setter
    def lives(self, value) -> None:
        self._lives = max(0, min(self.MAX_LIVES, value))

    def gain_life(self) -> None:
        self._lives = min(self.lives + 1, self.MAX_LIVES)

    def lose_life(self) -> None:
        self._lives = max(0, self._lives - 1)

    def use_hyperspace(self, width: int, height: int) -> None:
        if not self.is_alive:
            return

        if self.hyperspace_manager.should_explode():
            self.die()
            return

        self.x, self.y = self.hyperspace_manager.teleport(width, height)

        self.velocity_x = 0
        self.velocity_y = 0

        self.used_hyperspace_this_step = True

    def update(self, action: ActionMap, width: int, height: int) -> None:
        self.used_hyperspace_this_step = False

        if not self.is_alive:
            self.explosion.update()

            if self.lives > 0:
                self.respawn_timer += 1

            return

        if action.rotate_left:
            self.angle -= self.ROTATION_SPEED

        elif action.rotate_right:
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

        self.bullet_manager.update(width, height)

    def die(self) -> None:
        self.is_alive = False
        self.lose_life()

        self.is_accelerating = False

        self.explosion.trigger(
            self.x, self.y, self.angle, self.velocity_x, self.velocity_y
        )

        self.respawn_timer = 0

    def respawn(self) -> None:
        self.x = self.start_x
        self.y = self.start_y
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0

        self.hyperspace_manager.reset()

        self.explosion.reset()
        self.is_alive = True
        self.is_accelerating = False

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
        if not self.is_alive:
            self.explosion.draw(screen)
            return

        radians = float(np.radians(self.angle))

        tip_x = self.x + float(np.sin(radians)) * 12
        tip_y = self.y - float(np.cos(radians)) * 12
        right_x = self.x + float(np.sin(radians - 2.5)) * 10
        right_y = self.y - float(np.cos(radians - 2.5)) * 10
        inner_x = self.x - float(np.sin(radians)) * 4
        inner_y = self.y + float(np.cos(radians)) * 4
        left_x = self.x + float(np.sin(radians + 2.5)) * 10
        left_y = self.y - float(np.cos(radians + 2.5)) * 10

        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            [(tip_x, tip_y), (right_x, right_y), (inner_x, inner_y), (left_x, left_y)],
            2,
        )

        if self.is_accelerating:
            if random.choice([True, False]):
                fire_tip_x = self.x - float(np.sin(radians)) * 10
                fire_tip_y = self.y + float(np.cos(radians)) * 10
                fire_left_x = self.x + float(np.sin(radians + 2.8)) * 6
                fire_left_y = self.y - float(np.cos(radians + 2.8)) * 6
                fire_right_x = self.x + float(np.sin(radians - 2.8)) * 6
                fire_right_y = self.y - float(np.cos(radians - 2.8)) * 6

                pygame.draw.polygon(
                    screen,
                    (255, 255, 255),
                    [
                        (inner_x, inner_y),
                        (fire_left_x, fire_left_y),
                        (fire_tip_x, fire_tip_y),
                        (fire_right_x, fire_right_y),
                    ],
                    2,
                )

        self.bullet_manager.draw(screen)
