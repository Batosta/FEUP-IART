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


def printBoard(board, moves):
    print()
    print("Moves: ", moves)
    for row in board:
        printRow(row)
def printRow(row):
    print("[", end='')
    for col in row:
        print(" " + col.color + " ",end='')
    print("]")

def printBlocks(blocks):
    for block in blocks:
        for pieces in block.pieces:
            print(pieces)
        print()

def getBoardArray(gameBoard):
    board = []
    for row in gameBoard:
        boardRow = []
        for piece in row:
            boardRow.append(piece.color)
        board.append(boardRow)
    return board