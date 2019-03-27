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
        self.printBoard()
        # self.createBlocks()
    	# self.checkWin(3)
        # self.algorithm = utilities.chooseAlg()



    def is_adjacent(piece, piece2):
        if ((abs(piece.coords[0] - piece.coords[0]) + abs(piece2.coords[1]- piece2.coords[1])) < 2))
            return True
        else:
            return False

    def in_bloc(block, piece):
        for p in block.board:
            if is_adjacent(p, piece)
                return True
        return False

    def add_piece(self, piece):
        for block in self.blocks:
            if block.color == piece.color:
                if in_block(block, piece):
                    block.board.append(piece)
                    return
        newBlock = Block([piece], piece.color)
        self.blocks.append(newBlock)
        
    def createPieceBoard(self, board):
    	r = 0
    	for row in board:
    		c = 0
    		newRow = []
    		for col in row:
    			newPiece = Piece(col, [c,r])
    			newRow.append(newPiece)
    			c += 1
    		self.board.append(newRow)
    		r += 1

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

    # 	print(coords)

    # def select_piece(self, piece):
    #     r = 0
    #     positions = []
    #     for row in self.board:
    #         c = 0
    #         for col in self.board[r]:
    #             if self.board[r][c] == piece:
    #                 positions.append([r,c])
    #             c += 1
    #         r += 1
    #     if len(positions) == 0:
    #         print("There is no " + piece + " piece")
    #     return positions
    # def change_pieces(self, piece, pos, pos2):
    #     if pos2[0] not in [0, 1, 2, 3] or pos2[1] not in [0, 1, 2, 3]:
    #         return piece
    #     piece2 = self.board[pos2[0]][pos2[1]]
    #     if piece[0] == piece2[0] and piece < piece2:
    #         self.board[pos2[0]][pos2[1]] = piece
    #         return piece
    #     elif piece[0] == piece2[0]:
    #         self.board[pos[0]][pos[1]] = piece2
    #         return piece2
    # def check_adjacent_squares(self, piece, pos):
    #     p1 = self.change_pieces(piece, pos, [pos[0], pos[1]+1])
    #     p2 = self.change_pieces(p1, pos, [pos[0], pos[1]-1])
    #     p3 = self.change_pieces(p2, pos, [pos[0]+1, pos[1]])
    #     self.change_pieces(p3, pos, [pos[0]-1, pos[1]])
    # def join_color(self, piece, positions):
    #     for pos in positions:
    #         self.check_adjacent_squares(piece, pos)
    #     new_positions = self.select_piece(piece)
    #     if new_positions != positions:
    #         self.join_color(piece, new_positions)

    # def move(self, piece, movements):
    #     r = 0
    #     for row in self.board:
    #         c = 0
    #         for col in self.board[r]:
    #             if [r,c] in movements:
    #                 self.board[r][c] = piece
    #             elif self.board[r][c] == piece:
    #                 self.board[r][c] = '0'
    #             c += 1
    #         r += 1
    # def can_move(self, piece, x, y):
    #     positions_to_move = self.select_piece(piece)
    #     positions_after_move = []
    #     for pos in positions_to_move:
    #         positions_after_move.append([pos[0]+y,pos[1]+x])
    #     for pos in positions_after_move:
    #         if pos[0] not in [0, 1, 2, 3] or pos[1] not in [0, 1, 2, 3]:
    #             print("Out of bounds move")
    #             return False
    #         if self.board[pos[0]][pos[1]] not in ['0', piece]:
    #             print("Piece blocking the movement: " + self.board[pos[0]][pos[1]])
    #             return False
    #     self.move(piece, positions_after_move)
    #     self.join_color(piece, positions_after_move)
    #     self.moves += 1
    #     return True
    # def move_left(self, piece):
    #     self.can_move(piece, -1, 0)
    #     self.printBoard()
    #     self.win()
    # def move_right(self, piece):
    #     self.can_move(piece, 1, 0)
    #     self.printBoard()
    #     self.win()
    # def move_up(self, piece):
    #     self.can_move(piece, 0, -1)
    #     self.printBoard()
    #     self.win()
    # def move_down(self, piece):
        # self.can_move(piece, 0, 1)
        # self.printBoard()
        # self.win()

p1 = Game(levels.test)
