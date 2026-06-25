import numpy as np

from entities import Asteroid, Player, Saucer

from .game_world import GameWorld
from .toroidal_space import ToroidalSpace


class Observation:
    MAX_ASTEROIDS: int = 5

    PLAYER_FEATURES: int = 6
    TARGET_FEATURES: int = 7

    SIZE: int = PLAYER_FEATURES + TARGET_FEATURES + (MAX_ASTEROIDS * TARGET_FEATURES)
    
    def __init__(self, space: ToroidalSpace) -> None:

        self.space = space

    def _encode_target(
        self,
        player: Player,
        target_x: float,
        target_y: float,
        target_vx: float,
        target_vy: float,
        radius: float,
        max_radius: float,
        rad_angle: float,
        max_rel_speed: float,
    ) -> list[float]:
        dx = target_x - player.x
        dy = target_y - player.y

        dx = self.space.delta_x(dx)
        dy = self.space.delta_y(dy)

        target_angle = float(np.arctan2(dy, dx))

        rel_angle = (target_angle - rad_angle + np.pi) % (2 * np.pi) - np.pi

        distance = np.hypot(dx, dy) / np.hypot(self.space.width, self.space.height)
        distance = float(np.clip(distance, 0.0, 1.0))

        vx_rel = (target_vx - player.velocity_x) / max_rel_speed
        vy_rel = (target_vy - player.velocity_y) / max_rel_speed

        vx_rel = float(np.clip(vx_rel, -1.0, 1.0))
        vy_rel = float(np.clip(vy_rel, -1.0, 1.0))

        size_norm = float(radius / max_radius)

        return [
            distance,
            float(np.sin(rel_angle)),
            float(np.cos(rel_angle)),
            vx_rel,
            vy_rel,
            size_norm,
            1.0,
        ]

    def build(self, world: GameWorld) -> np.ndarray:
        player: Player = world.player

        max_rel_speed = (
            Player.MAX_SPEED
            + Asteroid.MAX_SPEED
            + (Saucer.MAX_SPEED if hasattr(Saucer, "MAX_SPEED") else 0)
        )

        px_norm = float(np.clip(player.x / self.space.width, 0.0, 1.0))
        py_norm = float(np.clip(player.y / self.space.height, 0.0, 1.0))

        vx_norm = float(
            np.clip(
                player.velocity_x / Player.MAX_SPEED,
                -1.0,
                1.0,
            )
        )

        vy_norm = float(
            np.clip(
                player.velocity_y / Player.MAX_SPEED,
                -1.0,
                1.0,
            )
        )

        rad_angle = float(np.radians(player.angle))

        obs: list[float] = [
            px_norm,
            py_norm,
            vx_norm,
            vy_norm,
            float(np.cos(rad_angle)),
            float(np.sin(rad_angle)),
        ]

        saucer: Saucer | None = world.saucer

        if saucer is not None:
            obs.extend(
                self._encode_target(
                    player=player,
                    target_x=saucer.x,
                    target_y=saucer.y,
                    target_vx=saucer.speed_x,
                    target_vy=saucer.speed_y,
                    radius=saucer.radius,
                    max_radius=saucer.radius,
                    rad_angle=rad_angle,
                    max_rel_speed=max_rel_speed,
                )
            )
        else:
            obs.extend([0.0] * self.TARGET_FEATURES)

        asteroids = sorted(
            world.asteroids,
            key=lambda a: ((a.x - player.x) ** 2 + (a.y - player.y) ** 2),
        )

        visible_asteroids = asteroids[: self.MAX_ASTEROIDS]

        for asteroid in visible_asteroids:
            obs.extend(
                self._encode_target(
                    player=player,
                    target_x=asteroid.x,
                    target_y=asteroid.y,
                    target_vx=asteroid.velocity_x,
                    target_vy=asteroid.velocity_y,
                    radius=asteroid.radius,
                    max_radius=Asteroid.MAX_RADIUS,
                    rad_angle=rad_angle,
                    max_rel_speed=max_rel_speed,
                )
            )

        missing = self.MAX_ASTEROIDS - len(visible_asteroids)

        for _ in range(missing):
            obs.extend([0.0] * self.TARGET_FEATURES)

        return np.asarray(obs, dtype=np.float32)
