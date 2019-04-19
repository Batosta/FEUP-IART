import copy
import time

import problems

class N_line:
    def __init__(self):
        self.start()

    def start(self):
        print("Choose the problem (1-4):")
        print("\n  Problem 1")
        self.printBoard(problems.prob1)
        print("\n  Problem 2")
        self.printBoard(problems.prob2)
        print("\n  Problem 3")
        self.printBoard(problems.prob3)
        print("\n  Problem 4")
        self.printBoard(problems.prob4)
        problem = input("\n")
        while problem not in ['1','2','3','4']:
            problem = input("\nPlease select a valid number (1-4)\n")


        print("Choose the algorithm (1-3):")
        print("\n 1) Breadth first")
        print("\n 2) Greedy")
        print("\n 3) A*")

        algorithm = input("\nPlease select a valid number (1 or 2)\n")
        while algorithm not in ['1','2','3']:
            algorithm = input("\nPlease select a valid number (1 or 2)\n")

        if algorithm == '1':
            self.solve(problem , '1', 0)
            return

        print("Choose the heuristic (1 or 2):")
        print("\n 1) Number of pieces out of their position")
        print("\n 2) Manhattan distance of pieces to their position")
        heuristic = input("\n")
        while heuristic not in ['1','2']:
            heuristic = input("\nPlease select a valid number (1 or 2)\n")
        self.solve(problem, algorithm, int(heuristic))


    def solve(self, problem, algorithm, heuristic):
        self.chooseBoard(problem)
        if algorithm == '1':
            self.breadthfirst(self.board)
        elif algorithm == '2':
            self.greedy(self.board, heuristic)
        elif algorithm == '3':
            self.astar(self.board, heuristic)
        else:
            print('Unknown algorithm (solve)')

    def chooseBoard(self, problem):
        if problem == '1':
            self.board = problems.prob1
        if problem == '2':
            self.board = problems.prob2
        if problem == '3':
            self.board = problems.prob3
        if problem == '4':
            self.board = problems.prob4

        self.n = len(self.board[0])
        self.solution = self.createSol(self.n)

    def printBoard(self, board):
        for line in board:
            for col in line:
                if col < 10:
                    print(" " + str(col), end="   ")
                else:
                    print(str(col), end="   ")
            print(end="\n")

    def createSol(self, n):
        i = 1
        solution = []
        while len(solution) < n:
            col = []
            while len(col) < n:
                col.append(i)
                i += 1
            solution.append(col)
        solution[n-1][n-1] = 0
        return solution

    def coords(self, board, number):
        l = 0
        for line in board:
            c = 0
            for col in line:
                if col == number:
                    return c,l
                c += 1
            l += 1

    def isMovePossible(self, board, diretion):
        x, y = self.coords(board, 0)
        if diretion == 'up':
            return y-1 >= 0
        elif diretion == 'down':
            return y+1 < self.n
        elif diretion == 'left':
            return x-1 >= 0
        elif diretion == 'right':
            return x+1 < self.n
        else:
            print("Invalid diretion")

    def move(self, boardToMove, diretion):
        x, y = self.coords(boardToMove, 0)

        if diretion == 'up':
            numberToSwitch = boardToMove[y-1][x]
            boardToMove[y-1][x], boardToMove[y][x] = 0, numberToSwitch
        elif diretion == 'down':
            numberToSwitch = boardToMove[y+1][x]
            boardToMove[y+1][x], boardToMove[y][x] = 0, numberToSwitch
        elif diretion == 'left':
            numberToSwitch = boardToMove[y][x-1]
            boardToMove[y][x-1], boardToMove[y][x] = 0, numberToSwitch
        elif diretion == 'right':
            numberToSwitch = boardToMove[y][x+1]
            boardToMove[y][x+1], boardToMove[y][x] = 0, numberToSwitch

    def checkWin(self, board):
        return board == self.solution

    def breadthfirst(self, initialState):
        intialTime = time.time()

        if initialState == self.solution:
            print(initialState)
            print("Time elapsed: 0 seconds")
            print("The problem was already solved.")
            return

        tocheck = [initialState]
        visited = []
        solution = []
        searching = True

        while len(tocheck) != 0 and searching:
            currentBoard = tocheck.pop(0)
            visited.append(currentBoard)

            childs = self.getAllChilds(currentBoard)
            for child in childs:
                if self.checkWin(child):
                    solution = child
                    searching = False
                    break
                if child not in visited:
                    tocheck.append(child)

        endTime = time.time()

        print("Solution found!")
        print("Number of visited nodes: ", end="")
        print(len(visited), end=" nodes.\n")

        print("Time elapsed: ", end="")
        print(round(endTime-intialTime, 5), end=" seconds.\n")

        path = [solution]
        while path[-1] != initialState:
            for vis in visited:
                if path[-1] in self.getAllChilds(vis):
                    path.append(vis)
                    break

        path.reverse()
        i = 0
        for b in path:
            print("   Move ", end="")
            print(i)
            self.printBoard(b)
            i += 1

    def greedy(self, initialState, heuristic):
        intialTime = time.time()

        if initialState == self.solution:
            print(initialState)
            print("Time elapsed: 0 seconds")
            print("The problem was already solved.")
            return

        state = initialState
        nodesChecked = 0
        visited = [initialState]

        searching = True
        while searching:
            heuristicValue = 1000
            nextState = []
            nodesChecked += 1
            newChildren = self.getAllChilds(state)

            for child in newChildren:

                if child in visited:
                    continue

                if self.checkWin(child):
                    visited.append(child)
                    searching = False
                    break

                tempHeuristic = self.heuristic(child, heuristic)

                if(tempHeuristic < heuristicValue):
                    heuristicValue = tempHeuristic
                    nextState = copy.deepcopy(child)

            if searching and nextState != []:
                visited.append(nextState)
                state = nextState
            elif searching:
                break

        endTime = time.time()

        if searching:
            print("Solution not found!")
            return

        print("Solution found!")
        print("Number of visited nodes: ", end="")
        print(nodesChecked, end=" nodes.\n")

        print("Time elapsed: ", end="")
        print(round(endTime-intialTime, 5), end=" seconds.\n")

        z = 0
        for b in visited:
            print("   Move ", end="")
            print(z)
            self.printBoard(b)
            z += 1



    def astar(self, initialState, heuristic):
        intialTime = time.time()

        if initialState == self.solution:
            print(initialState)
            print("Time elapsed: 0 seconds")
            print("The problem was already solved.")
            return

        front = [[self.heuristic(initialState, heuristic), initialState]]
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

            for k in self.getAllChilds(endnode):
                if k in expanded: continue
                newpath = [path[0] + self.heuristic(k, heuristic) - self.heuristic(endnode, heuristic)] + path[1:] + [k]
                front.append(newpath)
                expanded.append(endnode)

        endTime = time.time()

        print("Solution found!")
        print("Number of visited nodes: ", end="")
        print(nodesChecked, end=" nodes.\n")

        print("Time elapsed: ", end="")
        print(round(endTime-intialTime, 5), end=" seconds.\n")

        z = 0
        for b in path[1:]:
            print("   Move ", end="")
            print(z)
            self.printBoard(b)
            z += 1


    def getAllChilds(self, board):
        childs = []

        if self.isMovePossible(board, 'up'):
            temp = copy.deepcopy(board)
            self.move(temp,'up')
            childs.append(temp)
        if self.isMovePossible(board, 'down'):
            temp = copy.deepcopy(board)
            self.move(temp,'down')
            childs.append(temp)
        if self.isMovePossible(board, 'left'):
            temp = copy.deepcopy(board)
            self.move(temp,'left')
            childs.append(temp)
        if self.isMovePossible(board, 'right'):
            temp = copy.deepcopy(board)
            self.move(temp,'right')
            childs.append(temp)
        return childs


    def heuristic(self, board, heuristic):
        if heuristic == 1:
            return self.h1(board)
        elif heuristic == 2:
            return self.h2(board)
        else:
            print("Unknown heuristic (1 or 2)")

    def h1(self, board):
        piecesOutside = 0
        l = 0
        for line in board:
            c = 0
            for col in line:
                if col != self.solution[l][c]:
                    piecesOutside += 1
                c += 1
            l += 1
        return piecesOutside

    def h2(self, board):
        distManhattan = 0
        i = 0
        while i < (self.n*self.n):
            distManhattan += self.distFromPos(board, i)
            i += 1
        return distManhattan

    def distFromPos(self, board, number):
        actualX, actualY = self.coords(board, number)
        desiredX, desiredY = self.coords(self.solution, number)
        return abs(desiredX - actualX) + abs(desiredY - actualY)

p1 = N_line()
