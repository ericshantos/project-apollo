import random
from dataclasses import dataclass
from enum import IntEnum


@dataclass(slots=True)
class ActionMap:
    rotate_right: bool = False
    rotate_left: bool = False
    thrust: bool = False
    shoot: bool = False
    hyperspace: bool = False


class Action(IntEnum):
    NOTHING = 0
    LEFT = 1
    RIGHT = 2
    THRUST = 3
    SHOOT = 4
    HYPERSPACE = 5
    THRUST_SHOOT = 6
    LEFT_THRUST = 7
    RIGHT_THRUST = 8
    LEFT_SHOOT = 9
    RIGHT_SHOOT = 10
    LEFT_THRUST_SHOOT = 11
    RIGHT_THRUST_SHOOT = 12


class ActionSpace:
    N_ACTIONS: int = len(Action)

    @staticmethod
    def to_action(action_id: int) -> ActionMap:
        match action_id:
            case Action.NOTHING:
                return ActionMap()

            case Action.LEFT:
                return ActionMap(rotate_left=True)

            case Action.RIGHT:
                return ActionMap(rotate_right=True)

            case Action.THRUST:
                return ActionMap(thrust=True)

            case Action.SHOOT:
                return ActionMap(shoot=True)

            case Action.HYPERSPACE:
                return ActionMap(hyperspace=True)

            case Action.THRUST_SHOOT:
                return ActionMap(thrust=True, shoot=True)

            case Action.LEFT_THRUST:
                return ActionMap(rotate_left=True, thrust=True)

            case Action.RIGHT_THRUST:
                return ActionMap(rotate_right=True, thrust=True)

            case Action.LEFT_SHOOT:
                return ActionMap(rotate_left=True, shoot=True)

            case Action.RIGHT_SHOOT:
                return ActionMap(rotate_right=True, shoot=True)

            case Action.LEFT_THRUST_SHOOT:
                return ActionMap(rotate_left=True, thrust=True, shoot=True)

            case Action.RIGHT_THRUST_SHOOT:
                return ActionMap(rotate_right=True, thrust=True, shoot=True)

            case _:
                raise ValueError(f"Invalid action_id: {action_id}")

    @staticmethod
    def sample() -> Action:
        return random.choice(list(Action))
