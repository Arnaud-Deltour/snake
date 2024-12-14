import snake


def test_creation() -> None:
    """Test tile creation."""
    t = snake.Tile(1,1,(0,255,0))
    assert t.row == 1

def test_equality() -> None:
    """Test tile equality."""
    t1 = snake.Tile(5,5,(0,0,0))
    t2 = snake.Tile(5,5,(255,255,255))
    assert t1 == t2
