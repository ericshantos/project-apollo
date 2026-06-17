from agents import AgentProtocol, RandomAgent
from env import AsteroidEnv

from .trainer import Trainer

env: AsteroidEnv = AsteroidEnv(render_mode="human")

agent: AgentProtocol = RandomAgent()

trainer: Trainer = Trainer(env, agent)

trainer.train(episodes=100)
