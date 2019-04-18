import copy
import time

import levels

class Game:
    # Constructor
    def __init__(self):
        

        board = self.chooseLevel()

        self.board = self.createBoard(board)
        self.size = len(self.board)
        self.solution = self.createSolution()
        
        algorithm = self.chooseAlg()
        if algorithm == 1:
            self.breadthFirst(self.board)

        elif algorithm == 2:
            n = self.chooseHeuristic()
            self.nodesChecked = 0
            self.greedy([], self.board, n)

        elif algorithm == 3:
            n = self.chooseHeuristic()
            self.aStar([], self.board, n)


    # Breadth First Search (bfs) algorithm
    def breadthFirst(self, initState):

        startAlgTime = time.time()
        if initState == self.solution:
            print("Path:")
            self.printBoard(initState)
            print()
        
        visitedNodes = []           # nodes already visited
        visitedNodesID = []         # ID's of the nodes already visited

        toVisitNodesID = [[initState,'0']]      # nodes that still need to be checked + their ID's
        
        stillSearching = True

        solutionID = ""
        path = []

        while len(toVisitNodesID) != 0 and stillSearching:

            visitedNodes.append(toVisitNodesID[0][0])       # appending the board itself
            visitedNodesID.append(toVisitNodesID[0][1])     # appending the ID of the board

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

        # Get the path
        while solutionID != "0":

            solutionID = solutionID[:len(solutionID)-1]
            index = visitedNodesID.index(solutionID)
            path.append(visitedNodes[index])
        path.reverse()

        # Show the path
        print("Path:")
        for a in path:
            self.printBoard(a)
            print()

        self.showAlgInformation(len(path) - 1, len(visitedNodes), round(endAlgTime-startAlgTime, 3))

    # A* algorithm
    def aStar(self, initState, heuristic):

        startAlgTime = time.time()
        if initState == self.solution:
            print("Path:")
            self.printBoard(initState)
            print()

        if heuristic == 1:
            front = [[self.heuristic1(initState), initState]]
        elif heuristic == 2:
            front = [[self.heuristic1(initState), initState]]
        expanded = []
        nodesChecked = 0

        while front:
            nodesChecked += 1
            i = 0
            for j in range(1,len(front)):
                if front[i][0] > front[j][0]:
                    i = j
            path = front[i]
            front = front[:i] + front[i+1:]
            endnode = path[-1]

            if self.checkWin(endnode):   
                break

            if endnode in expanded: 
                continue

            for k in self.checkAllBoardChilds(endnode):
                
                if k in expanded: 
                    continue

                if heuristic == 1:
                    newpath = [path[0] + self.heuristic1(k) - self.heuristic1(endnode)] + path[1:] + [k]
                elif heuristic == 2:
                    newpath = [path[0] + self.heuristic2(k) - self.heuristic2(endnode)] + path[1:] + [k]
                front.append(newpath)
                expanded.append(endnode)

        endAlgTime = time.time()

        # Get the path
        finalPath = []
        for sol in path[1:]:
            finalPath.append(sol)

        # Show the path
        print("Path:")
        for k in finalPath:
            self.printBoard(k)
            print()

        self.showAlgInformation(len(finalPath) - 1, nodesChecked, round(endAlgTime-startAlgTime, 3))

    # Greedy algorithm
    def greedy(self, visited, initState, heuristic):

        startAlgTime = time.time()

        if initState == self.solution:
            return

        states = [initState]
        heuristicValue = 1000
        nextState = None

        i = 0
        going = True
        while i < len(states) and going:

            self.nodesChecked += 1
            newChildren = self.checkAllBoardChilds(states[i])
            for child in newChildren:

                if self.checkWin(child):
                    visited.append(child)
                    going = False
                    break

                if heuristic == 1:
                    tempHeuristic = self.heuristic1(child)
                elif heuristic == 2:
                    tempHeuristic = self.heuristic2(child)

                if(tempHeuristic < heuristicValue):
                    heuristicValue = tempHeuristic
                    nextState = copy.deepcopy(child)

            i += 1

        if(nextState in visited) and going:
            print("Couldn't find solution")
            return

        elif going:
            visited.append(nextState)
            self.greedy(visited, nextState, heuristic)
            return

        endAlgTime = time.time()

        for sol in visited:
            self.printBoard(sol)
            print()

        self.showAlgInformation(len(visited) - 1, self.nodesChecked, round(endAlgTime-startAlgTime, 3))


    # Number of pieces out of order
    def heuristic1(self, board):

        number = 0

        for i in range(0, self.size):
            for k in range(0, self.size):
                if board[i][k] != self.solution[i][k]:
                    number += 1

        return number

    # Sum of the Manhattan distances of the out of order pieces to their right order
    def heuristic2(self, board):

        distance = 0

        for i in range(0, self.size):
            for k in range(0, self.size):

                if board[i][k] != self.solution[i][k]:
                    inSolCoords = self.findInSolution(board[i][k])
                    distance += abs(inSolCoords[0]-i) + abs(inSolCoords[1]-k)

        return distance

    # Finds in the solution board the given value, and returns its coordinates
    def findInSolution(self, value):

        for i in range(0, self.size):
            for k in range(0, self.size):
                if self.solution[i][k] == value:
                    return [i, k]

    # Returns an array with all the boards that are children of the given board
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

    # Utility function that prints the given board in a user friendly way
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

    # Creates the board as an array of arrays of ints
    def createBoard(self, board):
        newBoard = []
        for row in board:
            newRow = []
            for col in row:
                newRow.append(int(col))
            newBoard.append(newRow)
        return newBoard
    
    # Creates the solution of the puzzle, taking into account only the size of the board
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

    # Checks if the 0 (zero) is able to move in the request direction in the given board
    def ableToMove(self, board, direction):

        zeroCoords = self.getZeroCoords(board)
        zeroRow = zeroCoords[0]
        zeroCol = zeroCoords[1]

        if (direction == "up" and (zeroRow - 1) < 0) or (direction == "down" and (zeroRow + 1) >= self.size) or (direction == "left" and (zeroCol - 1) < 0) or (direction == "right" and (zeroCol + 1) >= self.size):
            return False
        else:
            return True

    # Move predicates
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

    # Returns the coordinates of the 0 (zero)
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

    # Checks if the board is solution
    def checkWin(self, board):
        if self.solution == board:
            return True
        else:
            return False

    # Prints information about how many moves, how many nodes were visited 
    # and how much time the algorithm spent searching for the solution
    def showAlgInformation(self, nMoves, nVisitedNodes, timeElapsed):
        
        print("Number of moves: ", end="")
        print(nMoves, end=" moves.\n")

        print("Number of visited nodes: ", end="")
        print(nVisitedNodes, end=" nodes.\n")

        print("Time elapsed: ", end="")
        print(timeElapsed, end=" seg.\n")

    # Allows the user to choose the algorithm to apply
    def chooseLevel(self):

        print("\nPlease, choose which level you wish to be solved:")
        print("A) probl1.")
        print("B) probl2.")
        print("C) probl3.")
        print("D) probl4.")

        ans=input()

        if ans == "A" or ans == "a":
            return levels.probl1
        elif ans == "B" or ans == "b":
            return levels.probl2
        elif ans == "C" or ans == "c":
            return levels.probl3
        elif ans == "D" or ans == "d":
            return levels.probl4
        else:
            self.chooseLevel()


    # Allows the user to choose the algorithm to apply
    def chooseAlg(self):

        print("\nPlease, choose which search method you wish to use:")
        print("A) Breadth-first search.")
        print("B) Greedy.")
        print("C) A*.")

        ans=input()

        if ans == "A" or ans == "a":
            return 1
        elif ans == "B" or ans == "b":
            return 2
        elif ans == "C" or ans == "c":
            return 3
        else:
            self.chooseAlg()

    # Allows the user to choose the heuristic to apply
    def chooseHeuristic(self):
        
        print("\nPlease, choose which heuristic you wish to apply: ")
        print("A) Number of pieces out of order.")
        print("B) Sum of the Manhattan distances of the out of order pieces to their right order.")

        ans=input()

        if ans == "A" or ans == "a":
            return 1
        elif ans == "B" or ans == "b":
            return 2
        else:
            self.chooseHeuristic()


p1 = Game()