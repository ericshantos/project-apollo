from entities import Player


class ScoreManager:
    def __init__(self, player: Player) -> None:
        self.player = player

        self.score: int
        self.score_extra_for_live: int

        self.reset()

    def __str__(self) -> str:
        return str(self.score)

    def add(self, points: int) -> None:
        if self.player.lives == 0 and not self.player.is_alive:
            return

        self.score += points
        self.score_extra_for_live += points

        if self.score_extra_for_live >= 10000:
            self.player.lives += 1
            self.score_extra_for_live -= 1000

    def get_score(self) -> str:
        if self.score == 0:
            return "00"
        return str(self.score)

    def reset(self) -> None:
        self.score = 0
        self.score_extra_for_live = 0
