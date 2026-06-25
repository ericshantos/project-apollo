import numpy as np

from entities import Asteroid, Player, Saucer

from .danger_model import DangerModel
from .game_world import GameWorld
from .toroidal_space import ToroidalSpace


class Observation:
    MAX_ASTEROIDS: int = 5

    PLAYER_FEATURES: int = 4
    TARGET_FEATURES: int = 9

    SIZE: int = (
        PLAYER_FEATURES
        + TARGET_FEATURES
        + (MAX_ASTEROIDS * TARGET_FEATURES)
        + 3
    )

    def __init__(self, space: ToroidalSpace) -> None:
        self.space = space
        self.danger_model = DangerModel(
            space,
            self.MAX_ASTEROIDS,
        )

    def _encode_target(
        self,
        player: Player,
        tx: float,
        ty: float,
        tvx: float,
        tvy: float,
        radius: float,
        max_radius: float,
        rad_angle: float,
        max_rel_speed: float,
    ) -> list[float]:

        dx, dy = self.space.relative_vector(
            player.x,
            player.y,
            tx,
            ty,
        )

        distance = np.hypot(dx, dy)

        max_distance = np.hypot(
            self.space.width,
            self.space.height,
        )

        distance_norm = float(
            np.clip(
                distance / max_distance,
                0.0,
                1.0,
            )
        )

        dvx = tvx - player.velocity_x
        dvy = tvy - player.velocity_y

        closing_velocity = (
            (dx * dvx + dy * dvy)
            / (distance + 1e-6)
        )

        closing_velocity = float(
            np.clip(
                closing_velocity / max_rel_speed,
                -1.0,
                1.0,
            )
        )

        ttc = distance / (abs(closing_velocity * max_rel_speed) + 1e-6)

        # Normaliza TTC para [0, 1]
        ttc = float(
            np.clip(
                ttc / 300.0,
                0.0,
                1.0,
            )
        )

        angle_to_target = np.arctan2(dy, dx)

        rel_angle = (
            angle_to_target
            - rad_angle
            + np.pi
        ) % (2 * np.pi) - np.pi

        vx_rel = float(
            np.clip(
                dvx / max_rel_speed,
                -1.0,
                1.0,
            )
        )

        vy_rel = float(
            np.clip(
                dvy / max_rel_speed,
                -1.0,
                1.0,
            )
        )

        size_norm = float(
            np.clip(
                radius / max_radius,
                0.0,
                1.0,
            )
        )

        danger = float(
            np.tanh(
                np.exp(-distance_norm)
                * max(
                    0.0,
                    -closing_velocity,
                )
            )
        )

        return [
            distance_norm,
            float(np.sin(rel_angle)),
            float(np.cos(rel_angle)),
            vx_rel,
            vy_rel,
            size_norm,
            closing_velocity,
            ttc,
            danger,
        ]

    def build(
        self,
        world: GameWorld,
    ) -> np.ndarray:

        player = world.player

        max_rel_speed = (
            Player.MAX_SPEED
            + Asteroid.MAX_SPEED
            + (
                Saucer.MAX_SPEED
                if hasattr(Saucer, "MAX_SPEED")
                else 0
            )
        )

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

        rad_angle = float(
            np.radians(player.angle)
        )

        obs: list[float] = [
            vx_norm,
            vy_norm,
            float(np.cos(rad_angle)),
            float(np.sin(rad_angle)),
        ]

        saucer = world.saucer

        if saucer is not None:
            obs.extend(
                self._encode_target(
                    player,
                    saucer.x,
                    saucer.y,
                    saucer.velocity_x,
                    saucer.velocity_y,
                    saucer.radius,
                    saucer.radius,
                    rad_angle,
                    max_rel_speed,
                )
            )
        else:
            obs.extend(
                [0.0] * self.TARGET_FEATURES
            )

        analysis = self.danger_model.analyze(
            player,
            world.asteroids,
        )

        visible_asteroids = [
            asteroid
            for asteroid, _ in analysis.ranked_asteroids
        ]

        for asteroid in visible_asteroids:
            obs.extend(
                self._encode_target(
                    player,
                    asteroid.x,
                    asteroid.y,
                    asteroid.velocity_x,
                    asteroid.velocity_y,
                    asteroid.radius,
                    Asteroid.MAX_RADIUS,
                    rad_angle,
                    max_rel_speed,
                )
            )

        missing = (
            self.MAX_ASTEROIDS
            - len(visible_asteroids)
        )

        obs.extend(
            [0.0]
            * self.TARGET_FEATURES
            * missing
        )

        obs.extend(
            [
                analysis.top_risk,
                analysis.risk_vector_x,
                analysis.risk_vector_y,
            ]
        )

        return np.asarray(
            obs,
            dtype=np.float32,
        )
