from .stats import EpisodeStats


class Logger:
    @staticmethod
    def log_episode(stats: EpisodeStats) -> None:
        print(
            f"Episode={stats.episode}",
            f"Reward={stats.reward:.2f}",
            f"Score={stats.score}",
            f"Destroyed={stats.destroyed}",
            f"Wave={stats.wave}",
            f"Accuracy={stats.accuracy:.2%}",
        )
