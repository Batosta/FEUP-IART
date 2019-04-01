# import the pygame module, so you can use it
import pygame
import time
import game
import utilities
from game import Game
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# define a main function
def main():

    # Para escolher o algoritmo a ser usado:
    # self.algorithm = utilities.chooseAlg()
    allLevels = utilities.parseFile()
    pygame.board = allLevels[0]
    game = Game(pygame.board)

    BACKGROUND = (0, 0, 0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0, 0, 255)
    ORANGE = (62 , 124, 124)

    colours = {
        '0': WHITE,
        '1': RED,
        '2': GREEN,
        '3': BLUE,
        '4': ORANGE
    }
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("minimal program")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((600,600))

    TileSize = 120



    def draw_game(screen):
        r = 0
        for row in pygame.board:
            c = 0
            for col in row:
                pygame.draw.rect(screen, colours[col], (60+c*TileSize,60+r*TileSize,TileSize,TileSize))
                c += 1
            r += 1

    def update(n):
        pygame.board = game.update(n)

    # define a variable to control the main loop
    running = True

    walking = 0
    # main loop
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        screen.fill(BACKGROUND)
        update(walking)
        draw_game(screen)
        pygame.display.update()
        walking += 1
        if(walking == len(game.solution)):
            running = False
        time.sleep(0.2)


    time.sleep(2)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
