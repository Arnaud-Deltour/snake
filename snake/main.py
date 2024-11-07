import pygame
import argparse

def windowsize():
    # using argparse to change the window size if wanted
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15
    
    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-w','--width', type=int, default=DEFAULT_WIDTH, help="Takes an integer value for the width in tiles of the game.")
    parser.add_argument('-e','--height', type=int, default=DEFAULT_HEIGHT, help="Takes an integer value for the height in tiles of the game.")
    args = parser.parse_args()

    return args

def checkerboard(size, screen):
    # draws the checkerboard for the background

    screen.fill( (0, 0, 0) )
    color = (255, 255, 255)
    for i in range(0,size.width,2):
        for j in range(0,size.height,2):
            rect = pygame.Rect(i*20, j*20, 20, 20)
            pygame.draw.rect(screen, color, rect)
    for i in range(1,size.width,2):
        for j in range(1,size.height,2):
            rect = pygame.Rect(i*20, j*20, 20, 20)
            pygame.draw.rect(screen, color, rect)

def draw_snake(screen, snake_position):
    # draws the snake

    color = (0, 255, 0)
    for t in snake_position:
        rect = pygame.Rect(t[1]*20, t[0]*20, 20, 20)
        pygame.draw.rect(screen, color, rect)

def snake():
    # main function for the game

    # initialisation
    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode( (size.width*20, size.height*20) )
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

    snake_position = [(10,5),(10,6),(10,7)] # initial position of the snake
    game_running = True

    # game loop
    while game_running:
        clock.tick(10)

        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_running = False
        
        checkerboard(size, screen)
        draw_snake(screen, snake_position)

        pygame.display.update()

    pygame.quit()
    quit(0)