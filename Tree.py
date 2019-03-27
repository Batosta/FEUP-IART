import game

id = 0

# Class node gets the argument game which represents the class game.
# The argument game represents the state of the board.
class Node(object):
    def __init__(self, game):
        global id
        id += 1
        self.identifier = id
        self.game = game 
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


#Class tree, holds all of the nodes at the same level to simplify search algorithms
class Tree(object):
    def __init__(self):
        self.nodes = []

    def get_node(self, identifier):
        for node in enumerate(self.nodes):
            if node.identifier == identifier:
                break
        return node

    def create_node(self, parentID):
        node = Node(game)
        self.nodes.append(node)

        nodeParent = self.get_node(parentID)
        nodeParent.add_child(node)