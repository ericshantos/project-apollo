from typing import Protocol

import numpy as np
from numpy.typing import NDArray


class AgentProtocol(Protocol):
    def act(
        self, observation: NDArray[np.float32], deterministic: bool = True
    ) -> int: ...

    def train(self, total_timesteps: int) -> None: ...

    def save(self, path: str) -> None: ...
