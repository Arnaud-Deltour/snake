import snake

def test_creation():
    t = snake.Tile(1,1,(0,255,0))
    assert t.row == 1