from dataclasses import dataclass


@dataclass(slots=True)
class EpisodeStats:
    episode: int
    reward: float
    score: int
    destroyed: int
    wave: int
    accuracy: float
