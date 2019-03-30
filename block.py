class Block:

	def __init__(self, pieces, color):
		self.pieces = pieces
		self.color = color
	
	def distance(self, block):

		dist = 100

		for i in self.pieces:
			for j in block.pieces:
				distance = i.distance(j)
				if distance < dist:
					dist = distance
		
		return dist

	def __eq__(self, other):
		return self.pieces == other.pieces

	def __repr__(self):
		return str(self.pieces)