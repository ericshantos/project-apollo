import random


class HyperspaceManager:
    FAILURE_CHANCE: float = 0.02
    INCREMENT: float = 0.003

    def __init__(self) -> None:
        self.uses: int = 0

    def teleport(
        self,
        width: int,
        height: int,
    ) -> tuple[float, float]:
        return (random.uniform(0, width), random.uniform(0, height))

    def should_explode(self) -> bool:
        probability = self.FAILURE_CHANCE + self.uses * self.INCREMENT

        self.uses += 1

        return random.random() < probability

    def reset(self) -> None:
        self.uses = 0
