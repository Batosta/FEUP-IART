import utilities
from intersection import Intersection

class Board:

    def __init__(self):
        self.player = 1
        self.player1PiecesOffBoard = 9
        self.player2PiecesOffBoard = 9
        self.intersections = []

        #ring configuration:
        # 0----1----2
        # |         |
        # 7-       -3
        # |         |
        # 6----5----4 

        self.createBoard()
        # utilities.printMap(self.intersections)
        # self.play()

    
    def play(self):
        while True:
            if self.player1PiecesOffBoard == 0 and self.player2PiecesOffBoard == 0:
                self.move()
            else:
                self.place()

    def createBoard(self):
        self.createRing(0)
        self.createMiddleRing()
        self.createRing(2)
    def createRing(self, ring):
        self.intersections.append(Intersection(0, ring, [[1,ring],[7,ring]]))
        self.intersections.append(Intersection(1, ring, [[0,ring],[2,ring],[1,1]]))
        self.intersections.append(Intersection(2, ring, [[1,ring],[3,ring]]))
        self.intersections.append(Intersection(3, ring, [[2,ring],[4,ring],[3,1]]))
        self.intersections.append(Intersection(4, ring, [[3,ring],[5,ring]]))
        self.intersections.append(Intersection(5, ring, [[4,ring],[6,ring],[5,1]]))
        self.intersections.append(Intersection(6, ring, [[5,ring],[7,ring]]))
        self.intersections.append(Intersection(7, ring, [[0,ring],[6,ring],[7,1]]))
    def createMiddleRing(self):
        self.intersections.append(Intersection(0, 1, [[1,1],[7,1]]))
        self.intersections.append(Intersection(1, 1, [[0,1],[2,1],[1,0],[1,2]]))
        self.intersections.append(Intersection(2, 1, [[1,1],[3,1]]))
        self.intersections.append(Intersection(3, 1, [[2,1],[4,1],[3,0],[3,2]]))
        self.intersections.append(Intersection(4, 1, [[3,1],[5,1]]))
        self.intersections.append(Intersection(5, 1, [[4,1],[6,1],[5,0],[5,2]]))
        self.intersections.append(Intersection(6, 1, [[5,1],[7,1]]))
        self.intersections.append(Intersection(7, 1, [[0,1],[6,1],[7,0],[7,2]]))


    def check3row(self, inter):
        return self.checkHorizontal(inter) or self.checkVertical(inter)

    def checkHorizontal(self, intersection):
        p = intersection.getPos()
        r = intersection.getRing()
        if p in [0,1,2]:
            for pos in [0,1,2]:
                if self.selecti(pos,r) != intersection:
                    return False
            return True
        elif p in [3,7]:
            return self.selecti(p, 2) == self.selecti(p, 1) and self.selecti(p, 1) == self.selecti(p, 0)
        elif p in [4,5,6]:
            for pos in [4,5,6]:
                if self.selecti(pos,r) != intersection:
                    return False
            return True
        return False

    def checkVertical(self, intersection):
        p = intersection.getPos()
        r = intersection.getRing()
        if p in [0,7,6]:
            for pos in [0,7,6]:
                if self.selecti(pos,r) != intersection:
                    return False
            return True
        elif p in [1,5]:
            return self.selecti(p, 2) == self.selecti(p, 1) and self.selecti(p, 1) == self.selecti(p, 0)
        elif p in [2,3,4]:
            for pos in [2,3,4]:
                if self.selecti(pos,r) != intersection:
                    return False
            return True
        return False

    def selecti(self, pos, ring):
        i = pos + ring * 8
        return self.intersections[i]

    def insertPiece(self, piece, pos, ring):
        intersection = self.selecti(pos,ring)
        intersection.set(piece)
        utilities.printMap(self.intersections)
        if self.check3row(intersection):
            self.remove()
            utilities.printMap(self.intersections)
        self.changePlayer()

    def remove(self):
        while True:
            print("Choose a piece from your adversary to remove.")
            pos = utilities.inputNumber()
            ring = utilities.inputRing()
            i = self.selecti(pos,ring)
            if i.getValue() == self.player or i.getValue() == 0:
                continue
            else:
                i.set(0)
                utilities.printMap(self.intersections)       
                break

    def resetBoard(self):
        for intersection in self.intersections:
            intersection.set(0)
            
    def changePlayer(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def countPieces(self, player):
        c = 0
        for intersection in self.intersections:
            if intersection.getValue() == player:
                c += 1
        return c
    
    def canmove(self, pos, ring):
        return [pos, ring] in self.playerMoves(self.player)

    def move(self, pos, ring, pos2, ring2):
        if self.canmove(pos2, ring2):
            intersection = self.selecti(pos, ring)
            intersection2 = self.selecti(pos2, ring2)
            intersection2.set(intersection.getValue())
            intersection.set(0)
            if self.check3row(intersection2):
                self.remove()
            self.checkWin()
            self.changePlayer()
        else:
            print("Illegal move\n")

    def place(self, pos, ring):
        intersection = self.selecti(pos, ring)
        if intersection.getValue() == 0:
            intersection.set(self.player)
            self.takePiece()
            utilities.printMap(self.intersections)
            if self.check3row(intersection):
                self.remove()
            self.changePlayer()
        else:
            print("Choose an empty intersection")

    def takePiece(self):
        if self.player == 1:
            self.player1PiecesOffBoard -= 1
        else:
            self.player2PiecesOffBoard -= 1

    def getNextPlayer(self):
        if self.player == 1:
            return 2
        else:
            return 1

    def checkWin(self):
        nextPlayer = self.getNextPlayer()
        if self.playerHasNoMoves(nextPlayer) or (self.countPieces(nextPlayer) <= 2):
            print('Player ', end='')
            print(self.player, end=' wins!\n')
            exit()
        
    
    def playerHasNoMoves(self, player):
        moves = self.playerMoves(self.player)
        if len(moves) == 0:
            return True
        else:
            return False

    def playerMoves(self, player):
        moves = []
        for intersection in self.intersections:
            if (intersection.getValue() == player):
                for connection in intersection.getConnections():
                    if self.selecti(connection[0], connection[1]).getValue() == 0:
                        moves.append(connection) 
        return moves

    def choosePiece(self):
        while True:
            pos = utilities.inputNumber()
            ring = utilities.inputRing()
            selected = self.selecti(pos, ring)
            if selected.getValue() == self.player:
                return selected
            print("Choose a piece you control!\n")

    def chooseIntersection(self):
        while True:
            pos = utilities.inputNumber()
            ring = utilities.inputRing()
            selected = self.selecti(pos, ring)
            if selected.getValue() == 0:
                return selected
            print("Choose an empty intersection!\n")

"""
def minimax(game, depth, alpha, beta, maximizingPlayer, agent):

    if (depth == 0 or game.winning_move(1) or game.winning_move(2)) and agent == 1:
        return None, None, Agente1(game)

    if (depth == 0 or game.winning_move(1) or game.winning_move(2)) and agent == 2:
        return None, None, Agente2(game)

    if (depth == 0 or game.winning_move(1) or game.winning_move(2)) and agent == 3:
        return None, None, Agente3(game)

    if (depth == 0 or game.winning_move(1) or game.winning_move(2)) and agent == 4:
        return None, None, Agente4(game)
        
    valid_locations = game.get_valid_locations()
    
    if maximizingPlayer:
        value = -math.inf
        children = game.children(1)

        column = random.choice(valid_locations)
        row = game.is_valid_position(column)

        for child in children:

            new_score = minimax(child[0], depth - 1, alpha, beta, False, agent)

            if new_score[2] > value:
                value = new_score[2]
                column = child[2]
                row = child[1]

            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return column, row, value

    else:
        value = math.inf
        children = game.children(2)

        column = random.choice(valid_locations)
        row = game.is_valid_position(column)

        for child in children:
            new_score = minimax(child[0], depth - 1, alpha, beta, True, agent)
            if new_score[2] < value:
                value = new_score[2]
                column = child[2]
                row = child[1]
            beta = min(beta, value)
            if beta <= alpha:
                break
        return column, row, value

"""

# game = Board()