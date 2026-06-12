import numpy as np
from numpy.typing import NDArray

from env.action_space import ActionSpace


class RandomAgent:
    def act(self, observation: NDArray[np.float32]) -> int:
        return ActionSpace.sample()

    def learn(self) -> None: ...

    def save(self, path: str) -> None: ...
