import pygame
import argparse

class Tile:

    def __init__(self, row, column, size, color):
        self._row = row
        self._column = column
        self._size = size
        self._color = color

    def __repr__(self):
        return f"Tile on row {self._row} and column {self._column}"

    def draw(self, screen):
        rect = pygame.Rect(self._column*self._size, self._row*self._size, self._size, self._size)
        pygame.draw.rect(screen, self._color, rect)

class CheckerBoard:

    def __init__(self, size, color1, color2, tile_size):
        self._size = size
        self._color1 = color1
        self._color2 = color2
        self._tile_size = tile_size

    def __repr__(self):
        return f"Checkerboard size : {self._size} colors : {self._color1},{self._color2}"

    def draw(self, screen):
        screen.fill(self._color1)
        for i in range(0,self._size.height,2):
            for j in range(0,self._size.width,2):
                tile = Tile(i,j,self._tile_size,self._color2)
                tile.draw(screen)
        for i in range(1,self._size.height,2):
            for j in range(1,self._size.width,2):
                tile = Tile(i,j,self._tile_size,self._color2)
                tile.draw(screen)

class Snake:

    def __init__(self, position, color, size, tile_size, direction):
        self._position = position
        self._color = color
        self._size = size
        self._tile_size = tile_size
        self._direction = direction

    def __repr__(self):
        return f"Snake in {self._position}"

    # drawing the snake
    def draw(self, screen):
        for p in self._position:
            tile = Tile(p[0],p[1],self._tile_size,self._color)
            tile.draw(screen)

    # making the snake move
    def move(self, fruit):
        self._position.insert(0, ((self._position[0][0] + self._direction[0])%self._size.height, (self._position[0][1] + self._direction[1])%self._size.width))
        if fruit.eating(self._position[0]):
            pass
        else:
            self._position.pop()

    # changing the direction of the snake
    def up(self):
        if self._direction != (1,0):
            self._direction = (-1,0)

    def down(self):
        if self._direction != (-1,0):
            self._direction = (1,0)

    def right(self):
        if self._direction != (0,-1):
            self._direction = (0,1)

    def left(self):
        if self._direction != (0,1):
            self._direction = (0,-1)

class Fruit:

    def __init__(self, position, color, tile_size):
        self._position = position
        self._color = color
        self._tile_size = tile_size

    def __repr__(self):
        return f"Fruit in {self._position}"

    def draw(self, screen):
        tile = Tile(self._position[0],self._position[1],self._tile_size,self._color)
        tile.draw(screen)

    def eating(self, snake_head):
        return self._position == snake_head

def windowsize():
    # using argparse to change the window size if wanted
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15
    
    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-w','--width', type=int, default=DEFAULT_WIDTH, help="Takes an integer value for the width in tiles of the game.")
    parser.add_argument('-e','--height', type=int, default=DEFAULT_HEIGHT, help="Takes an integer value for the height in tiles of the game.")
    args = parser.parse_args()

    return args

def game():
    # main function for the game
    DEFAULT_TILE_SIZE = 20
    DEFAULT_STARTING_SNAKE = [(10,7),(10,6),(10,5)]
    DEFAULT_DIRECTION = (0,1)

    # initialisation
    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode( (size.width*DEFAULT_TILE_SIZE, size.height*DEFAULT_TILE_SIZE) )
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

    checkerboard = CheckerBoard(size, (0,0,0), (255,255,255), DEFAULT_TILE_SIZE)
    snake = Snake(DEFAULT_STARTING_SNAKE, (0,255,0), size, DEFAULT_TILE_SIZE, DEFAULT_DIRECTION) # initial position of the snake
    fruit = Fruit((3,3), (255,0,0), DEFAULT_TILE_SIZE)
    game_running = True

    # game loop
    while game_running:
        clock.tick(10)

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
                    snake.up()
                    break
                if event.key == pygame.K_DOWN:
                    snake.down()
                    break
                if event.key == pygame.K_RIGHT:
                    snake.right()
                    break
                if event.key == pygame.K_LEFT:
                    snake.left()
                    break
        
        snake.move(fruit)

        checkerboard.draw(screen)
        fruit.draw(screen)
        snake.draw(screen)

        pygame.display.update()

    pygame.quit()
    quit(0)