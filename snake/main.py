import pygame
import argparse

def windowsize():
    # using argparse to change the window size if wanted

    parser = argparse.ArgumentParser(description='Window size.')
    parser.add_argument('-w','--width', type=int, default=400, help="Takes an integer value for the width of the game.")
    parser.add_argument('-e','--height', type=int, default=300, help="Takes an integer value for the height of the game.")
    args = parser.parse_args()

    return args

def snake():
    # main function for the game

    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode( (size.width, size.height) )
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

    while True:
        clock.tick(10)

        for event in pygame.event.get():
            pass
    
        screen.fill( (255, 255, 255) )

        pygame.display.update()

    pygame.quit()