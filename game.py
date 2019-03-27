import levels
import utilities
from piece import Piece
from block import Block

class Game:
    def __init__(self, board):
        self.board = []
        self.blocks = []
        self.moves = 0
        self.createPieceBoard(board)
        self.createBlocks()
        for a in self.blocks:
            for b in a.pieces:
                print(b)
            print()
        # self.printBlocks()
        # self.printBoard()
    	# self.checkWin(3)
        # self.algorithm = utilities.chooseAlg()

    def printBlocks(self):
        # for block in self.blocks:
        #     for piece in block.pieces:
        #         print(piece.color)
        #     print()
        for block in self.blocks:
            print(block)

    def createBlocks(self):
        r = 0
        for row in self.board:
            c = 0
            for col in row:
                if self.board[r][c].color != '0':
                    self.add_piece(self.board[r][c])
                c += 1
            r += 1

    def is_adjacent(self, piece, piece2):
        if ((abs(piece.coords[0] - piece2.coords[0]) + abs(piece.coords[1]- piece2.coords[1])) < 2):
            return True
        else:
            return False
    def in_block(self, block, piece):
        for p in block.pieces:
            if self.is_adjacent(p, piece):
                return True
        return False
    def is_block_adjacent(self, b1, b2):
        for p in b1.pieces:
            for p2 in b2.pieces:
                if self.is_adjacent(p, p2):
                    return True
        return False
    def add_block_pieces_to_block(self, b1, b2):
        for p in b2.pieces:
            b1.pieces.append(p)
        self.blocks.remove(b2)
    def clean_blocks(self):
        for b1 in self.blocks:
            for b2 in self.blocks:
                if b1 != b2:
                    if self.is_block_adjacent(b1, b2):
                        self.add_block_pieces_to_block(b1,b2)
    def add_piece(self, piece):
        for block in self.blocks:
            if block.color == piece.color:
                if self.in_block(block, piece):
                    block.pieces.append(piece)
                    return
        newBlock = Block([piece], piece.color)
        self.blocks.append(newBlock)
        
    def createPieceBoard(self, board):
    	r = 0
    	for row in board:
    		c = 0
    		newRow = []
    		for col in row:
    			newPiece = Piece(col, [r,c])
    			newRow.append(newPiece)
    			c += 1
    		self.board.append(newRow)
    		r += 1

    def moveBlock(self, block, direction):
        if direction == "up":
            self.moveUp(block)
        elif direction == "down":
            self.moveDown(block)
        elif direction == "left":
            self.moveLeft(block)
        elif direction == "right":
            self.moveRight(block)

    def moveUp(self, block):
        a = 1
    def moveDown(self, block):
        a = 1
    def moveLeft(self, block):
        a = 1
    def moveRight(self, block):
        a = 1

    def printBoard(self):
        print()
        print("Moves: ", self.moves)
        for row in self.board:
            self.printRow(row)
    def printRow(self, row):
        print("[", end='')
        for col in row:
            print(" " + col.color + " ",end='')
        print("]")

    def checkWin(self):
        colors = []
        for block in self.blocks:
            if block.color not in colors:
                colors.append(block.color)
            else:
                return
        input("You won! Press Enter to continue...")
        exit()

p1 = Game(levels.lvl1)
