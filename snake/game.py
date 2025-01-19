# ruff: noqa: D100,S311

# Third party
import importlib.resources
from pathlib import Path

import pygame

# First party
from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit
from .score import Score
from .scores import Scores
from .snake import Snake
from .state import State

# Constants
SK_START_LENGTH = 3

class Game:
    """The main class of the game."""

    def __init__(self, width: int, height: int, tile_size: int, # noqa: PLR0913
                 fps: int,
                 *,
                 fruit_color: pygame.Color,
                 snake_head_color: pygame.Color,
                 snake_body_color: pygame.Color,
                 gameover_on_exit: bool,
                 score_file: Path,
                 ) -> None:
        """Object initialization."""
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._fps = fps
        self._fruit_color = fruit_color
        self._snake_head_color = snake_head_color
        self._snake_body_color = snake_body_color
        self._gameover_on_exit = gameover_on_exit
        self._snake = None
        self._new_high_score=None | Score
        self._score_file=score_file

    def _reset_snake(self) -> None:
        if self._snake is not None:
            self._board.detach_obs(self._snake)
            self._board.remove_object(self._snake)
        self._snake = Snake.create_random(
                nb_lines = self._height,
                nb_cols = self._width,
                length = SK_START_LENGTH,
                head_color = self._snake_head_color,
                body_color = self._snake_body_color,
                gameover_on_exit = self._gameover_on_exit,
                )
        self._board.add_object(self._snake)
        self._board.attach_obs(self._snake)

    def _init(self) -> None:
        """Initialize the game."""
        # Create a display screen
        screen_size = (self._width * self._tile_size,
                       self._height * self._tile_size)
        self._screen = pygame.display.set_mode(screen_size)

        # Create the clock
        self._clock = pygame.time.Clock()

        # Create the main board
        self._board = Board(screen = self._screen,
                            nb_lines = self._height,
                            nb_cols = self._width,
                            tile_size = self._tile_size)

        # Create checkerboard
        self._checkerboard = Checkerboard(nb_lines = self._height,
                                          nb_cols = self._width)
        self._board.add_object(self._checkerboard)

        # Create snake
        self._reset_snake()

        #Best Scores
        if self._score_file.exists():
            self._scores = Scores.load(self._score_file)
        else:
            self._scores = Scores.default(5)
            self._scores.save(self._score_file)

        # Create fruit
        Fruit.color = self._fruit_color
        self._board.create_fruit()

        #Upload fonts
        with importlib.resources.path("snake", "DejaVuSansMono-Bold.ttf") as f:
            self._fontscore = pygame.font.Font(f, 32)
            self._fontgameover = pygame.font.Font(f, 64)

    def _drawgameover(self) -> None:
        text_gameover = self._fontgameover.render("Game Over", True, pygame.Color("red"))  # noqa: E501, FBT003
        x, y = 80, 160
        self._screen.blit(text_gameover, (x, y))

    def _draw_scores(self) -> None:
        #mettre une ligne high scores
        x, y = 80, 10
        for score in self._scores:
            text_score = self._fontscore.render(score.name.ljust(Score.MAX_LENGTH)+ f"{score.score:.>8}", True, pygame.Color("red"))
            self._screen.blit(text_score, (x, y))
            y += 32

    def _process_scores_event(self, event: any) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._state = State.PLAY

    def _process_inputname(self, event: pygame.event.Event) -> None :
        """The player put his/her name in the ranking list of highscores."""
        if self._new_high_score is not None and event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RETURN:  # Validate the name
                self._state = State.SCORES
                self._scores.save(self._score_file)
            elif event.key == pygame.K_BACKSPACE:  # Correct a mistake
                self._new_high_score.name=self._new_high_score.name[:-1]
            else :
                self._new_high_score.name+= event.unicode


    def _process_play_event(self, event: any) -> None:
        # Key press
        if event.type == pygame.KEYDOWN:
            # Quit
            match event.key:
                case pygame.K_UP:
                    self._snake.dir = Dir.UP
                case pygame.K_DOWN:
                    self._snake.dir = Dir.DOWN
                case pygame.K_LEFT:
                    self._snake.dir = Dir.LEFT
                case pygame.K_RIGHT:
                    self._snake.dir = Dir.RIGHT


    def _process_events(self) -> None:
        """Process pygame events."""
        # Loop on all events
        for event in pygame.event.get():

            match self._state:
                case State.SCORES:
                    self._process_scores_event(event)
                case State.PLAY:
                    self._process_play_event(event)
                case State.INPUT_NAME :
                    self._process_inputname(event)

            # Closing window (Mouse click on cross icon or OS keyboard shortcut)
            if event.type == pygame.QUIT:
                self._state = State.QUIT

            # Key press
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self._state = State.QUIT


    def start(self) -> None:
        """Start the game."""
        # Initialize pygame
        pygame.init()


        # Initialize game
        self._init()

        # Start pygame loop
        self._state = State.SCORES
        while self._state != State.QUIT:

            # Wait 1/FPS second
            self._clock.tick(self._fps)

            # Listen for events
            self._process_events()

            # Update objects
            try:
                if self._state == State.PLAY:
                    self._snake.move()
            except GameOver:
                self._state = State.GAME_OVER
                cpt = self._fps

            # Draw
            self._board.draw()
            match self._state :
                case State.GAME_OVER :
                    self._drawgameover()
                    cpt-=1
                    if cpt==0 :
                        score=len(self._snake._tiles)
                        self._reset_snake()
                        if self._scores.is_highscore(score):
                            self._new_high_score=Score(name="", score=score)
                            self._scores.add_score(self._new_high_score)
                            self._state= State.INPUT_NAME
                        else :
                            self._state=State.SCORES
                case State.SCORES | State.INPUT_NAME:
                    self._draw_scores()


            # Display
            pygame.display.update()

    # Terminate pygame
    pygame.quit()

