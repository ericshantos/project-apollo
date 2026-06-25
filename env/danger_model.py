from dataclasses import dataclass

import numpy as np

from entities import Asteroid, Player

from .toroidal_space import ToroidalSpace


@dataclass(slots=True)
class DangerMetrics:
    top_risk: float
    risk_vector_x: float
    risk_vector_y: float


class DangerModel:
    def __init__(
        self,
        space: ToroidalSpace,
        max_asteroids: int = 5,
    ) -> None:
        self.space = space
        self.max_asteroids = max_asteroids

    def risk_score(
        self,
        player: Player,
        asteroid: Asteroid,
    ) -> float:
        dx, dy = self.space.relative_vector(
            player.x,
            player.y,
            asteroid.x,
            asteroid.y,
        )

        distance = np.hypot(dx, dy) + 1e-6

        dvx = asteroid.velocity_x - player.velocity_x
        dvy = asteroid.velocity_y - player.velocity_y

        closing_velocity = (dx * dvx + dy * dvy) / distance

        danger = 1.0 / (distance**2 + 1e-6)
        urgency = max(0.0, -closing_velocity)

        return float(danger * urgency)

    def ranked_asteroids(
        self,
        player: Player,
        asteroids: list[Asteroid],
    ) -> list[tuple[Asteroid, float]]:
        ranked = [
            (asteroid, self.risk_score(player, asteroid))
            for asteroid in asteroids
        ]

        ranked.sort(key=lambda item: item[1], reverse=True)

        return ranked

    def metrics(
        self,
        player: Player,
        asteroids: list[Asteroid],
    ) -> DangerMetrics:

        ranked = self.ranked_asteroids(player, asteroids)

        selected = ranked[: self.max_asteroids]

        top_risk = sum(risk for _, risk in selected)

        risk_vector = np.zeros(2, dtype=np.float32)

        for asteroid, risk in selected:
            direction = self.space.direction(
                player.x,
                player.y,
                asteroid.x,
                asteroid.y,
            )

            risk_vector += direction * risk

        if selected:
            risk_vector /= len(selected)

        return DangerMetrics(
            top_risk=float(top_risk),
            risk_vector_x=float(risk_vector[0]),
            risk_vector_y=float(risk_vector[1]),
        )
