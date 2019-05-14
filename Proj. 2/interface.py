# # import the pygame module, so you can use it
import pygame, time, game, utilities, os, sys
from game import Board

os.environ['SDL_VIDEO_CENTERED'] = '1'
block = None
command = 0


# # define a main function
def main():

    option = utilities.chooseGameMode()

    game = Board()

    circlePositions = []

    BACKGROUND = (0, 0, 0)
    RED = (255,0,0)
    BLUE = (0, 0, 255)
    WHITE = (255,255,255)

    # initialize the pygame module
    pygame.init()

    SQUARESIZE = 100
    width = 600
    height = 600
    size = (width, height)
     # load and set the logo
    pygame.display.set_caption("Nine Men's Morris")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(size)

    # TileSize = 120

    def draw_game():
        screen.fill(BACKGROUND)
        draw_lines()
        draw_circles()


    def draw_lines():
        for i in range(3):
            for k in range(4):
                a = 50 + (75*i)
                b = 550 - (75*i)
                pygame.draw.line(screen, WHITE, (a, a), (a, b))
                pygame.draw.line(screen, WHITE, (a, a), (b, a))
                pygame.draw.line(screen, WHITE, (b, a), (b, b))
                pygame.draw.line(screen, WHITE, (a, b), (b, b))

        pygame.draw.line(screen, WHITE, (300, 50), (300, 200))
        pygame.draw.line(screen, WHITE, (50, 300), (200, 300))
        pygame.draw.line(screen, WHITE, (300, 550), (300, 400))
        pygame.draw.line(screen, WHITE, (550, 300), (400, 300))

    def draw_circles():
        for i in range(3):
            a = 50 + (75*i)
            b = 550 - (75*i)
            pygame.draw.circle(screen, WHITE, (a, a), 5)
            pygame.draw.circle(screen, WHITE, (300, a), 5)
            pygame.draw.circle(screen, WHITE, (b, a), 5)
            pygame.draw.circle(screen, WHITE, (a, b), 5)
            pygame.draw.circle(screen, WHITE, (300, b), 5)
            pygame.draw.circle(screen, WHITE, (b, b), 5)
            pygame.draw.circle(screen, WHITE, (a, 300), 5)
            pygame.draw.circle(screen, WHITE, (a, b), 5)
            pygame.draw.circle(screen, WHITE, (b, 300), 5)

    def create_circle_coords():
        for i in range(3):
            a = 50 + (i*75)
            b = 550 - (i*75)
            newRing = [(a,a), (300,a), (b,a), (b,300), (b,b), (300,b), (a,b), (a,300)]
            circlePositions.append(newRing)


#     def updateAlg(n):
#         pygame.board = game.updateAlg(n)

#     def updatePlayer(block, opt):
#         pygame.board = game.updatePlayer(block, opt)

    def get_circle_index(mx, my):
        r = 0
        for ring in circlePositions:
            c = 0
            for order in ring:
                if mx >= (order[0] - 25) and mx <= (order[0] + 25) and my >= (order[1] - 25) and my <= (order[1] + 25):
                    return (r, c)
                c+=1
            r+=1
        return (-1, -1)

    running = True
    if(option == 0):
        create_circle_coords()

        while running:
            tx = -1
            ty = -1
            # global block, command
            draw_game()
            pygame.display.update()

            for event in pygame.event.get():
                if (event.type == pygame.QUIT or event.type == pygame.K_ESCAPE):
                    running = False
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    tx, ty = get_circle_index(mx, my)
                    print(tx, end=",")
                    print(ty)

                # if not tx == -1:
                #     print("peça")

        #         if event.type == pygame.KEYUP:

        #             if event.key == pygame.K_UP:
        #                 command = 1

        #             elif event.key == pygame.K_DOWN:
        #                 command = 2

        #             elif event.key == pygame.K_RIGHT:
        #                 command = 3

        #             elif event.key == pygame.K_LEFT:
        #                 command = 4

        #     screen.fill(BACKGROUND)

        #     updatePlayer(block, command)

        #     try:
        #         block = game.getBlock(block.pieces[0].coords)
        #     except:
        #         pass

        #     get_tiles_coords()

        #     command = 0

        #     draw_game(screen)
        #     pygame.display.update()

        #     if game.checkWin(): break

        # time.sleep(1)

    # if option != 0:

        # # define a variable to control the main loop
        # get_tiles_coords()

        # walking = 0
        # # main loop
        # while running:

        #     # event handling, gets all event from the event queue
        #     for event in pygame.event.get():
        #         # only do something if the event is of type QUIT
        #         if event.type == pygame.QUIT:
        #             # change the value to False, to exit the main loop
        #             running = False

        #     screen.fill(BACKGROUND)
        #     updateAlg(walking)
        #     get_tiles_coords()
        #     draw_game(screen)
        #     pygame.display.update()
        #     walking += 1
        #     if(walking == len(game.solution)):
        #         running = False
        #     time.sleep(0.75)
        # time.sleep(2)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
