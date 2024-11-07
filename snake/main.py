import pygame
import argparse

def windowsize(WIDTH,HEIGHT):
    # using argparse to change the window size if wanted

    parser = argparse.ArgumentParser(description='Window size.')
    parser.add_argument('-w','--width', type=int, default=WIDTH, help="Takes an integer value for the width of the game.")
    parser.add_argument('-e','--height', type=int, default=HEIGHT, help="Takes an integer value for the height of the game.")
    args = parser.parse_args()

    return args

def snake():
    # main function for the game

    WIDTH = 400
    HEIGHT = 300

    size = windowsize(WIDTH,HEIGHT)
    pygame.init()
    screen = pygame.display.set_mode( (size.width, size.height) )
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

    while True:
        clock.tick(10)

        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit(0)
    
        screen.fill( (255, 255, 255) )

        pygame.display.update()