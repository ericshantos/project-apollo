import random
from collections import deque

import numpy as np
from numpy.typing import NDArray

from .typed import Transition


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer: deque[Transition] = deque(maxlen=capacity)

    def add(
        self,
        state: NDArray[np.flaot32],
        action: int,
        reward: float,
        next_state: NDArray[np.flaot32],
        done: bool,
    ) -> None:
        self.buffer.append((state, action, reward, next_state, done))

    def sample(
        self, batch_size: int
    ) -> tuple[
        NDArray[np.flaot32],
        NDArray[np.int64],
        NDArray[np.float32],
        NDArray[np.flaot32],
        NDArray[np.bool_],
    ]:
        batch = random.sample(self.buffer, batch_size)

        states, actions, rewards, next_states, dones = zip(*batch, strict=False)

        return (
            np.array(states),
            np.array(actions),
            np.array(rewards),
            np.array(next_states),
            np.array(dones),
        )

    def __len__(self) -> int:
        return len(self.buffer)
