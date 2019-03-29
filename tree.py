# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

import utilities

id = 0

# Class node gets the argument game which represents the class game.
# The argument game represents the state of the board.
class Node(object):

    def __init__(self, game):
        global id
        id += 1

        self.__identifier = id
        self.__game = game 
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    @property
    def game(self):
        return self.__game

    def add_child(self, obj):
        self.__children.append(obj)

    def heuristic(self):

        heuristicValue = 0

        game = self.game
        blocks = game.blocks
        size = len(blocks)

        for i in range(size):
            for k in range(i+1, size): 
                if blocks[k].color == blocks[i].color:
                    heuristicValue += blocks[i].distance(blocks[k])

        return heuristicValue
    

#Class tree, holds all of the nodes at the same level to simplify search algorithms
class Tree(object):

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, game, parent=None):

        node = Node(game)
        self[node.identifier] = node

        if parent is not None:
            self[parent].add_child(node.identifier)
        
        return node

    def breadth_first(self, identifier):
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            queue = queue[1:] + expansion

    def depth_first(self, identifier):
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            queue = expansion + queue[1:]

    
    #recursive aux for progressive deepening
    def DLS(self, root, target, max_depth):
        if root == target : return True
        
        if max_depth <= 0 : return False

        for i in self[root]:
            if(self.DLS(i,target, max_depth-1)):
                return True
        return False
    
    #progressive deepening
    def IDDFS(self, root, target, max_depth):
        for i in range(max_depth):
            if (self.DLS(root, target, i)):
                return True
        return False

    #def uniform_cost_search(self, identifier):

    #def greedy(self, identifier):

    #def a_star(self, identifier):


    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    