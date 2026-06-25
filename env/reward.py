from configs import cfg

from .action_space import ActionMap
from .danger_model import DangerModel
from .game_world import GameWorld
from .toroidal_space import ToroidalSpace


class RewardFunction:
    def __init__(self, space: ToroidalSpace) -> None:
        self.danger_model = DangerModel(space)

        self.previous_score = 0
        self.previous_lives = cfg.game.max_lives
        self.previous_risk = 0.0

    def reset(self) -> None:
        self.previous_score = 0
        self.previous_lives = cfg.game.max_lives
        self.previous_risk = 0.0

    def compute(
        self,
        world: GameWorld,
        action: ActionMap,
    ) -> float:

        reward = cfg.reward.survive_step

        current_score = world.score

        score_delta = current_score - self.previous_score

        reward += score_delta * 0.01

        self.previous_score = current_score

        # -------------------------
        # LIVES
        # -------------------------
        current_lives = world.player_lives

        if current_lives < self.previous_lives:
            reward -= 3.0

        self.previous_lives = current_lives

        # -------------------------
        # ACTION COST
        # -------------------------
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

        # -------------------------
        # DANGER SHAPING
        # -------------------------
        analysis = self.danger_model.analyze(
            world.player,
            world.asteroids,
        )

        current_risk = analysis.top_risk

        reward -= 0.05 * current_risk

        reward += 0.02 * (
            self.previous_risk - current_risk
        )

        self.previous_risk = current_risk

        # -------------------------
        # TERMINAL
        # -------------------------
        if world.is_done():
            reward -= 10.0

        return reward
