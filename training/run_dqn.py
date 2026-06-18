from agent import DQNAgent
from configs import cfg
from env import AsteroidEnv

from .trainer import Trainer

env: AsteroidEnv = AsteroidEnv()

agent: DQNAgent = DQNAgent(env=env, config=cfg.dqn)

trainer: Trainer = Trainer(agent)

trainer.train(timesteps=cfg.dqn.total_timesteps)
