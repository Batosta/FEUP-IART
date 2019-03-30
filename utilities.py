def chooseAlg():

    print("Please, choose which search method do you wish to use:")
    print("A) Breadth-first search.")
    print("B) Depth-first search.")
    print("C) Progressive deepening.")
    print("D) Uniform cost search.")
    print("E) Greedy.")
    print("F) A*.")

    ans=input()
    
    if ans == "A" or ans == "a":
        return 1
    elif ans == "B" or ans == "b":
        return 2
    elif ans == "C" or ans == "c":
        return 3
    elif ans == "D" or ans == "d":
        return 4
    elif ans == "E" or ans == "e":
        return 5
    elif ans == "F" or ans == "f":
        return 6
    else:
        chooseAlg()


def printBoard(board):
    for row in board:
        printRow(row)
def printRow(row):
    print("[", end='')
    for col in row:
        print(" " + col.color + " ", end='')
    print("]")

def printBlocks(blocks):
    for block in blocks:
        for pieces in block.pieces:
            print(pieces)
        print()

def printGameChilds(gameChilds):
    for child in gameChilds:
        print("move: " + child[2])
        print("blockIndex: ", end="")
        print(child[1])
        printBoard(child[0].board)
        print()

def getBoardArray(gameBoard):
    board = []
    for row in gameBoard:
        boardRow = []
        for piece in row:
            boardRow.append(piece.color)
        board.append(boardRow)
    return board

def compareBoard(board1, board2):
    for i in range(len(board1)):
        for j in range(len(board1[i])):
            if(board1[i][j] != board2[i][j]):
                return False
    return True

