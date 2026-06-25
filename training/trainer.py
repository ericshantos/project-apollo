from agent import AgentProtocol


class Trainer:
    def __init__(self, agent: AgentProtocol) -> None:
        self._agent = agent

    def train(self, timesteps: int) -> None:
        self._agent.train(total_timesteps=timesteps)

        self._agent.save("models/apollo_dqn.zip")
