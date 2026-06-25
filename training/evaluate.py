from pathlib import Path

from stable_baselines3 import DQN

from env import AsteroidEnv
import numpy as np


MODEL_PATH = Path("models/apollo_dqn.zip")
EPISODES = 20


def evaluate():
    env = AsteroidEnv(render_mode="human")

    model = DQN.load(MODEL_PATH)

    scores = []
    survival_times = []
    accuracies = []
    asteroids_destroyed = []

    for episode in range(EPISODES):
        obs, info = env.reset()

        done = False
        truncated = False

        while not (done or truncated):
            action, _ = model.predict(obs, deterministic=True)

            obs, reward, done, truncated, info = env.step(action)

        scores.append(info.get("score", 0))
        survival_times.append(info.get("survival_time", 0))
        accuracies.append(info.get("accuracy", 0))
        asteroids_destroyed.append(
            info.get("asteroids_destroyed", 0)
        )

        print(
            f"Episode {episode + 1:02d} | "
            f"Score={scores[-1]} | "
            f"Asteroids={asteroids_destroyed[-1]} | "
            f"Accuracy={accuracies[-1]:.2%}"
        )

    print("\n=== RESULTS ===")

    print(f"Episodes: {EPISODES}")

    print(
        f"Average score: "
        f"{np.mean(scores):.2f}"
    )

    print(
        f"Average survival time: "
        f"{np.mean(survival_times):.2f}"
    )

    print(
        f"Average accuracy: "
        f"{np.mean(accuracies):.2%}"
    )

    print(
        f"Average asteroids destroyed: "
        f"{np.mean(asteroids_destroyed):.2f}"
    )

    env.close()


if __name__ == "__main__":
    evaluate()