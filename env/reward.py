from configs import cfg

from .game_world import GameWorld


class RewardFunction:
    def __init__(self) -> None:
        self.previous_score: int = 0
        self.previous_lives: int = cfg.game.max_lives

    def reset(self) -> None:
        self.previous_score = 0
        self.previous_lives = cfg.game.max_lives

    def compute(self, world: GameWorld) -> float:
        reward = cfg.reward.survive_step

        current_score = world.get_score()

        score_delta = current_score - self.previous_score

        reward += score_delta

        self.previous_score = current_score

        current_lives = world.get_player().lives

        if current_lives < self.previous_lives:
            reward -= cfg.reward.player_died

        self.previous_lives = current_lives

        if world.is_done():
            reward -= 20

        if (
            not world.player.is_accelerating
            and abs(world.player.velocity_x) < 0.1
            and abs(world.player.velocity_y) < 0.1
        ):
            reward += cfg.reward.idle_penalty

        return reward
