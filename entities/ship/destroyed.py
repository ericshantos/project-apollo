from abc import ABC, abstractmethod


class Destroyable(ABC):
    @abstractmethod
    def die(self) -> None:
        pass
