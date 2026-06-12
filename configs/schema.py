from dataclasses import dataclass


@dataclass
class ScreenConfig:
    width: int
    height: int


@dataclass
class GameConfig:
    max_lives: int
    max_asteroids: int
    max_steps_per_episode: int


@dataclass
class RewardConfig:
    player_died: float
    survive_step: float
    idle_penalty: float


@dataclass
class EnvironmentConfig:
    screen: ScreenConfig
    game: GameConfig
    reward: RewardConfig


@dataclass
class RLConfig:
    observation_radius: float
    max_episode_steps: int
    normalize_observation: bool


@dataclass
class EpsilonConfig:
    start: float
    end: float
    decay: float


@dataclass
class DQNConfig:
    learning_rate: float
    gamma: float
    batch_size: int
    replay_buffer_size: int
    target_update_frequency: int
    epsilon: EpsilonConfig


@dataclass
class TrainingConfig:
    total_timesteps: int
    evaluation_frequency: int
    save_frequency: int
    seed: int
    device: str


@dataclass
class ApolloConfig:
    screen: ScreenConfig
    game: GameConfig
    reward: RewardConfig
    rl: RLConfig
    dqn: DQNConfig
    training: TrainingConfig
