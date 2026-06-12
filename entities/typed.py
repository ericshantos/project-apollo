from typing import TypedDict


class AsteroidParticle(TypedDict):
    x: float
    y: float
    vel_x: float
    vel_y: float
    alpha: int


class SaucerParticle(TypedDict):
    x: float
    y: float

    vx: float
    vy: float

    lifetime: int
    alpha: float


class ShipFragments(TypedDict):
    x1: float
    y1: float

    x2: float
    y2: float

    vel_x: float
    vel_y: float

    alpha: int
