import math

class Piece:

	def __init__(self, color, coords):
		self.color = color
		self.coords = coords

	def __str__(self):
		qwerty = "color:" + str(self.color) + "->coords:" + str(self.coords[0]) + "," + str(self.coords[1]) 
		return qwerty

	def distance(self, piece):
		return abs(self.coords[0] - piece.coords[0]) + abs(self.coords[1] - piece.coords[1])

	def distance2(self, piece):
		return math.sqrt(math.pow(self.coords[0] - piece.coords[0], 2) + math.pow(self.coords[1] - piece.coords[1],2))


	def __eq__(self, other):
		return self.coords == other.coords

	def __repr__(self):
		return str(self.coords)