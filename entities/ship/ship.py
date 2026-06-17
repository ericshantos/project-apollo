from abc import ABC

from ..bullet import Bullet, BulletManager


class Shooter(ABC):
    MAX_BULLETS: int = 4

    def __init__(self) -> None:
        self.bullet_manager = BulletManager()

        self.shots_fired: int = 0

    def can_shoot(self) -> bool:
        return self.bullet_manager.count < self.MAX_BULLETS

    def shoot(self, angle: float | None = None) -> None:
        if not self.can_shoot():
            return

        self.shots_fired += 1

        shot_angle = self.angle if angle is None else angle

        self.bullet_manager.shoot(self.x, self.y, shot_angle)

    @property
    def bullets(self) -> list[Bullet]:
        return self.bullet_manager.bullets
