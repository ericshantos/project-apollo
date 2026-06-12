import random

import numpy as np

from configs import cfg
from entities import Asteroid, Bullet, BulletManager, Player

from .action_space import ActionMap


class GameWorld:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height

        self.score: int = 0
        self.frame_count: int = 0
        self.done: bool = False

        self.player: Player
        self.asteroids: list[Asteroid] = []

        self.bullet_manager: BulletManager = BulletManager()

        self.initial_asteroids: int = cfg.game.max_asteroids
        self.wave: int = 1

        self.asteroids_destroyed: int = 0
        self.shots_fired: int = 0
        self.accuracy_hits: int = 0

        self.reset()

    def reset(self) -> None:
        self.score = 0
        self.asteroids_destroyed = 0
        self.shots_fired = 0
        self.accuracy_hits = 0

        self.frame_count = 0

        self.wave = 1

        self.done = False

        self.player = Player(self.width // 2, self.height // 2)

        self.asteroids = []

        self.bullet_manager = BulletManager()

        self._spawn_asteroids(self.initial_asteroids)

    def _next_wave(self) -> None:
        self.wave += 1

        num_asteroids = self.initial_asteroids + self.wave - 1

        self._spawn_asteroids(num_asteroids)

    def _spawn_asteroids(self, quantity: int, min_distance: int = 200) -> None:
        self.asteroids.clear()

        while len(self.asteroids) < quantity:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            dx = x - self.player.x
            dy = y - self.player.y

            distance: float = float(np.hypot(dx, dy))

            if distance < min_distance:
                continue

            self.asteroids.append(
                Asteroid(screen_width=self.width, screen_height=self.height, x=x, y=y)
            )

    def _check_player_asteroid_collisions(self) -> None:
        if not self.player.is_alive:
            return

        for asteroid in self.asteroids:
            dx = asteroid.x - self.player.x
            dy = asteroid.y - self.player.y

            distance = float(np.hypot(dx, dy))

            collision_distance = asteroid.radius + self.player.RADIUS

            if distance <= collision_distance:
                self.player.trigger_explosion()

                break

    def _check_bullet_asteroid_collisions(self) -> None:
        bullets_to_remove = []
        asteroids_to_remove = []

        new_asteroids = []

        for bullet in self.bullets:
            for asteroid in self.asteroids:
                dx = asteroid.x - bullet.x
                dy = asteroid.y - bullet.y

                distance = float(np.hypot(dx, dy))

                collision_distance = asteroid.radius + bullet.RADIUS

                if distance <= collision_distance:
                    bullets_to_remove.append(bullet)
                    asteroids_to_remove.append(asteroid)

                    self.score += Asteroid.ASTEROID_POINTS[asteroid.size]

                    self.asteroids_destroyed += 1
                    self.accuracy_hits += 1

                    break

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullet_manager.remove_bullet(bullet)

        for asteroid in asteroids_to_remove:
            if asteroid not in self.asteroids:
                continue

            self.asteroids.remove(asteroid)

            new_asteroids.extend(asteroid.split())

        if new_asteroids:
            self.asteroids.extend(new_asteroids)

        if len(self.asteroids) == 0:
            self._next_wave()

    def update(self, action: ActionMap) -> None:
        if self.done:
            return

        self.frame_count += 1

        self.player.update(action, self.width, self.height)

        if action.shoot:
            self.shoot()

        for asteroid in self.asteroids:
            asteroid.update(self.width, self.height)

        self.bullet_manager.update(self.width, self.height)

        self._check_bullet_asteroid_collisions()

        self._check_player_asteroid_collisions()

        if self.is_game_over():
            self.done = True

    def shoot(self) -> None:
        if not self.player.is_alive:
            return

        self.shots_fired += 1

        self.bullet_manager.shoot(self.player.x, self.player.y, self.player.angle)

    def update_bullets(self) -> None:
        pass

    def update_asteroids(self) -> None:
        pass

    def _handle_asteroids(self) -> None: ...

    def render(self) -> None: ...

    @property
    def player_alive(self) -> bool:
        return self.player.is_alive

    @property
    def player_lives(self) -> int:
        return self.player.lives

    def get_score(self) -> int:
        return self.score

    def get_player(self) -> Player:
        return self.player

    def is_done(self) -> bool:
        return self.done

    def is_game_over(self) -> bool:
        return self.player.lives <= 0

    @property
    def bullets(self) -> list[Bullet]:
        return self.bullet_manager.bullets

    @property
    def accuracy(self) -> float:
        if self.shots_fired == 0:
            return 0.0

        return self.accuracy_hits / self.shots_fired
