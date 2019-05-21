# # import the pygame module, so you can use it
import pygame, time, game, utilities, os, sys, math
from game import Game

os.environ['SDL_VIDEO_CENTERED'] = '1'
block = None
command = 0


# # define a main function
def main():

    option = utilities.chooseGameMode()

    game = Game()

    # Useful variables for the game drawing
    circlePositions = []
    BLACK = (0, 0, 0)
    GREY = (200, 200, 200)
    RED = (255, 0, 0)
    WHITE = (255,255,255)

    # initialize the pygame module
    pygame.init()

    SQUARESIZE = 100
    width = 850
    height = 600
    size = (width, height)
     # load and set the logo
    pygame.display.set_caption("Nine Men's Morris")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(size)


    def draw_game(option):
        screen.fill(GREY)
        draw_lines()
        draw_circles()
        writeGameInfo(option)

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

    def writeGameInfo(option):
        writeText("Black Pieces: ", BLACK, 600, 100)
        writeText(str(game.getPiecesOffBoard(1)), BLACK, 750, 100)
        writeText("White Pieces:", BLACK, 600, 150)
        writeText(str(game.getPiecesOffBoard(2)), BLACK, 750, 150)
        if option == 1:
            if game.player == 1:
                writeText("PLACE A BLACK PIECE", RED, 600, 300)
            else:
                writeText("PLACE A WHITE PIECE", RED, 600, 300)
        elif option == 2:
            if game.player == 1:
                writeText("MOVE A BLACK PIECE", RED, 600, 300)
            else:
                writeText("MOVE A WHITE PIECE", RED, 600, 300)
        elif option == 3:
            if game.player == 1:
                writeText("REMOVE A WHITE PIECE", RED, 600, 300)
            else:
                writeText("REMOVE A BLACK PIECE", RED, 600, 300)


    def draw_game_result(winner):
        if winner == 1:     # black wins
            screen.fill(WHITE)
            writeText("BLACK WINS", BLACK, 200, 250, 100)
        else:
            screen.fill(BLACK)
            writeText("WHITE WINS", WHITE, 200, 250, 100)

    def writeText(message, color, px, py, size = 30):
        myfont = pygame.font.SysFont("Comic Sans MS", size)
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

    def AiVsAi():
        
        running = 0

        while running == 0:

            game.minimax(depth, alpha, beta, maximizingPlayer, phase)

        return running

    def humanVsHuman():

        running = 0

        placing_phase = 0
        moving_phase = 0
        can_remove = 0
        is_moving = 0
        movingIndex = -1
        movingRing = -1

        while running == 0:

            running, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing = humanPlay(placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing)
        
        return running

    def humanVsAi():
        
        running = 0

        placing_phase = 0
        moving_phase = 0
        can_remove = 0
        is_moving = 0
        movingIndex = -1
        movingRing = -1

        while running == 0:
            if game.player == 1:
                running, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing = humanPlay(placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing)
            else:
                running, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing = AiPlay(placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing)

        return running


    def AiPlay(placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing):

        # Placing pieces phase
        while placing_phase != 18 or can_remove == 1:

            for event in pygame.event.get():
            
                if (event.type == pygame.QUIT or event.type == pygame.K_ESCAPE):
                    self.running = False
                    sys.exit()
                
                if can_remove == 1:                             # remove a piece
                    
                    #returns value, index, ring
                    minimax_values = game.minimax(1, -math.inf, math.inf, True, 4)

                    index = minimax_values[1]
                    ring = minimax_values[2]

                    game.remove(ring, index)
                    can_remove = 0
                    if placing_phase != 18:
                        game.changePlayer()
                        draw_game(1)
                        return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                    else:
                        checkWin = game.checkWin()
                        game.changePlayer()
                        draw_game(2)
                        return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing

                else:                                           # place a piece

                    minimax_values = game.minimax(1, -math.inf, math.inf, True, 1)

                    index = minimax_values[1]
                    ring = minimax_values[2]

                    can_remove = game.place(index, ring)
                    placing_phase += 1
                    if can_remove == 1:
                        draw_game(3)
                        return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                    elif placing_phase == 18:
                        checkWin = game.checkWin()
                        game.changePlayer()
                        draw_game(2)
                        return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                    else:
                        game.changePlayer()
                        draw_game(1)
                        return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing

                pygame.display.update()


        # Moving pieces phase
        while moving_phase != 1:

            for event in pygame.event.get():

                if (event.type == pygame.QUIT or event.type == pygame.K_ESCAPE):
                    running = False
                    sys.exit()
                
                if can_remove == 1:                             # remove a piece
                    #returns value, index, ring
                    minimax_values = game.minimax(1, -math.inf, math.inf, True, 4)

                    index = minimax_values[1]
                    ring = minimax_values[2]
    
                    value = game.selecti(index, ring).getValue()
                    if value != game.player and value != 0:
                        game.remove(ring, index)
                        can_remove = 0
                        checkWin = game.checkWin()
                        game.changePlayer()
                        draw_game(2)
                        return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing

                elif is_moving == 0:                            # choose a piece to move
                    #returns value, index, ring
                    if game.countPieces(game.player) == 3:
                        minimax_values = game.minimax(1, -math.inf, math.inf, True, 3)
                    else:
                        minimax_values = game.minimax(1, -math.inf, math.inf, True, 2)

                    index = minimax_values[1]
                    ring = minimax_values[2]
                    index_to = minimax_values[3]
                    ring_to = minimax_values[4]

                    if game.countPieces(game.player) == 3 or len(game.pieceMoves(index, ring)) != 0:
                        movingResult = game.move(index, ring, index_to, ring_to)
                        if movingResult != 0:
                            movingIndex = -1
                            movingRing = -1
                            if movingResult == 2:
                                can_remove = 1
                                draw_game(3)
                                return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                            else:
                                checkWin = game.checkWin()
                                game.changePlayer()
                                draw_game(2)
                                return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                pygame.display.update()

    def humanPlay(placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing):
        # Placing pieces phase
        while placing_phase != 18 or can_remove == 1:

            for event in pygame.event.get():

                print(game.minimax(1,-math.inf, math.inf,True,1))
            
                if (event.type == pygame.QUIT or event.type == pygame.K_ESCAPE):
                    self.running = False
                    sys.exit()
                
                if can_remove == 1:                             # remove a piece
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        index, ring = get_circle_index(mx, my)
                        if index != -1:
                            value = game.selecti(index, ring).getValue()
                            if value == game.getNextPlayer(game.player):
                                game.remove(ring, index)
                                can_remove = 0
                                if placing_phase != 18:
                                    game.changePlayer()
                                    draw_game(1)
                                    return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                                else:
                                    checkWin = game.checkWin()
                                    game.changePlayer()
                                    draw_game(2)
                                    return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                else:                                           # place a piece
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        index, ring = get_circle_index(mx, my)
                        if index != -1:
                            value = game.selecti(index, ring).getValue()
                            if value == 0:
                                can_remove = game.place(index, ring)
                                placing_phase += 1
                                if can_remove == 1:
                                    draw_game(3)
                                    return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                                elif placing_phase == 18:
                                    checkWin = game.checkWin()
                                    game.changePlayer()
                                    draw_game(2)
                                    return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                                else:
                                    game.changePlayer()
                                    draw_game(1)
                                    return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing

                pygame.display.update()


        # Moving pieces phase
        while moving_phase != 1:

            for event in pygame.event.get():

                if (event.type == pygame.QUIT or event.type == pygame.K_ESCAPE):
                    running = False
                    sys.exit()
                
                if can_remove == 1:                             # remove a piece
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        index, ring = get_circle_index(mx, my)
                        if index != -1:
                            value = game.selecti(index, ring).getValue()
                            if value != game.player and value != 0:
                                game.remove(ring, index)
                                can_remove = 0
                                checkWin = game.checkWin()
                                game.changePlayer()
                                draw_game(2)
                                return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing

                elif is_moving == 0:                            # choose a piece to move
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        index, ring = get_circle_index(mx, my)
                        if index != -1:
                            value = game.selecti(index, ring).getValue()
                            if value == game.player:
                                if game.countPieces(game.player) == 3 or len(game.pieceMoves(index, ring)) != 0:
                                    is_moving = 1
                                    movingIndex = index
                                    movingRing = ring
                                    return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing

                else:                                           # choose where to move the piece
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        index, ring = get_circle_index(mx, my)
                        if index != -1:
                            value = game.selecti(index, ring).getValue()
                            if value == 0:
                                movingResult = game.move(movingIndex, movingRing, index, ring)
                                if movingResult != 0:
                                    is_moving = 0
                                    movingIndex = -1
                                    movingRing = -1
                                    if movingResult == 2:
                                        can_remove = 1
                                        draw_game(3)
                                        return 0, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                                    else:
                                        checkWin = game.checkWin()
                                        game.changePlayer()
                                        draw_game(2)
                                        return checkWin, placing_phase, moving_phase, can_remove, is_moving, movingIndex, movingRing
                pygame.display.update()

    def startGame():
        create_circle_coords()
        draw_game(1)
        pygame.display.update()

    def endGame(winner):
        draw_game_result(winner)
        pygame.display.update()
        time.sleep(5)
        sys.exit()

    startGame()

    if option == 0:
        running = humanVsHuman()
    elif option == 1:
        running = humanVsAi()
    else:
        running = AiVsAi()

    endGame(running)



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
