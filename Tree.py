# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

import game
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

    def add_child(self, obj):
        self.__children.append(obj)


    def heuristic(self):
        a = 1
        return a




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


    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item