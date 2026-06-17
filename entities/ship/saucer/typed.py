from typing import TypedDict


class Particle(TypedDict):
    x: float
    y: float

    vx: float
    vy: float

    lifetime: int
    alpha: float
