import operator
import copy
import time

import levels
import utilities
from piece import Piece
from block import Block

class Game:
    def __init__(self, board):
        # Para escolher o algoritmo a ser usado:
        # self.algorithm = utilities.chooseAlg()
        self.board = []
        self.blocks = []    
        self.moves = 0
        self.solved = False

        self.createPieceBoard(board)
        self.createBlocks()

        utilities.getBoardArray(self.board)

        # Para fazer um move e juntar os blocks:
        # self.tryMoveBlock(self.blocks[1], "left")
        # self.clean_blocks()

        # Para mostrar o board e moves | Mostrar os blocos existentes:
        # utilities.printBoard(self.board, self.moves)
        # utilities.printBlocks(self.blocks)

        # while not self.solved:
        #     self.tryMoveBlock(self.blocks[1], "left")
        #     utilities.printBoard(self.board, self.moves)
        #     self.clean_blocks()
        #     self.solved = self.checkWin



    def createBlocks(self):
        r = 0
        for row in self.board:
            c = 0
            for col in row:
                if self.board[r][c].color != '0':
                    newPiece = copy.deepcopy(self.board[r][c])
                    self.add_piece(newPiece)
                c += 1
            r += 1
        self.clean_blocks()
    def is_adjacent(self, piece, piece2):
        if ((abs(piece.coords[0] - piece2.coords[0]) + abs(piece.coords[1]- piece2.coords[1])) < 2):
            return True
        else:
            return False
    def in_block(self, block, piece):
        if block.color == piece.color:
            for p in block.pieces:
                if self.is_adjacent(p, piece):
                    return True
        return False
    def is_block_adjacent(self, b1, b2):
        for p2 in b2.pieces:
            if self.in_block(b1, p2):
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

    def tryMoveBlock(self, block, direction):
        canMove = True
        for piece in block.pieces:
            row = piece.coords[0]
            col = piece.coords[1]
            if direction == "up":
                if not ((row - 1) >= 0 and (self.board[row-1][col].color == piece.color or self.board[row-1][col].color == '0')):
                    canMove = False
            elif direction == "down":
                if not ((row + 1) <= 3 and (self.board[row+1][col].color == piece.color or self.board[row+1][col].color == '0')):
                    canMove = False
            elif direction == "left":
                if not ((col - 1) >= 0 and (self.board[row][col-1].color == piece.color or self.board[row][col-1].color == '0')):
                    canMove = False
            elif direction == "right":
                if not ((col + 1) <= 3 and (self.board[row][col+1].color == piece.color or self.board[row][col+1].color == '0')):
                    canMove = False
        if canMove:
            self.moveBlock(block, direction)
    def moveBlock(self, block, direction):
        self.moves += 1
        if direction == "up":
            self.moveBlockUp(block)
        elif direction == "down":
            self.moveBlockDown(block)
        elif direction == "left":
            self.moveBlockLeft(block)
        elif direction == "right":
            self.moveBlockRight(block)
    def moveBlockUp(self, block):
        for piece in block.pieces:
            self.board[piece.coords[0]][piece.coords[1]].color = '0'
        for piece in block.pieces:
            piece.coords[0] -= 1
            self.board[piece.coords[0]][piece.coords[1]].color = block.color
    def moveBlockDown(self, block):
        for piece in block.pieces:
            self.board[piece.coords[0]][piece.coords[1]].color = '0'
        for piece in block.pieces:
            piece.coords[0] += 1
            self.board[piece.coords[0]][piece.coords[1]].color = block.color
    def moveBlockLeft(self, block):
        for piece in block.pieces:
            self.board[piece.coords[0]][piece.coords[1]].color = '0'
        for piece in block.pieces:
            piece.coords[1] -= 1
            self.board[piece.coords[0]][piece.coords[1]].color = block.color
    def moveBlockRight(self, block):
        for piece in block.pieces:
            self.board[piece.coords[0]][piece.coords[1]].color = '0'
        for piece in block.pieces:
            piece.coords[1] += 1
            self.board[piece.coords[0]][piece.coords[1]].color = block.color
 

    def checkWin(self):
        colors = []
        for block in self.blocks:
            if block.color not in colors:
                colors.append(block.color)
            else:
                return False
        return True

p1 = Game(levels.test)