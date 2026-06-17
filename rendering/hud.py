import pygame

from entities import Player

from .font import FontManager


class HUD:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

        self.color: tuple[int, int, int] = (255, 255, 255)

        self.lives_start_x: int = 30
        self.lives_start_y: int = 35
        self.lives_spacing: int = 25

    def draw_score(self, score: str) -> None:
        font = FontManager.to_write(28)

        score_surface = font.render(score, True, self.color)

        score_x = self.screen.get_width() - score_surface.get_width() - 20

        score_y = 10

        self.screen.blit(score_surface, (score_x, score_y))

    def draw_lives(self, player: Player) -> None:
        for i in range(player.lives):
            life_x = self.lives_start_x + (i * self.lives_spacing)
            life_y = self.lives_start_y

            pygame.draw.polygon(
                self.screen,
                self.color,
                [
                    (life_x, life_y - 8),
                    (life_x + 5, life_y + 6),
                    (life_x, life_y + 2),
                    (life_x - 5, life_y + 6),
                ],
                1,
            )
