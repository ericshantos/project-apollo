from pathlib import Path

from stable_baselines3 import DQN

from ..callbacks import ApolloMetricsCallback


class DQNAgent:
    def __init__(self, env, config) -> None:

        policy_kwargs = dict(net_arch=[128, 128])

        self._model = DQN(
            policy="MlpPolicy",
            env=env,
            learning_rate=config.learning_rate,
            buffer_size=config.buffer_size,
            batch_size=config.batch_size,
            gamma=config.gamma,
            tensorboard_log="./logs/tensorboard",
            learning_starts=config.learning_starts,
            policy_kwargs=policy_kwargs,
            target_update_interval=config.target_update_interval,
            verbose=1,
        )

    def train(
        self,
        total_timesteps: int,
    ) -> None:
        callback = ApolloMetricsCallback()

        self._model.learn(
            total_timesteps=total_timesteps, callback=callback, tb_log_name="apollo_dqn"
        )

    def act(self, observation, deterministic: bool = True) -> int:
        action, _ = self._model.predict(observation, deterministic=deterministic)

        return int(action)

    def save(self, path: str | Path) -> None:
        self._model.save(path)
