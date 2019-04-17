import copy
import time

import levels

class Game:
    def __init__(self, board):
        
        self.board = self.createBoard(board)
        self.size = len(self.board)
        self.solution = self.createSolution()

        self.breadthFirst(self.board)


    def breadthFirst(self, initState):

        startAlgTime = time.time()
        if initState == self.solution:
            self.printBoard(initState)
            return initState
        
        visitedNodes = []           # nós que já visitei
        visitedNodesID = []         # ids dos nós que já visitei (tem indexes = aos de visitedNodes)

        toVisitNodesID = [[initState,'0']]      # nós para visitar + id's
        
        stillSearching = True

        solutionID = ""
        path = []

        while len(toVisitNodesID) != 0 and stillSearching:

            visitedNodes.append(toVisitNodesID[0][0])       # estou a ir buscar o board
            visitedNodesID.append(toVisitNodesID[0][1])     # estou a ir buscar o id do board

            childs = self.checkAllBoardChilds(toVisitNodesID[0][0])
            toVisitNodesID.pop(0)

            i = 0
            for child in childs:

                if self.checkWin(child):
                    stillSearching = False
                    solutionID = visitedNodesID[-1] + str(i)
                    path.append(child)

                elif child not in visitedNodes:
                    toVisitNodesID.append([child, visitedNodesID[-1] + str(i)])
                i += 1

        endAlgTime = time.time()

        # get the path
        while solutionID != "0":

            solutionID = solutionID[:len(solutionID)-1]
            index = visitedNodesID.index(solutionID)
            path.append(visitedNodes[index])
        path.reverse()

        # show the path
        print("Path:")
        for a in path:
            self.printBoard(a)
            print()

        print("Number of visited nodes: ", end="")
        print(len(visitedNodes), end=" nodes.\n")

        print("Time elapsed: ", end="")
        print(round(endAlgTime-startAlgTime, 3), end=" seg.\n")


    def checkAllBoardChilds(self, board):

        boardChilds = []

        if self.ableToMove(board, "up"):
            tempBoard = copy.deepcopy(board)
            self.move(tempBoard, "up")
            boardChilds.append(tempBoard)
        if self.ableToMove(board, "down"):
            tempBoard = copy.deepcopy(board)
            self.move(tempBoard, "down")
            boardChilds.append(tempBoard)
        if self.ableToMove(board, "left"):
            tempBoard = copy.deepcopy(board)
            self.move(tempBoard, "left")
            boardChilds.append(tempBoard)
        if self.ableToMove(board, "right"):
            tempBoard = copy.deepcopy(board)
            self.move(tempBoard, "right")
            boardChilds.append(tempBoard)

        return boardChilds



    def printBoard(self, board):
        for row in board:
            self.printRow(row)
    def printRow(self, row):
        print("[", end='')
        for col in row:
            if(col >= 10):
                print(" " + str(col) +  " ", end='')
            else:
                print(" " + str(col) + "  ", end='')
        print("]")



    def createBoard(self, board):
        newBoard = []
        for row in board:
            newRow = []
            for col in row:
                newRow.append(int(col))
            newBoard.append(newRow)
        return newBoard
    def createSolution(self):

        newSolution = []

        for i in range(0, self.size):
            newRow = []
            for k in range(0, self.size):
                if(i == self.size - 1 and k == self.size -1):
                    newRow.append(0)
                else:
                    newRow.append(k + (self.size)*i + 1)
            newSolution.append(newRow)
        return newSolution


    def ableToMove(self, board, direction):

        zeroCoords = self.getZeroCoords(board)
        zeroRow = zeroCoords[0]
        zeroCol = zeroCoords[1]

        if (direction == "up" and (zeroRow - 1) < 0) or (direction == "down" and (zeroRow + 1) >= self.size) or (direction == "left" and (zeroCol - 1) < 0) or (direction == "right" and (zeroCol + 1) >= self.size):
            return False
        else:
            return True

    def move(self, board, direction):

        zeroCoords = self.getZeroCoords(board)
        zeroRow = zeroCoords[0]
        zeroCol = zeroCoords[1]

        if direction == "up":
            self.moveUp(board, zeroRow, zeroCol)
        elif direction == "down":
            self.moveDown(board, zeroRow, zeroCol)
        elif direction == "left":
            self.moveLeft(board, zeroRow, zeroCol)
        elif direction == "right":
            self.moveRight(board, zeroRow, zeroCol)
    def moveUp(self, board, zeroRow, zeroCol):

        oldValue = board[zeroRow - 1][zeroCol]
        board[zeroRow - 1][zeroCol] = 0
        board[zeroRow][zeroCol] = oldValue
    def moveDown(self, board, zeroRow, zeroCol):

        oldValue = board[zeroRow + 1][zeroCol]
        board[zeroRow + 1][zeroCol] = 0
        board[zeroRow][zeroCol] = oldValue
    def moveLeft(self, board, zeroRow, zeroCol):

        oldValue = board[zeroRow][zeroCol - 1]
        board[zeroRow][zeroCol - 1] = 0
        board[zeroRow][zeroCol] = oldValue
    def moveRight(self, board, zeroRow, zeroCol):

        oldValue = board[zeroRow][zeroCol + 1]
        board[zeroRow][zeroCol + 1] = 0
        board[zeroRow][zeroCol] = oldValue

    def getZeroCoords(self, board):

        zeroCol = -1
        zeroRow = -1

        i = 0
        for row in board:
            k = 0
            for col in row:
                if(col == 0):
                    zeroCol = k
                    zeroRow = i
                    return [zeroRow, zeroCol]
                else:
                    k += 1
            i += 1

    def checkWin(self, board):
        if self.solution == board:
            return True
        else:
            return False


p1 = Game(levels.probl2)