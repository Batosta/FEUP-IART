class Piece:

    def __init__(self, color, coords):
    	self.color = color
    	self.coords = coords

    def createPieceBoard(self, board):
    	board = []
    	r = 0
    	for row in board:
    		c = 0
    		newRow = []
    		for col in row:
    			newPiece = Piece(col, [c,r])
    			newRow.append(newPiece)
    			c += 1
    		board.append(newRow)
    		r += 1
    	return board