"""Snake game."""
from __future__ import annotations

import abc
import argparse
import enum
import random
import re
from collections.abc import Iterator
from typing import NoReturn

import pygame


class SnakeException(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class GameOver(SnakeException):

    def __init__(self) -> None:
        super().__init__("Game Over")

class SnakeError(SnakeException):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class IntRangeError(SnakeError):

    def __init__(self, value: int, arg: str, min: int, max: int) -> None:
        super().__init__(f"Value {value} of {arg} is out of allowed range [{min};{max}].")

class ColorError(SnakeError):

    def __init__(self, value: str, arg: str) -> None:
        super().__init__(f"Wrong color ({value}) for argument {arg}.")

class Observer(abc.ABC):
    """Observers class."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()

    def notify_object_eaten(self, obj: Fruit) -> None:
        """Object eaten."""

    def notify_object_moved(self, obj: GameObject) -> None:
        """Object moved."""

    def notify_collision(self, obj: GameObject) -> None:
        """Collisions detected."""

class Subject(abc.ABC):
    """Subject class."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        """Return observer list."""
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        """Add observation."""
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        """Remove observation."""
        self._observers.remove(obs)

class Tile:
    """Tile object."""

    def __init__(self, row: int, column: int, color: str) -> None:
        """Init."""
        self._row = row
        self._column = column
        self._color = color

    def __eq__(self, other: object) -> bool:
        """Tell if 2 tiles are at the same place."""
        if not isinstance(other, Tile):
            raise TypeError("Equality tested between a tile and something else")
        return self._column == other.column and self._row == other.row

    def draw(self, screen: pygame.Surface, tile_size: int) -> None:
        """Draws a tile."""
        rect = pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)

    def __add__(self, other: Dir) -> Tile:
        """Use + to add a direction to a tile."""
        if not isinstance(other, Dir):
            raise TypeError("Given object for addition is not a direction")
        return Tile(self._row + other.value[1], self._column + other.value[0], self._color)

    @property
    def row(self) -> int:
        """Row."""
        return self._row

    @property
    def column(self) -> int:
        """Column."""
        return self._column

    @property
    def color(self) -> str:
        """Color."""
        return self._color

    @color.setter
    def color(self, new_color: str) -> None:
        """Change color."""
        self._color = new_color

class GameObject(Subject, Observer):
    """Class common to all game objects."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()

    def __contains__(self, obj: GameObject) -> bool:
        """Implement in operator."""
        if isinstance(obj, GameObject):
            return any(t==ti for ti in obj.tiles for t in self.tiles)
        return False

    @property
    @abc.abstractmethod
    def tiles(self) -> Iterator[Tile]:
        """Raises an error if no iteration on tiles is defined."""
        raise NotImplementedError

    @property
    def background(self) -> bool:
        """All gameobjects are not background by default."""
        return False

class Board(Subject, Observer):
    """Game board storing all game objects."""

    def __init__(self, screen: pygame.Surface, tile_size: int) -> None:
        """Init."""
        super().__init__()
        self._screen = screen
        self._tile_size = tile_size
        self._objects: list[GameObject]= []
        self._border = []

    def draw(self) -> None:
        """Draws every objects of the board."""
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def add_object(self, obj: GameObject) -> None:
        """Add an object to the board."""
        self._objects.append(obj)
        obj.attach_obs(self)

    def remove_object(self, obj: GameObject) -> None:
        """Remove an object from the board."""
        obj.detach_obs(self)
        self._objects.remove(obj)

    def detect_collision(self, obj: GameObject) -> GameObject | None:
        """Detect any collisons excepting background objects."""
        for o in self._objects:
            if o != obj and not o.background and o in obj:
                return o
        return None

    def create_fruit(self, color: str) -> Fruit:
        """Create a new fruit."""
        fruit = None
        while fruit is None or self.detect_collision(fruit) is not None:
            fruit = Fruit((random.randint(0, int(self._screen.get_height()/self._tile_size) - 1), random.randint(0, int(self._screen.get_width()/self._tile_size) - 1)), color)  # noqa: S311
        self.add_object(fruit)

    def notify_object_moved(self, obj: GameObject) -> None:
        """Check for collision and notify if there is."""
        o = self.detect_collision(obj)
        if o is not None:
            obj.notify_collision(o)

        # Check if the snake exits the screen
        for tile in obj.tiles:
            if not 0<=tile.row<=(self._screen.get_height()/self._tile_size - 1) or not 0<=tile.column<=(self._screen.get_width()/self._tile_size - 1):
                raise GameOver()

    def notify_object_eaten(self, obj: Fruit) -> None:
        """Remove the object eaten."""
        self.remove_object(obj)
        self.create_fruit(obj.color)

    @property
    def objects(self) -> list[GameObject]:
        """Return objects."""
        return self._objects

class CheckerBoard(GameObject):
    """Checkerboard as a background for the game."""

    def __init__(self, size: argparse.Namespace, color1: str, color2: str) -> None:
        """Init."""
        super().__init__()
        self._size = size
        self._color1 = color1
        self._color2 = color2

    @property
    def tiles(self) -> Iterator[Tile]:
        """Return the iterator on tiles."""
        for row in range(self._size.height):
            for column in range(self._size.width):
                yield Tile(row=row, column=column, color=self._color1 if (row+column)%2==0 else self._color2)

    @property
    def background(self) -> bool:
        """Checkerboard is a background object."""
        return True

class Dir(enum.Enum):
    """Direction tuples."""

    UP = (0,-1)
    DOWN = (0,1)
    RIGHT = (1,0)
    LEFT = (-1,0)

class Snake(GameObject, Subject):
    """Snake object."""

    def __init__(self, positions: list[tuple[int,int]], body_color: str, head_color: str, direction: Dir) -> None:
        """Init."""
        super().__init__()
        self._tiles = [Tile(positions[0][0], positions[0][1], head_color)]
        for p in positions[1:]:
            self._tiles.append(Tile(p[0], p[1], body_color))
        self._lenght= len(self._tiles)
        self._body_color = body_color
        self._head_color = head_color
        self._direction = direction

    def __len__(self) -> int:
        """Return the length of the snake."""
        return len(self._tiles)

    def move(self) -> None:
        """Move the snake."""
        # moving the head, the snake becomes one tile longer
        new_head = self._tiles[0] + self._direction
        if new_head in self._tiles:
            raise GameOver()
        self._tiles.insert(0, new_head)
        self._tiles[1].color = self._body_color

        # notify observers
        for obs in self.observers:
            obs.notify_object_moved(self)

        # remove tail if no fruit was eaten
        if self._lenght < len(self._tiles):
            self._tiles.pop()

    def notify_collision(self, obj: GameObject) -> None:
        """Check if it is a fruit to eat it."""
        if isinstance(obj, Fruit):
            self._lenght += 1
            for o in self.observers:
                o.notify_object_eaten(obj)

    @property
    def tiles(self) -> Iterator[Tile]:
        """Return the iterator on tiles."""
        return iter(self._tiles)

    @property
    def dir(self) -> Dir:
        """Set direction property."""
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        """Change direction."""
        self._direction = new_direction

class Fruit(GameObject):
    """Fruit object."""

    def __init__(self, position: tuple[int,int], color: str) -> None:
        """Init."""
        super().__init__()
        self._tiles = [Tile(row=position[0], column=position[1], color=color)]
        self._color = color

    @property
    def tiles(self) -> Iterator[Tile]:
        """Return the operator on tiles."""
        return iter(self._tiles)

    @property
    def color(self) -> str:
        """Return the color of the fruit."""
        return self._color

def parser() -> argparse.Namespace:
    """Get the window size as an input for the game."""
    # using argparse to change the window size if wanted
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15
    DEFAULT_FPS = 5
    FPS_MIN = 1
    FPS_MAX = 25
    DEFAULT_FRUIT_COLOR = "#FF0000"
    DEFAULT_SNAKE_BODY_COLOR = "#00FF00"
    DEFAULT_SNAKE_HEAD_COLOR = "#0000FF"

    parser = argparse.ArgumentParser(description="Window size with numbers of tiles.")
    parser.add_argument("-w","--width", type=int, default=DEFAULT_WIDTH, help="Takes an integer value for the width in tiles of the game.")
    parser.add_argument("-e","--height", type=int, default=DEFAULT_HEIGHT, help="Takes an integer value for the height in tiles of the game.")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Takes an integer value for the fps of the game.")
    parser.add_argument("--fruit-color", default=DEFAULT_FRUIT_COLOR, help="Takes the color for the fruits.")
    parser.add_argument("--snake-body-color", default=DEFAULT_SNAKE_BODY_COLOR, help="Takes the color for the snake body.")
    parser.add_argument("--snake-head-color", default=DEFAULT_SNAKE_HEAD_COLOR, help="Takes the color for the snake head.")

    args = parser.parse_args()

    if not (FPS_MIN <= args.fps <= FPS_MAX):
        raise IntRangeError(args.fps, "FPS", FPS_MIN, FPS_MAX)

    if not re.match(r"#([0-9A-Fa-f]){6}$", args.fruit_color):
        raise ColorError(args.fruit_color, "--fruit-color")
    if not re.match(r"#([0-9A-Fa-f]){6}$", args.snake_body_color):
        raise ColorError(args.snake_body_color, "--snake-body-color")
    if not re.match(r"#([0-9A-Fa-f]){6}$", args.snake_head_color):
        raise ColorError(args.snake_head_color, "--snake-head-color")

    return args

def game() -> NoReturn:
    """Run the game."""
    DEFAULT_TILE_SIZE = 20
    DEFAULT_STARTING_SNAKE = [(10,7),(10,6),(10,5)]
    DEFAULT_DIRECTION = Dir.RIGHT

    # initialisation
    pygame.init()

    try:
        args = parser()
        screen = pygame.display.set_mode((args.width*DEFAULT_TILE_SIZE, args.height*DEFAULT_TILE_SIZE))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Snake - score : 0")

        board = Board(screen=screen, tile_size=DEFAULT_TILE_SIZE)

        checkerboard = CheckerBoard(args, "#FFFFFF", "#000000")
        snake = Snake(DEFAULT_STARTING_SNAKE, args.snake_body_color, args.snake_head_color, DEFAULT_DIRECTION) # initial position of the snake
        board.add_object(checkerboard)
        board.add_object(snake)

        board.create_fruit(args.fruit_color)

        game_running = True

        # game loop
        while game_running:
            clock.tick(args.fps)

            for event in pygame.event.get():

                # quit game
                if event.type == pygame.QUIT:
                    game_running = False

                elif event.type == pygame.KEYDOWN:
                    # quit game
                    if event.key == pygame.K_q:
                        game_running = False

                    # change the direction of the snake
                    if event.key == pygame.K_UP:
                        snake.dir = Dir.UP
                    elif event.key == pygame.K_DOWN:
                        snake.dir = Dir.DOWN
                    elif event.key == pygame.K_RIGHT:
                        snake.dir = Dir.RIGHT
                    elif event.key == pygame.K_LEFT:
                        snake.dir = Dir.LEFT

            snake.move()

            board.draw()

            pygame.display.set_caption(f"Snake - score : {len(snake) - 3}")

            pygame.display.update()

    except GameOver:
        print(f"Game Over - score : {len(snake) - 4}")
        pygame.quit()

# game()
