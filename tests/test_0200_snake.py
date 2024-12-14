import pygame

import snake


def test_contains() -> None:
    """Test in."""
    s = snake.Snake([(2,3),(2,2),(2,1)], (0,255,0), snake.Dir.RIGHT)
    f = snake.Fruit((2,2), (255,0,0))
    assert f in s

def test_change_dir() -> None:
    """Test direction change."""
    s = snake.Snake([(2,3),(2,2),(2,1)], (0,255,0), snake.Dir.RIGHT)
    s.dir = snake.Dir.UP
    assert s.dir == snake.Dir.UP

def test_board_fruit() -> None:
    """Test board create fruit."""
    pygame.init()
    screen = pygame.display.set_mode((300,400))
    board = snake.Board(screen=screen, tile_size=20)

    board.create_fruit()
    assert isinstance (board.objects[0], snake.Fruit)

def test_move() -> None:
    """Test if the fruit is still there."""
    s = snake.Snake([(2,3),(2,2),(2,1)], (0,255,0), snake.Dir.RIGHT)
    f = snake.Fruit((2,5), (255,0,0))

    pygame.init()
    screen = pygame.display.set_mode((300,400))
    board = snake.Board(screen=screen, tile_size=20)

    board.add_object(s)
    board.add_object(f)

    s.move()
    assert board.objects[1] == f

def test_move2() -> None:
    """Test if the fruit was eaten."""
    s = snake.Snake([(2,3),(2,2),(2,1)], (0,255,0), snake.Dir.RIGHT)
    f = snake.Fruit((2,4), (255,0,0))

    pygame.init()
    screen = pygame.display.set_mode((300,400))
    board = snake.Board(screen=screen, tile_size=20)

    board.add_object(s)
    board.add_object(f)

    s.move()
    assert board.objects[1] != f