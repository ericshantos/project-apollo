from .bullet import Bullet


class BulletManager:
    def __init__(self) -> None:
        self.bullets: list[Bullet] = []

    def shoot(self, x: float, y: float, angle: float) -> None:
        self.bullets.append(Bullet(x, y, angle))

    def update(self, width: int, height: int) -> None:
        for bullet in self.bullets:
            bullet.update(width, height)

        self.clean_expired_bullets()

    def get_bullets(self) -> list[Bullet]:
        return self.bullets

    def remove_bullet(self, bullet: Bullet) -> None:
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def clean_expired_bullets(self) -> None:
        self.bullets = [bullet for bullet in self.bullets if bullet.is_alive()]
