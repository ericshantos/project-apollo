from agents import AgentProtocol
from env import AsteroidEnv

from .logger import Logger
from .stats import EpisodeStats


class Trainer:
    def __init__(self, env: AsteroidEnv, agent: AgentProtocol) -> None:
        self.env = env
        self.agent = agent

    def train(self, episodes: int) -> None:
        for episode in range(episodes):
            obs, _ = self.env.reset()

            done: bool = False

            total_reward: float = 0

            while not done:
                action = self.agent.act(obs)

                (next_obs, reward, terminated, truncated, info) = self.env.step(action)

                done = terminated or truncated

                total_reward += reward

                obs = next_obs

                stats = EpisodeStats(
                    episode=episode,
                    reward=total_reward,
                    score=info["score"],
                    destroyed=info["asteroid_destroyed"],
                    wave=info["wave"],
                    accuracy=info["accuracy"],
                )

            Logger.log_episode(stats)
