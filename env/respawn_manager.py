import numpy as np

from entities import Asteroid


class RespawnManager:
    SAFE_RADIUS: float = 120.0

    @classmethod
    def can_respawn(cls, x: float, y: float, asteroids: list[Asteroid]) -> bool:
        for asteroid in asteroids:
            dx = asteroid.x - x
            dy = asteroid.y - y

            distance = float(np.hypot(dx, dy))

            safe_distance = cls.SAFE_RADIUS + asteroid.radius

            if distance <= safe_distance:
                return False

        return True
