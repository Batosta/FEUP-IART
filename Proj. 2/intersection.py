class Intersection:
        def __init__(self, pos, ring, connections):
            self.value = 0
            self.pos = pos
            self.ring = ring
            self.connections = connections

        def __eq__(self, intersection2):
            return self.value != 0 and intersection2.value != 0 and self.value == intersection2.value

        def getPos(self):
            return self.pos
        
        def getRing(self):
            return self.ring

        def getValue(self):
            return self.value

        def getConnections(self):
            return self.connections

        def set(self, value):
            self.value = value