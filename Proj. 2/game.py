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
        self.printMap()
        # self.play()

    def printMap(self):
        print(self.intersections[0].getValue(), end='-------')
        print(self.intersections[1].getValue(), end='-------')
        print(self.intersections[2].getValue())

        print('|       |       |')

        print('|  ', end='')
        print(self.intersections[8].getValue(), end='----')
        print(self.intersections[9].getValue(), end='----')
        print(self.intersections[10].getValue(), end='  |\n')
        
        print('|  |    |    |  |')

        print('|  |  ', end='')
        print(self.intersections[16].getValue(), end='-')
        print(self.intersections[17].getValue(), end='-')
        print(self.intersections[18].getValue(), end='  |  |\n')
        
        print('|  |  |   |  |  |')

        print(self.intersections[7].getValue(), end='--')
        print(self.intersections[15].getValue(), end='--')
        print(self.intersections[23].getValue(), end='   ')
        print(self.intersections[19].getValue(), end='--')
        print(self.intersections[11].getValue(), end='--')
        print(self.intersections[3].getValue())
        
        print('|  |  |   |  |  |')

        print('|  |  ', end='')
        print(self.intersections[22].getValue(), end='-')
        print(self.intersections[21].getValue(), end='-')
        print(self.intersections[20].getValue(), end='  |  |\n')

        print('|  |    |    |  |')

        print('|  ', end='')
        print(self.intersections[14].getValue(), end='----')
        print(self.intersections[13].getValue(), end='----')
        print(self.intersections[12].getValue(), end='  |\n')

        print('|       |       |')

        print(self.intersections[6].getValue(), end='-------')
        print(self.intersections[5].getValue(), end='-------')
        print(self.intersections[4].getValue())

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
        self.printMap()
        if self.check3row(intersection):
            self.remove()
            self.printMap()
        self.changePlayer()

    def remove(self):
        while True:
            pos = self.inputNumber()
            ring = self.inputRing()
            i = self.selecti(pos,ring)
            if i.getValue() == self.player or i.getValue() == 0:
                print("Choose a piece from your adversary to remove.")
            else:
                i.set(0)
                self.printMap()       
                break

    def resetBoard(self):
        for intersection in self.intersections:
            intersection.set(0)
            
    def changePlayer(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def inputRing(self):
        while True:
            ring = input("Select position (outer/middle/inner):  ")

            if ring in ['outer','middle','inner']:
                return ring
            else:
                print("Insert a valid ring (outer/middle/inner)\n")

    def inputNumber(self):
        while True:
            pos = input("Select position (0-7):  ")
            try:
                number = int(pos)
            except :
                print("Type a number (0-7)\n")
                continue
            if number >= 0 and number <=7:
                return number
            else:
                print("Insert a valid number (0-7)\n")
            
    def countPieces(self, player):
        c = 0
        for intersection in self.intersections:
            if intersection.getValue() == player:
                c += 1
    
    def canmove(self, intersection, intersection2):
        print(intersection.getValue())
        print(intersection2.getValue())
        print([intersection2.getPos(), intersection2.getRing()])
        print(intersection.getConnections())
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
        self.printMap()
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
            return 1
        else:
            return 2

    def checkWin(self):
        nextPlayer = self.getNextPlayer()
        if self.playerHasNoMoves(nextPlayer) or self.countPieces(nextPlayer) <= 2:
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
            pos = self.inputNumber()
            ring = self.inputRing()
            selected = self.selecti(pos, ring)
            if selected.getValue() == self.player:
                return selected
            print("Choose a piece you control!\n")

    def chooseIntersection(self):
        while True:
            pos = self.inputNumber()
            ring = self.inputRing()
            selected = self.selecti(pos, ring)
            if selected.getValue() == 0:
                return selected
            print("Choose an empty intersection!\n")

game = Board()