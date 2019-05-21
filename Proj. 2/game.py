import utilities, copy, math, random
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
        i = self.selecti(index, ring)
        i.set(0)

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
            return 1
        else:
            return 0

    def place(self, pos, ring):
        intersection = self.selecti(pos, ring)
        intersection.set(self.player)
        self.takePiece()
        if self.check3row(intersection):
            return 1
        # print(self.possibleMills(self.intersections, self.player))
        return 0

    def takePiece(self):
        if self.player == 1:
            self.player1PiecesOffBoard -= 1
        else:
            self.player2PiecesOffBoard -= 1

    def getNextPlayer(self, player):
        if player == 1:
            return 2
        else:
            return 1

    def checkWin(self):
        nextPlayer = self.getNextPlayer(self.player)
        if self.playerHasNoMoves(nextPlayer) or (self.countPieces(nextPlayer) <= 2):
            return self.player
        else:
            return 0

        
    def pieceMoves(self, pos, ring):
        intersection = self.selecti(pos, ring)
        moves = []
        for connection in intersection.getConnections():
            intersectionMove = self.selecti(connection[0], connection[1])
            if intersectionMove.getValue() == 0:
                moves.append(intersectionMove.getCoords())
        return moves
    
    def playerHasNoMoves(self, player):
        moves = self.playerMoves(player)
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

    def playerMoves_for_AI(self, player):
        moves = []
        for intersection in self.intersections:
            count = 0
            moves_aux = []
            if (intersection.getValue() == player):
                for connection in intersection.getConnections():
                    if self.selecti(connection[0], connection[1]).getValue() == 0:
                        moves_aux.append(connection)
                        count += 1
            if count != 0:
                positions = []
                positions.append(intersection.pos)
                positions.append(intersection.ring)
                moves.append((positions, moves_aux))
            moves_aux = []
             
        return moves

    def choosePiece(self):
        while True:
            pos = utilities.inputNumber()
            ring = utilities.inputRing()
            selected = self.selecti(pos, ring)
            if selected.getValue() == self.player:
                return selected

    def chooseIntersection(self):
        while True:
            pos = utilities.inputNumber()
            ring = utilities.inputRing()
            selected = self.selecti(pos, ring)
            if selected.getValue() == 0:
                return selected

    def getPiecesOffBoard(self, color):
        if(color == 1):
            return self.player1PiecesOffBoard
        else:
            return self.player2PiecesOffBoard

    def isPieceBlocked(self, pos, ring, intersections):
        intersection = self.selectIntersection(pos, ring, intersections)
        if self.countPieces(intersection.getValue()) == 3:
            return False
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

    def possibleMills(self, intersections, player):
        possibelMills = 0
        possibelMills += self.checkVerticalPossible(intersections, player)
        possibelMills += self.checkHorizontalPossible(intersections, player)
        return possibelMills

    def checkHorizontalPossible(self, intersections, player):
        possible = 0

        for ring in [0, 1, 2]:
            numberOfEmpty = 0
            for pos in [0, 1, 2]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer(player):
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections, player, [[0,ring], [1, ring], [2, ring]]):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

            numberOfEmpty = 0
            for pos in [4, 5, 6]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer(player):
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections, player, [[4,ring], [5, ring], [6, ring]]):
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
                if intersections[index].getValue() == self.getNextPlayer(player):
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections,  player, [[pos, 0], [pos, 1], [pos, 2]]):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

        return possible
    
    def checkVerticalPossible(self, intersections, player):
        possible = 0

        for ring in [0, 1, 2]:
            numberOfEmpty = 0
            for pos in [0, 7, 6]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer(player):
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections, player, [[0,ring], [7, ring], [6, ring]]):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

            numberOfEmpty = 0
            for pos in [2, 3, 4]:
                index = pos + 8 * ring
                if intersections[index].getValue() == self.getNextPlayer(player):
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections, player, [[2,ring], [3, ring], [4, ring]]):
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
                if intersections[index].getValue() == self.getNextPlayer(player):
                    numberOfEmpty = -1    
                    break
                elif intersections[index].getValue() == 0:
                    if self.canBeMove(intersections[index], intersections, player, [[pos, 0], [pos, 1], [pos, 2]]):
                        numberOfEmpty += 1
                        continue
                    numberOfEmpty = -1
                    break
            if numberOfEmpty == 1:
                possible += 1

        return possible
        

    def canBeMove(self, intersection, intersections, player, connections):
        for connection in intersection.getConnections():
            if self.selectIntersection(connection[0], connection[1], intersections).getValue() == player and connection not in connections:
                return True
        return False

    def getIntersectionValuePlace(self, intersection, intersections , player):
        value = 1
        if intersection.getPos() in [1,3,5,7]:
            value += 1
            if intersection.getRing() == 1:
                value += 2
        if self.isPieceBlocked(intersection.getPos(), intersection.getRing(), intersections):
            value -= 1
        if intersection.getValue() == player:
            return value
        return -value

    def getIntersectionValuePlace(self, intersection, intersections , player):
        value = 1
        if intersection.getPos() in [1,3,5,7]:
            value += 1
            if intersection.getRing() == 1:
                value += 2
        if self.isPieceBlocked(intersection.getPos(), intersection.getRing(), intersections):
            value -= 1
        if intersection.getValue() == player:
            return value
        return -value
    
    def getIntersectionValueMove(self, intersection, intersections , player):
        value = 1
        if intersection.getPos() in [1,3,5,7]:
            value += 1
            if intersection.getRing() == 1:
                value += 2
        if self.isPieceBlocked(intersection.getPos(), intersection.getRing(), intersections):
            value -= 3
        if intersection.getValue() == player:
            return value
        return -value

    def heuristicPhase1(self, intersections, player):
        value = 0
        for intersection in intersections:
            if intersection.getValue() != 0:
                value += self.getIntersectionValuePlace(intersection, intersections, player)
        value += (self.possibleMills(intersections, player) - self.possibleMills(intersections, self.getNextPlayer(player))) * 3
        return value

    def heuristicPhase2(self, intersections, player):
        value = 0
        for intersection in intersections:
            if intersection.getValue() != 0:
                value += self.getIntersectionValueMove(intersection, intersections, player)
        value += self.possibleMills(intersections, player) * 5 - self.possibleMills(intersections, self.getNextPlayer(player)) * 6
        return value
                

    def heuristic(self, phase, intersections, player):
        if phase == 1 or phase == 4:
            return self.heuristicPhase1(intersections, player)
        elif phase == 2 or phase == 3:
            return self.heuristicPhase2(intersections, player)

    """
    No caso de phase 1 ou 4, retorna as posições onde se podem colocar peças e que peças pode remover respetivamente
    No caso de phase 2 ou 3 retorna as peças que podem ser jogadas
    """
    def get_valid_locations(self, phase):
        positions = []
        #Colocar peças
        if phase == 1:
            for position in self.intersections:
                if position.value == 0:
                    positions.append((position.pos, position.ring))
            return positions
        #Mover peças
        if phase == 2:
            return self.playerMoves_for_AI(self.player)
        if phase == 3:
            empty_positions = []
            for empty_pos in self.intersections:
                if empty_pos.value == 0:
                    coords = []
                    coords.append(empty_pos.pos)
                    coords.append(empty_pos.ring)
                    empty_positions.append(coords)

            for empty_pos in self.intersections:
                if empty_pos.value == self.player:
                    coords = []
                    coords.append(empty_pos.pos)
                    coords.append(empty_pos.ring)
                    positions.append((coords, empty_positions))

            return positions
            

        #Remover peça do outro jogador
        if phase == 4:
            for position in self.intersections:
                if position.value != self.player and position.value != 0:
                    positions.append((position.pos, position.ring))
            return positions

    def children(self, phase):
        children = []

        if phase == 1:
            for intersection in self.intersections:
                if intersection.value == 0:
                    temporaryGame = copy.deepcopy(self)
                    temporaryGame.place(intersection.pos, intersection.ring)
                    children.append((temporaryGame, intersection.pos, intersection.ring))

        if phase == 2:
            moves = self.playerMoves_for_AI(phase)
            for move in moves:
                pos_to_move = move[0][0] 
                ring_to_move = move[0][1]
                for position in move[1]:
                    temporaryGame = copy.deepcopy(self)
                    temporaryGame.move(pos_to_move, ring_to_move, position[0], position[1])
                    children.append((temporaryGame, pos_to_move, ring_to_move, position[0], position[1]))

        if phase == 3:
            for intersection in self.intersections:
                if intersection.value == self.player:
                    for intersection_aux in self.intersections:
                        if intersection_aux.value == 0:
                            temporaryGame = copy.deepcopy(self)
                            temporaryGame.move(intersection.pos, intersection.ring, intersection_aux.pos, intersection_aux.ring)
                            children.append((temporaryGame, intersection.pos, intersection.ring, intersection_aux.pos, intersection_aux.ring))

        if phase == 4:
            for intersection in self.intersections:
                if intersection.value != 0 and intersection.value != self.player:
                    temporaryGame = copy.deepcopy(self)
                    temporaryGame.place(intersection.pos, intersection.ring)
                    children.append((temporaryGame, intersection.pos, intersection.ring))

        return children

    def minimax(self, depth, alpha, beta, maximizingPlayer, phase):
        if depth == 0 or self.checkWin() == 0:
            if phase == 2 or phase == 3:
                return self.heuristic(phase, self.intersections, self.player), None, None, None, None
            else:
                return self.heuristic(phase, self.intersections, self.player), None, None
    
        valid_locations = self.get_valid_locations(phase)    
        if maximizingPlayer:

            value = -math.inf
            children = self.children(phase)

            if phase != 2 and phase != 3:
                index, ring = random.choice(valid_locations)
            else:
                rand = random.choice(valid_locations)
                index, ring = random.choice(rand[1])
                index_to_move = rand[0][0]
                ring_to_move = rand[0][1]

            for child in children:

                if phase == 2 or phase == 3:
                    intersection = child[0].selecti(child[3], child[4])
                else:
                    intersection = child[0].selecti(child[1], child[2])

                if child[0].check3row(intersection):
                    phase = 4 #remove
                elif child[0].player1PiecesOffBoard == 0 and child[0].player2PiecesOffBoard == 0:
                    if child[0].countPieces(child[0].player) == 3:
                        phase = 3
                    phase = 2
                else:
                    phase = 1

                new_score = child[0].minimax(depth - 1, alpha, beta, False, phase)

                if new_score[0] > value:
                    if phase == 2 or phase == 3:
                        value = new_score[0]
                        index = child[1]
                        ring = child[2]
                        index_to_move = child[3]
                        ring_to_move = child[4] 
                    else:                       
                        value = new_score[0]
                        index = child[1]
                        ring = child[2]

                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            if phase != 2 and phase != 3:
                return value, index, ring
            else:
                return value, index, ring, index_to_move, ring_to_move

        else:

            value = math.inf
            children = self.children(phase)

            if phase != 2 and phase != 3:
                index, ring = random.choice(valid_locations)
            else:
                rand = random.choice(valid_locations)
                index, ring = random.choice(rand[1])
                index_to_move = rand[0][0]
                ring_to_move = rand[0][1]

            for child in children:

                if phase == 2 or phase == 3:
                    intersection = child[0].selecti(child[3], child[4])
                else:
                    intersection = child[0].selecti(child[1], child[2])

                if child[0].check3row(intersection):
                    phase = 4 #remove
                elif child[0].player1PiecesOffBoard == 0 and child[0].player2PiecesOffBoard == 0:
                    if child[0].countPieces(child[0].player) == 3:
                        phase = 3
                    phase = 2
                else:
                    phase = 1

                new_score = child[0].minimax(depth - 1, alpha, beta, True, phase)

                if new_score[0] < value:
                    if phase == 2 or phase == 3:
                        value = new_score[0]
                        index = child[1]
                        ring = child[2]
                        index_to_move = child[3]
                        ring_to_move = child[4] 
                    else:                       
                        value = new_score[0]
                        index = child[1]
                        ring = child[2]
                beta = min(beta, value)
                if beta <= alpha:
                    break
            if phase != 2 and phase != 3:
                return value, index, ring
            else:
                return value, index, ring, index_to_move, ring_to_move
