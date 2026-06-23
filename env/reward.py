from configs import cfg

from .game_world import GameWorld
from .action_space import ActionMap


class RewardFunction:
    def __init__(self) -> None:
        self.previous_score: int
        self.previous_lives: int

        self.reset()

    def reset(self) -> None:
        self.previous_score = 0
        self.previous_lives = cfg.game.max_lives

    def compute(self, world: GameWorld, action: ActionMap) -> float:
        reward = cfg.reward.survive_step

        current_score = world.score

        score_delta = current_score - self.previous_score

        reward += score_delta * 0.01

        self.previous_score = current_score

        current_lives = world.player_lives

        if current_lives < self.previous_lives:
            reward -= 3.0

        self.previous_lives = current_lives

        if action.rotate_left:
            reward -= 0.001

        if action.rotate_right:
            reward -= 0.001

        if action.thrust:
            reward -= 0.002

        if action.shoot:
            reward -= 0.003

        if action.hyperspace:
            reward -= 0.01

        if world.is_done():
            reward -= 10

        return reward
