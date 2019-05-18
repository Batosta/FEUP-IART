import utilities
from intersection import Intersection

class Game:

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
                if self.selecti(pos, r) != intersection:
                    return False
            return True
        elif p in [3,7]:
            return self.selecti(p, 2) == self.selecti(p, 1) and self.selecti(p, 1) == self.selecti(p, 0)
        elif p in [4,5,6]:
            for pos in [4,5,6]:
                if self.selecti(pos, r) != intersection:
                    return False
            return True
        return False

    def checkVertical(self, intersection):
        p = intersection.getPos()
        r = intersection.getRing()
        if p in [0,7,6]:
            for pos in [0,7,6]:
                if self.selecti(pos, r) != intersection:
                    return False
            return True
        elif p in [1,5]:
            return self.selecti(p, 2) == self.selecti(p, 1) and self.selecti(p, 1) == self.selecti(p, 0)
        elif p in [2,3,4]:
            for pos in [2,3,4]:
                if self.selecti(pos, r) != intersection:
                    return False
            return True
        return False

    def selecti(self, pos, ring):
        i = pos + ring * 8
        return self.intersections[i]

    def selectIntersection(self, pos, ring, intersections):
        i = pos + ring * 8
        return intersections[i]

    def remove(self, ring, index):
        #print("Choose a piece from your adversary to remove.")
        self.changePlayer()
        i = self.selecti(index, ring)
        #if i.getValue() == self.player or i.getValue() == 0:
        #    print("Choose a valid piece")
        #    self.remove(ring, index)
        #else:
        i.set(0)
        # utilities.printMap(self.intersections)       

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
    
    def canmove(self, pos, ring, pos2, ring2):
        return [pos2, ring2] in self.playerMoves(self.player) and [pos2, ring2] in self.selecti(pos, ring).getConnections()

    def move(self, pos, ring, pos2, ring2):
        if self.canmove(pos, ring, pos2, ring2) or self.countPieces(self.player) == 3:
            intersection = self.selecti(pos, ring)
            intersection2 = self.selecti(pos2, ring2)
            intersection2.set(intersection.getValue())
            intersection.set(0)
            if self.check3row(intersection2):
                return 2
            self.checkWin()
            self.changePlayer()
            return 1
        else:
            return 0

    def place(self, pos, ring):
        intersection = self.selecti(pos, ring)
        if intersection.getValue() == 0:
            intersection.set(self.player)
            self.takePiece()
            # utilities.printMap(self.intersections)
            if self.check3row(intersection):
                #self.remove()
                return 1
            print(self.possibleMills(self.intersections))
            self.changePlayer()
            return 0
        else:
            print("Choose an empty intersection")
            return 0

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

        
    def pieceMoves(self, pos, ring):
        intersection = self.selecti(pos, ring)
        moves = []
        for connection in intersection.getConnections():
            intersectionMove = self.selecti(connection[0], connection[1])
            if intersectionMove.getValue() == 0:
                moves.append(intersectionMove.getCoords())
        return moves
    
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

    def getPiecesOffBoard(self, color):
        if(color == 1):
            return self.player1PiecesOffBoard
        else:
            return self.player2PiecesOffBoard

    def isPieceBlocked(self, pos, ring, intersections):
        intersection = self.selectIntersection(pos, ring, intersections)
        for connection in intersection.getConnections():
            if self.selectIntersection(connection[0], connection[1], intersections).getValue() == 0:
                return False
        return True
    def getNumberOfPieces(self, player):
        counter = 0
        for intersection in self.intersections:
            if intersection.getValue() == player:
                counter += 1
        return counter

    def possibleMills(self, intersections):
        possibelMills = 0
        possibelMills += self.checkVerticalPossible(intersections)
        possibelMills += self.checkHorizontalPossible(intersections)
        return possibelMills

    def checkHorizontalPossible(self, intersections):
        possible = 0

        for ring in [0, 1, 2]:
            numberOfEmpty = 0
            for pos in [0, 1, 2]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer():
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

            numberOfEmpty = 0
            for pos in [4, 5, 6]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer():
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1


                
        for pos in [3, 7]:
            numberOfEmpty = 0
            for ring in [0, 1, 2]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer():
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

        return possible
    
    def checkVerticalPossible(self, intersections):
        possible = 0

        for ring in [0, 1, 2]:
            numberOfEmpty = 0
            for pos in [0, 7, 6]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer():
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

            numberOfEmpty = 0
            for pos in [2, 3, 4]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer():
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1


                
        for pos in [1, 5]:
            numberOfEmpty = 0
            for ring in [0, 1, 2]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer():
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

        return possible
        

    def canBeMove(self, intersection, intersections):
        for connection in intersection.getConnections():
            if self.selectIntersection(connection[0], connection[1], intersections).getValue() == self.player:
                return True
        return False


    def heuristic(self, intersections):
        value = 0
        for intersection in intersections:
            if intersection.getValue() != 0:
                pass

    def heuristic(self, phase):
        return 1

    """
    No caso de phase 1 ou 4, retorna as posições onde se podem colocar peças e que peças pode remover respetivamente
    No caso de phase 2 ou 3 retorna as peças que podem ser jogadas
    """
    def get_valid_locations(self, phase):
        positions = []
        #Colocar peças
        if phase == 1 or phase == 3:
            for position in self.intersections:
                if position.value == 0:
                    positions.append((position.pos, position.ring))
            return positions
        #Mover peças
        if phase == 2:
            return self.playerMoves(self.player)
        #Remover peça do outro jogador
        if phase == 4:
            for position in self.intersections:
                if position.value != self.player and position.value != 0:
                    positions.append((position.pos, position.ring))
            return positions

    def minimax(self, depth, alpha, beta, maximizingPlayer, phase):

        #colocar peças
        if (depth == 0 or self.checkWin()):
            return None, None, self.heuristic(phase)
        
        valid_locations = self.get_valid_locations(phase)
    
        if maximizingPlayer:

            value = -math.inf
            children = self.children(phase)
            index, ring = random.choice(valid_locations)

            for child in children:

                intersection = self.selecti(index, ring)

                if self.check3row(intersection):
                    phase = 4 #remove
                elif self.player1PiecesOffBoard == 0 and self.player2PiecesOffBoard == 0:
                    if self.countPieces(self.player) == 3:
                        phase = 3
                    phase = 2
                else:
                    phase = 1

                new_score = minimax(child[0], depth - 1, alpha, beta, False, phase)

                if new_score[2] > value:
                    value = new_score[2]
                    index = child[2]
                    ring = child[1]

                alpha = max(alpha, value)
                
                if beta <= alpha:
                    break

            return index, ring, value

        else:

            value = math.inf
            children = self.children(phase)
            index, ring = random.choice(valid_locations)

            for child in children:

                intersection = self.selecti(index, ring)

                if self.check3row(intersection):
                    phase = 4 #remove
                elif self.player1PiecesOffBoard == 0 and self.player2PiecesOffBoard == 0:
                    if self.countPieces(self.player) == 3:
                        phase = 3
                    phase = 2
                else:
                    phase = 1

                new_score = minimax(child[0], depth - 1, alpha, beta, True, phrase)

                if new_score[2] < value:
                    value = new_score[2]
                    index = child[2]
                    ring = child[1]
                
                beta = min(beta, value)
                
                if beta <= alpha:
                    break
            
            return index, ring, value