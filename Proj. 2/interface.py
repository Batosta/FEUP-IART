# # import the pygame module, so you can use it
import pygame, time, game, utilities, os, sys
from game import Game

os.environ['SDL_VIDEO_CENTERED'] = '1'
block = None
command = 0


# # define a main function
def main():

    option = utilities.chooseGameMode()

    game = Game()

    circlePositions = []

    BLACK = (0, 0, 0)
    GREY = (200, 200, 200)
    RED = (255,0,0)
    BLUE = (0, 0, 255)
    WHITE = (255,255,255)

    # initialize the pygame module
    pygame.init()

    SQUARESIZE = 100
    width = 800
    height = 600
    size = (width, height)
     # load and set the logo
    pygame.display.set_caption("Nine Men's Morris")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(size)

    # TileSize = 120

    def draw_game():
        screen.fill(GREY)
        draw_lines()
        draw_circles()
        writeGameInfo()

    def draw_lines():
        for i in range(3):
            for k in range(4):
                a = 50 + (75*i)
                b = 550 - (75*i)
                pygame.draw.line(screen, BLACK, (a, a), (a, b))
                pygame.draw.line(screen, BLACK, (a, a), (b, a))
                pygame.draw.line(screen, BLACK, (b, a), (b, b))
                pygame.draw.line(screen, BLACK, (a, b), (b, b))

        pygame.draw.line(screen, BLACK, (300, 50), (300, 200))
        pygame.draw.line(screen, BLACK, (50, 300), (200, 300))
        pygame.draw.line(screen, BLACK, (300, 550), (300, 400))
        pygame.draw.line(screen, BLACK, (550, 300), (400, 300))

    def draw_circle(a, b):
        index, ring = get_circle_index(a, b)
        if game.selecti(index, ring).getValue() == 0:
            pygame.draw.circle(screen, BLACK, (a, b), 5)
        elif game.selecti(index, ring).getValue() == 1:
            pygame.draw.circle(screen, BLACK, (a, b), 20)
        else:
            pygame.draw.circle(screen, WHITE, (a, b), 20)

    def draw_circles():
        for i in range(3):
            a = 50 + (75*i)
            b = 550 - (75*i)
            draw_circle(a, a)
            draw_circle(300, a)
            draw_circle(b, a)
            draw_circle(a, b)
            draw_circle(300, b)
            draw_circle(b, b)
            draw_circle(a, 300)
            draw_circle(a, b)
            draw_circle(b, 300)

    def writeGameInfo():
        writeText("Black Pieces: ", BLACK, 600, 100)
        writeText(str(game.getPiecesOffBoard(1)), BLACK, 750, 100)
        writeText("White Pieces:", BLACK, 600, 150)
        writeText(str(game.getPiecesOffBoard(2)), BLACK, 750, 150)

    def writeText(message, color, px, py):
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        label = myfont.render(message, 1, color)
        screen.blit(label, (px, py))

    def create_circle_coords():
        for i in range(3):
            a = 50 + (i*75)
            b = 550 - (i*75)
            newRing = [(a,a), (300,a), (b,a), (b,300), (b,b), (300,b), (a,b), (a,300)]
            circlePositions.append(newRing)

    def get_circle_index(mx, my):
        r = 0
        for ring in circlePositions:
            c = 0
            for order in ring:
                if mx >= (order[0] - 25) and mx <= (order[0] + 25) and my >= (order[1] - 25) and my <= (order[1] + 25):
                    return (c, r)
                c+=1
            r+=1
        return (-1, -1)

    def play(ring, index):
        place(ring, index)

    def place(ring, index):
        game.place(index, ring)

    running = True
    if(option == 0):
        create_circle_coords()

        while running:
            tx = -1
            ty = -1
            # global block, command

            for event in pygame.event.get():
                
                draw_game()
                pygame.display.update()
                
                if (event.type == pygame.QUIT or event.type == pygame.K_ESCAPE):
                    running = False
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    index, ring = get_circle_index(mx, my)
                    if index != -1:
                        play(ring, index)
                        


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
