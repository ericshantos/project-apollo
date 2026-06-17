import numpy as np

from entities import Asteroid, AsteroidManager, Bullet, Player, Saucer

from .score_manager import ScoreManager


class CollisionManager:
    def __init__(
        self,
        player: Player,
        asteroid_manager: AsteroidManager,
        score_manager: ScoreManager,
    ) -> None:
        self.player = player
        self.asteroid_manager = asteroid_manager
        self.score_manager = score_manager

        self.reset()

    def reset(self) -> None:
        self.asteroids_destroyed = 0
        self.accuracy_hits = 0

    def check_saucer_player_collision(self, saucer: Saucer) -> None:
        if not self.player.is_alive:
            return

        if not saucer.is_alive:
            return

        dx = saucer.x - self.player.x
        dy = saucer.y - self.player.y

        distance = float(np.hypot(dx, dy))

        collision_distance = saucer.radius + self.player.RADIUS

        if distance <= collision_distance:
            self.player.die()

    def check_saucer_bullets_player_collision(self, saucer: Saucer) -> None:
        if not self.player.is_alive:
            return

        for bullet in saucer.bullet_manager.bullets:
            dx = self.player.x - bullet.x
            dy = self.player.y - bullet.y

            distance = float(np.hypot(dx, dy))

            collision_distance = bullet.RADIUS + self.player.RADIUS

            if distance <= collision_distance:
                self.player.die()

                saucer.bullet_manager.remove(bullet)

                return

    def check_bullet_saucer_collision(self, saucer: Saucer) -> None:
        if not saucer.is_alive:
            return

        for bullet in list(self.player.bullet_manager.bullets):
            dx = saucer.x - bullet.x
            dy = saucer.y - bullet.y

            distance = float(np.hypot(dx, dy))

            collision_distance = saucer.radius + bullet.RADIUS

            if distance <= collision_distance:
                self.player.bullet_manager.remove(bullet)

                saucer.die()

                self.score_manager.add(Saucer.points(saucer.size_type))

                self.accuracy_hits += 1

                return

    def check_saucer_asteroid_collision(self, saucer: Saucer) -> None:
        if not saucer.is_alive:
            return

        for asteroid in self.asteroid_manager.asteroids:
            dx = asteroid.x - saucer.x
            dy = asteroid.y - saucer.y

            distance = float(np.hypot(dx, dy))

            collision_distance = asteroid.radius + saucer.radius

            if distance <= collision_distance:
                saucer.die()

                return

    def check_player_asteroid_collisions(self) -> None:
        if not self.player.is_alive:
            return

        for asteroid in self.asteroid_manager.asteroids:
            dx = asteroid.x - self.player.x
            dy = asteroid.y - self.player.y

            distance = float(np.hypot(dx, dy))

            collision_distance = asteroid.radius + self.player.RADIUS

            if distance <= collision_distance:
                self.player.die()

                return

    def check_bullet_asteroid_collisions(self) -> None:
        bullets_to_remove: set[Bullet] = set()
        asteroids_to_remove: set[Asteroid] = set()

        for bullet in self.player.bullet_manager.bullets:
            if bullet in bullets_to_remove:
                continue

            for asteroid in self.asteroid_manager.asteroids:
                if asteroid in asteroids_to_remove:
                    continue

                dx = asteroid.x - bullet.x
                dy = asteroid.y - bullet.y

                distance = float(np.hypot(dx, dy))

                collision_distance = asteroid.radius + bullet.RADIUS

                if distance <= collision_distance:
                    bullets_to_remove.add(bullet)

                    asteroids_to_remove.add(asteroid)

                    self.score_manager.add(Asteroid.points(asteroid.size))

                    self.asteroids_destroyed += 1
                    self.accuracy_hits += 1

                    break

        for bullet in bullets_to_remove:
            self.player.bullet_manager.remove(bullet)

        for asteroid in asteroids_to_remove:
            self.asteroid_manager.remove(asteroid)

    def update(self, saucer: Saucer | None) -> None:
        self.check_bullet_asteroid_collisions()

        self.check_player_asteroid_collisions()

        if saucer is None:
            return

        self.check_bullet_saucer_collision(saucer)

        self.check_saucer_player_collision(saucer)

        self.check_saucer_bullets_player_collision(saucer)

        self.check_saucer_asteroid_collision(saucer)
