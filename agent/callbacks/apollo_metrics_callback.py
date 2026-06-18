from stable_baselines3.common.callbacks import BaseCallback


class ApolloMetricsCallback(BaseCallback):
    def __init__(self, verbose: int = 0) -> None:
        super().__init__(verbose)

    def _on_step(self) -> bool:
        infos = self.locals.get("infos")

        if not infos:
            return True

        info = infos[0]

        self.logger.record("apollo/score", info.get("score", 0))

        self.logger.record("apollo/destroyed", info.get("asteroid_destroyed", 0))

        self.logger.record("apollo/wave", info.get("wave", 0))

        self.logger.record("apollo/accuracy", info.get("accuracy", 0.0))

        return True
