# import the pygame module, so you can use it
import pygame, time, game, utilities, os
from game import Game

os.environ['SDL_VIDEO_CENTERED'] = '1'
block = None
command = 0

# define a main function
def main():

    option = utilities.chooseAlg()
    allLevels = utilities.parseFile()
    level = int(utilities.chooseLevel())
    
    pygame.board = allLevels[level-1]
    game = Game(pygame.board, option)

    tilePositions = []

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

    def get_tiles_coords():
        r = 0
        for row in pygame.board:
            rowArray = []
            c = 0
            for col in row:
                rowArray.append((colours[col],60+c*TileSize,60+r*TileSize,180+c*TileSize,60+r*TileSize,60+c*TileSize,180+r*TileSize,180+c*TileSize,180+r*TileSize))
                c+=1
            r+=1
            tilePositions.append(rowArray)

    def draw_game(screen):
        for row in tilePositions:
            for col in row:
                pygame.draw.rect(screen, col[0], (col[1],col[2],TileSize,TileSize))

    def updateAlg(n):
        pygame.board = game.updateAlg(n)
    
    def updatePlayer(block, opt):
        pygame.board = game.updatePlayer(block, opt)

    def get_tile_index(mx, my):
        r = 0
        for row in tilePositions:
            c = 0
            for col in row:
                if(mx >= col[1] and mx <= col[3] and my >= col[2] and my <= col[6]):
                    return (r,c)
                c+=1
            r+=1

    if(option == 0):
        running = True
        get_tiles_coords()

        while running:
            tx = -1
            ty = -1
            global block, command

            for event in pygame.event.get():
                if (event.type == pygame.QUIT or event.type == pygame.K_ESCAPE):
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    tx, ty = get_tile_index(mx, my)

                if(tx != -1 and ty != -1):
                    block = game.getBlock([tx,ty])

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_UP:
                        command = 1

                    elif event.key == pygame.K_DOWN:
                        command = 2

                    elif event.key == pygame.K_RIGHT:
                        command = 3

                    elif event.key == pygame.K_LEFT:
                        command = 4

            screen.fill(BACKGROUND)

            updatePlayer(block, command)

            get_tiles_coords()
            
            command = 0
            
            draw_game(screen)
            pygame.display.update()

            if game.checkWin(): break        
        
        time.sleep(1)         

    if option != 0:

        # define a variable to control the main loop
        running = True
        get_tiles_coords()

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
            updateAlg(walking)
            get_tiles_coords()
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
