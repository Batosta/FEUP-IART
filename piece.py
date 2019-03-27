class Piece:

    def __init__(self, color, coords):
    	self.color = color
    	self.coords = coords

    def __str__(self):
    	qwerty = "color:" + str(self.color) + "->coords:" + str(self.coords[0]) + "," + str(self.coords[1]) 
    	return qwerty