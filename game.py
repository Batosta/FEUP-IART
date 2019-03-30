import operator
import copy
import time

import levels
import utilities
from piece import Piece
from block import Block
from tree import Tree

class Game:
    def __init__(self, board):
        
        self.board = []
        self.blocks = []
        self.solved = False

        self.createPieceBoard(board)
        self.createBlocks()

        self.tree = Tree(self)
        finalState = self.tree.depthFirst(self)
        print("finalState: ")
        utilities.printBoard(finalState.board)

        # heuristicValue = node.heuristic()
        # print(heuristicValue)

        # Para fazer um move e juntar os blocks:
        # if self.ableToMove(self.blocks[1], "left"):
        #     self.moveBlock(self.blocks[1], "left")

        # Para mostrar o board | Mostrar os blocos existentes:
        # utilities.printBoard(self.board)
        # utilities.printBlocks(self.blocks)


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

    def ableToMove(self, block, direction):
        for piece in block.pieces:
            row = piece.coords[0]
            col = piece.coords[1]
            if direction == "up":
                if not ((row - 1) >= 0 and (self.board[row-1][col].color == piece.color or self.board[row-1][col].color == '0')):
                    return 0
            elif direction == "down":
                if not ((row + 1) <= 3 and (self.board[row+1][col].color == piece.color or self.board[row+1][col].color == '0')):
                    return 0
            elif direction == "left":
                if not ((col - 1) >= 0 and (self.board[row][col-1].color == piece.color or self.board[row][col-1].color == '0')):
                    return 0
            elif direction == "right":
                if not ((col + 1) <= 3 and (self.board[row][col+1].color == piece.color or self.board[row][col+1].color == '0')):
                    return 0
        return 1

    def moveBlock(self, block, direction):
        if direction == "up":
            self.moveBlockUp(block)
        elif direction == "down":
            self.moveBlockDown(block)
        elif direction == "left":
            self.moveBlockLeft(block)
        elif direction == "right":
            self.moveBlockRight(block)
        self.clean_blocks()
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

    def checkAllGameChilds(self):

        gameChilds = []

        blockIndex = 0
        for block in self.blocks:

            if self.ableToMove(block, "up"):
                temporaryGame = copy.deepcopy(self)
                temporaryGame.moveBlock(temporaryGame.blocks[blockIndex], "up")
                gameChilds.append([temporaryGame, blockIndex, "up"])

            if self.ableToMove(block, "down"):
                temporaryGame = copy.deepcopy(self)
                temporaryGame.moveBlock(temporaryGame.blocks[blockIndex], "down")
                gameChilds.append([temporaryGame, blockIndex, "down"])

            if self.ableToMove(block, "right"):
                temporaryGame = copy.deepcopy(self)
                temporaryGame.moveBlock(temporaryGame.blocks[blockIndex], "right")
                gameChilds.append([temporaryGame, blockIndex, "right"])

            if self.ableToMove(block, "left"):
                temporaryGame = copy.deepcopy(self)
                temporaryGame.moveBlock(temporaryGame.blocks[blockIndex], "left")
                gameChilds.append([temporaryGame, blockIndex, "left"])

            blockIndex += 1

        return gameChilds

    def checkWin(self):
        colors = []
        for block in self.blocks:
            if block.color not in colors:
                colors.append(block.color)
            else:
                return False
        return True
    def update(self):
        return utilities.getBoardArray(self.board)

    def getBlock(self, coordinates):
        for block in self.blocks:
            for piece in block.pieces:
                    if(piece.coords == coordinates):
                        return block

    def heuristic(self):

        heuristicValue = 0 
        blocks = self.blocks

        for i in range(len(blocks)):
            for k in range(i+1, len(blocks)): 
                if blocks[k].color == blocks[i].color:
                    heuristicValue += blocks[i].distance(blocks[k])

        return heuristicValue

    def __eq__(self, other):
        return self.blocks == other.blocks

p1 = Game(levels.lvl4)