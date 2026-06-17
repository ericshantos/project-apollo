from configs import cfg
from entities import Asteroid, AsteroidManager, Bullet, Player, Saucer, SaucerManager
from rendering import Renderer

from .action_space import ActionMap
from .collision_manager import CollisionManager
from .respawn_manager import RespawnManager
from .score_manager import ScoreManager


class GameWorld:
    def __init__(self, width: int, height: int, render_mode: True) -> None:
        self.width: int = width
        self.height: int = height

        self.render_mode = render_mode

        self.frame_count: int
        self.done: bool

        self.player: Player
        self.asteroid_manager: AsteroidManager
        self.score_manager: ScoreManager
        self.collision_manager: CollisionManager

        self.initial_asteroids: int = cfg.game.initial_asteroids
        self.wave: int

        self.saucer_spawn_timer: int

        self.player_spawn_timer: int

        self.saucer_manager: SaucerManager

        self.reset()

        if self.render_mode:
            self.renderer: Renderer = Renderer(self)

    def reset(self) -> None:
        self.frame_count = 0

        self.wave = 1

        self.done = False

        self.player = Player(*self.center_world)

        self.saucer_manager = SaucerManager(self.width, self.height)

        self.saucer_spawn_timer = 0

        self.asteroid_manager = AsteroidManager(self.width, self.height)

        self.score_manager = ScoreManager(self.player)

        self.collision_manager = CollisionManager(
            self.player, self.asteroid_manager, self.score_manager
        )

        self.asteroid_manager.spawn_wave(
            self.initial_asteroids, self.player.x, self.player.y
        )

    def _next_wave(self) -> None:
        self.wave += 1

        num_asteroids = min(
            self.initial_asteroids + (self.wave - 1) * 2, cfg.game.max_asteroids
        )

        self.asteroid_manager.spawn_wave(num_asteroids, self.player.x, self.player.y)

    def update(self, action: ActionMap) -> None:
        if self.done:
            return

        self.saucer_spawn_timer += 1

        if (
            self.saucer_manager.saucer is None
            and self.saucer_spawn_timer > self.saucer_manager.spawn_interval(self.score)
        ):
            difficulty_score = self.score + self.wave * 1500

            self.saucer_manager.spawn(difficulty_score)

            self.saucer_spawn_timer = 0

        self.frame_count += 1

        self.player.update(action, self.width, self.height)

        if action.shoot and self.player.is_alive:
            self.player.shoot()

        # if action.hyperspace:
        # self.player.use_hyperspace(
        #    self.width,
        #    self.height
        # )

        self.asteroid_manager.update()

        self.saucer_manager.update(self.player.x, self.player.y)

        self.collision_manager.update(self.saucer)

        self._handle_respawn()

        if self.asteroid_manager.is_empty:
            self._next_wave()

        if self.is_game_over():
            self.done = True

    def _handle_respawn(self) -> None:
        if self.player.is_alive:
            return

        if self.is_game_over():
            return

        if self.player.respawn_timer < self.player.RESPAWN_DELAY:
            return

        if RespawnManager.can_respawn(
            self.player.start_x, self.player.start_y, self.asteroids
        ):
            self.player.respawn()

    def render(self) -> None:
        if not self.render_mode:
            return

        self.renderer.draw()

    @property
    def player_alive(self) -> bool:
        return self.player.is_alive

    @property
    def player_lives(self) -> int:
        return self.player.lives

    @property
    def score(self) -> int:
        return self.score_manager.score

    def is_done(self) -> bool:
        return self.done

    def is_game_over(self) -> bool:
        return self.player.lives <= 0

    @property
    def bullets(self) -> list[Bullet]:
        return self.player.bullet_manager.bullets

    @property
    def asteroids(self) -> list[Asteroid]:
        return self.asteroid_manager.asteroids

    @property
    def asteroids_destroyed(self) -> int:
        return self.collision_manager.asteroids_destroyed

    @property
    def accuracy_hits(self) -> int:
        return self.collision_manager.accuracy_hits

    @property
    def shots_fired(self) -> int:
        return self.player.shots_fired

    @property
    def saucer(self) -> Saucer:
        return self.saucer_manager.saucer

    @property
    def accuracy(self) -> float:
        if self.shots_fired == 0:
            return 0.0

        return self.accuracy_hits / self.shots_fired

    @property
    def center_world(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2
