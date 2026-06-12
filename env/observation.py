import numpy as np

from entities import Asteroid, Player

from .game_world import GameWorld


class Observation:
    MAX_ASTEROIDS: int = 5

    SIZE: int = 6 + (MAX_ASTEROIDS * 6)

    @staticmethod
    def build(world: GameWorld) -> np.ndarray:
        player: Player = world.get_player()

        max_rel_asteroid: float = Player.MAX_SPEED + Asteroid.MAX_SPEED

        px_norm: float = player.x / world.width
        py_norm: float = player.y / world.height

        vx_norm: float = float(np.clip(player.velocity_x / 10, -1.0, 1.0))
        vy_norm: float = float(np.clip(player.velocity_y / 10, -1.0, 1.0))

        rad_angle: float = float(np.radians(player.angle))
        cos_angle: float = float(np.cos(rad_angle))
        sin_angle: float = float(np.sin(rad_angle))

        obs: list[float] = [px_norm, py_norm, vx_norm, vy_norm, cos_angle, sin_angle]

        asteroids: list[Asteroid] = sorted(
            world.asteroids, key=lambda a: (a.x - player.x) ** 2 + (a.y - player.y) ** 2
        )

        visible_asteroids = asteroids[: Observation.MAX_ASTEROIDS]

        for asteroid in visible_asteroids:
            dx_rel = (asteroid.x - player.x) / world.width
            dy_rel = (asteroid.y - player.y) / world.height

            vx_rel = asteroid.velocity_x - player.velocity_x
            vy_rel = asteroid.velocity_y - player.velocity_y

            vx_rel = np.clip(vx_rel / max_rel_asteroid, -1.0, 1.0)
            vy_rel = np.clip(vy_rel / max_rel_asteroid, -1.0, 1.0)

            size_norm = asteroid.radius / Asteroid.MAX_RADIUS

            exists = 1.0

            obs.extend([dx_rel, dy_rel, vx_rel, vy_rel, size_norm, exists])

        missing: int = Observation.MAX_ASTEROIDS - len(visible_asteroids)

        for _ in range(missing):
            obs.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        return np.array(obs, dtype=np.float32)
