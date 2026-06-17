from abc import ABC, abstractmethod


class ExplosionEffect(ABC):
    def __init__(self) -> None:
        self.is_active = False

    @abstractmethod
    def trigger(self, x: float, y: float) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    def draw(self, surface) -> None:
        pass
