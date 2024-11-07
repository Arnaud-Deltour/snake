import pygame
import argparse

def windowsize():
    # using argparse to change the window size if wanted
    DEFAULT_WIDTH = 400
    DEFAULT_HEIGHT = 300
    
    parser = argparse.ArgumentParser(description='Window size.')
    parser.add_argument('-w','--width', type=int, default=DEFAULT_WIDTH, help="Takes an integer value for the width of the game.")
    parser.add_argument('-e','--height', type=int, default=DEFAULT_HEIGHT, help="Takes an integer value for the height of the game.")
    args = parser.parse_args()

    return args

def snake():
    # main function for the game

    # initialisation
    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode( (size.width, size.height) )
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

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
    
        screen.fill( (255, 255, 255) )

        pygame.display.update()

    pygame.quit()
    quit(0)