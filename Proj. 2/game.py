import utilities
from intersection import Intersection

class Board:

    position = {'outer' : 0, 'middle' : 8, 'inner' : 16}

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
        utilities.printMap(self.intersections)
        self.play()

    
    def play(self):
        while True:
            if self.player1PiecesOffBoard == 0 and self.player2PiecesOffBoard == 0:
                self.move()
            else:
                self.place()

    def createBoard(self):
        self.createRing("outer")
        self.createMiddleRing()
        self.createRing("inner")
    def createRing(self, ring):
        self.intersections.append(Intersection(0, ring, [[1,ring],[7,ring]]))
        self.intersections.append(Intersection(1, ring, [[0,ring],[2,ring],[1,"middle"]]))
        self.intersections.append(Intersection(2, ring, [[1,ring],[3,ring]]))
        self.intersections.append(Intersection(3, ring, [[2,ring],[4,ring],[3,"middle"]]))
        self.intersections.append(Intersection(4, ring, [[3,ring],[5,ring]]))
        self.intersections.append(Intersection(5, ring, [[4,ring],[6,ring],[5,"middle"]]))
        self.intersections.append(Intersection(6, ring, [[5,ring],[7,ring]]))
        self.intersections.append(Intersection(7, ring, [[0,ring],[6,ring],[7,"middle"]]))
    def createMiddleRing(self):
        self.intersections.append(Intersection(0, "middle", [[1,"middle"],[7,"middle"]]))
        self.intersections.append(Intersection(1, "middle", [[0,"middle"],[2,"middle"],[1,"outer"],[1,"inner"]]))
        self.intersections.append(Intersection(2, "middle", [[1,"middle"],[3,"middle"]]))
        self.intersections.append(Intersection(3, "middle", [[2,"middle"],[4,"middle"],[3,"outer"],[3,"inner"]]))
        self.intersections.append(Intersection(4, "middle", [[3,"middle"],[5,"middle"]]))
        self.intersections.append(Intersection(5, "middle", [[4,"middle"],[6,"middle"],[5,"outer"],[5,"inner"]]))
        self.intersections.append(Intersection(6, "middle", [[5,"middle"],[7,"middle"]]))
        self.intersections.append(Intersection(7, "middle", [[0,"middle"],[6,"middle"],[7,"outer"],[7,"inner"]]))


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
            return self.selecti(p, 'inner') == self.selecti(p, 'middle') and self.selecti(p, 'middle') == self.selecti(p, 'outer')
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
            return self.selecti(p, 'inner') == self.selecti(p, 'middle') and self.selecti(p, 'middle') == self.selecti(p, 'outer')
        elif p in [2,3,4]:
            for pos in [2,3,4]:
                if self.selecti(pos,r) != intersection:
                    return False
            return True
        return False

    def selecti(self, pos, ring):
        i = self.position[ring] + pos
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
    
    def canmove(self, intersection, intersection2):
        return intersection.getValue() != 0 and intersection2.getValue() == 0 and ([intersection2.getPos(), intersection2.getRing()] in intersection.getConnections())

    def move(self):
        while True:
            intersection = self.choosePiece()
            intersection2 = self.chooseIntersection()
            if self.canmove(intersection, intersection2):
                intersection2.set(intersection.getValue())
                intersection.set(0)
                if self.check3row(intersection2):
                    self.remove()
                self.checkWin()
                self.changePlayer()
            else:
                print("Illegal move\n")

    def place(self):
        intersection = self.chooseIntersection()            
        intersection.set(self.player)
        self.takePiece()
        utilities.printMap(self.intersections)
        if self.check3row(intersection):
            self.remove()
        self.changePlayer()

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

    def playerPlacements(self, player):
        placements = []
        for intersection in self.intersections:
            if (intersection.getValue() == 0):
                placements.append([intersection.getPos(), intersection.getRing()])
        return placements

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

game = Board()