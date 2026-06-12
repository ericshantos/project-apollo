from typing import Protocol

import numpy as np
from numpy.typing import NDArray


class AgentProtocol(Protocol):
    def act(self, observation: NDArray[np.float32]) -> int: ...

    def learn(
        self,
        state: NDArray[np.float32],
        action: int,
        reward: float,
        next_state: NDArray[np.float32],
        done: bool,
    ) -> None: ...

    def save(self, path: str) -> None: ...
