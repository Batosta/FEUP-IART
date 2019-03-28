class Piece:

	def __init__(self, color, coords):
		self.color = color
		self.coords = coords

	def __str__(self):
		qwerty = "color:" + str(self.color) + "->coords:" + str(self.coords[0]) + "," + str(self.coords[1]) 
		return qwerty

	def distance(self, piece):
		return abs(self.coords[0] - piece.coords[0]) + abs(self.coords[1] - piece.coords[1])