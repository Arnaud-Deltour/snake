"""Snake game."""

import abc
import argparse
import enum
import random
from collections.abc import Iterator
from typing import Any, NoReturn

import pygame


class Board:
    """Game board storing all game objects."""

    def __init__(self: Any, screen: pygame.Surface, tile_size: int) -> None:
        """Init."""
        self._screen = screen
        self._tile_size = tile_size
        self._objects: list[object]= []

    def draw(self: Any) -> None:
        """Draws every objects of the board."""
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def add_object(self: Any, gameobject: object) -> None:
        """Add an object to the board."""
        self._objects.append(gameobject)

class GameObject(abc.ABC):
    """Class common to all game objects."""

    def __init__(self: Any) -> None:
        """Init."""
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self: Any) -> Iterator[object]:
        """Raises an error if no iteration on tiles is defined."""
        raise NotImplementedError

class Tile:
    """Tile object."""

    def __init__(self: Any, row: int, column: int, color: tuple[int,int,int]) -> None:
        """Init."""
        self._row = row
        self._column = column
        self._color = color

    def draw(self: Any, screen: pygame.Surface, tile_size: int) -> None:
        """Draws a tile."""
        rect = pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)

    def __add__(self: Any, other: tuple[int,int]) -> object:
        """Use + to add a direction to a tile."""
        if not isinstance(other, Dir):
            raise TypeError("Given object for addition is not a direction")
        return Tile(self._row + other.value[1], self._column + other.value[0], self._color)

class CheckerBoard(GameObject):
    """Checkerboard as a background for the game."""

    def __init__(self: Any, size: object, color1: tuple[int,int,int], color2: tuple[int,int,int]) -> None:
        """Init."""
        super().__init__()
        self._size = size
        self._color1 = color1
        self._color2 = color2

    @property
    def tiles(self: Any) -> Iterator[object]:
        """Return the iterator on tiles."""
        for row in range(self._size.height):
            for column in range(self._size.width):
                yield Tile(row=row, column=column, color=self._color1 if (row+column)%2==0 else self._color2)

class Dir(enum.Enum):
    """Direction tuples."""

    UP = (0,-1)
    DOWN = (0,1)
    RIGHT = (1,0)
    LEFT = (-1,0)

class Snake(GameObject):
    """Snake object."""

    def __init__(self: Any, positions: list[tuple[int,int]], color: tuple[int,int,int], direction: tuple[int,int]) -> None:
        """Init."""
        super().__init__()
        self._tiles = [Tile(p[0], p[1], color) for p in positions]
        self._color = color
        self._direction = direction

    def __len__(self: Any) -> int:
        """Return the length of the snake."""
        return len(self._tiles)

    def move(self: Any) -> None:
        """Move the snake."""
        # moving the head, the snake becomes one tile longer
        self._tiles.insert(0, self._tiles[0] + self._direction)

        # cheking if the fruit was eaten
        #if fruit.eating(self._position[0]):
        #    fruit.move(self._size)
        #else:
        self._tiles.pop()

    @property
    def tiles(self: Any) -> Iterator[object]:
        """Return the iterator on tiles."""
        return iter(self._tiles)

    @property
    def dir(self: Any) -> Any:
        """Set direction property."""
        return self._direction

    @dir.setter
    def dir(self: Any, new_direction: tuple[int,int]) -> None:
        """Change direction."""
        self._direction = new_direction

class Fruit(GameObject):
    """Fruit object."""

    def __init__(self: Any, position: tuple[int,int], color: tuple[int,int,int]) -> None:
        """Init."""
        super().__init__()
        self._tiles = [Tile(row=position[0], column=position[1], color=color)]
        self._color = color

    # test if the snake_head is where the fruit is
    def eating(self, snake_head):
        return self._position == snake_head

    # randomly moves the fruit, taking the size of the game
    def move(self, size):
        self._position = (random.randint(0, size.height - 1), random.randint(0, size.width - 1))

    @property
    def tiles(self: Any) -> Iterator[object]:
        """Return the operator on tiles."""
        return iter(self._tiles)

def windowsize() -> object:
    """Get the window size as an input for the game."""
    # using argparse to change the window size if wanted
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15

    parser = argparse.ArgumentParser(description="Window size with numbers of tiles.")
    parser.add_argument("-w","--width", type=int, default=DEFAULT_WIDTH, help="Takes an integer value for the width in tiles of the game.")
    parser.add_argument("-e","--height", type=int, default=DEFAULT_HEIGHT, help="Takes an integer value for the height in tiles of the game.")

    return parser.parse_args()

def game() -> NoReturn:
    """Run the game."""
    DEFAULT_TILE_SIZE = 20
    DEFAULT_STARTING_SNAKE = [(10,7),(10,6),(10,5)]
    DEFAULT_DIRECTION = Dir.RIGHT

    # initialisation
    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode((size.width*DEFAULT_TILE_SIZE, size.height*DEFAULT_TILE_SIZE))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake - score : 0")

    board = Board(screen=screen, tile_size=DEFAULT_TILE_SIZE)

    checkerboard = CheckerBoard(size, (0,0,0), (255,255,255))
    snake = Snake(DEFAULT_STARTING_SNAKE, (0,255,0), DEFAULT_DIRECTION) # initial position of the snake
    fruit = Fruit((3,3), (255,0,0))
    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)

    game_running = True

    # game loop
    while game_running:
        clock.tick(5)

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

    pygame.quit()
    quit(0)