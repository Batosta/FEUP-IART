# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

import utilities
import collections

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

    def __init__(self, game):
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


    def breadthFirst(self, initState):

        if initState.checkWin():
            return initState

        states = [initState]

        i = 0
        while(i < len(states)):

            newChildren = states[i].checkAllGameChilds()
            #child = [[board, moves, direction]]
            for child in newChildren:
                if child[0].checkWin():
                    return child[0]
                elif child[0] not in states:
                    states.append(child[0])
            i += 1


    def limitedDepthFirst(self, initState, maxDepth):

        if initState.checkWin():
            return initState

        states = [initState]

        i = 0
        while(i < len(states)):

            newChildren = states[i].checkAllGameChilds()
            #child = [[board, moves, direction]]
            for child in newChildren:
                if child[0].checkWin():
                    return child[0]
                elif child[0] not in states:
                    states.append(child[0])
            i += 1


    
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

    #Para aplicar será necessário criar uma instância de tree(root) e depois chamar a função
    #Ainda não testei, tenho de instalar a merda do pygame
    def greedy(self, game, moves):
        
        moves += 1

        if(game.checkWin()): return game

        bestOption = None

        for block in game.blocks:

            gameUp = game
            gameDown = game 
            gameRight = game 
            gameLeft = game

            heuristicValues = []

            if gameUp.ableToMove(block, "up"):
                gameUp.moveBlock(block, "up")
                nodeUp = Node(gameUp)
                h1 = nodeUp.heuristic()
                heuristicValues.append([nodeUp,h1])

            if gameDown.ableToMove(block, "down"):
                gameDown.moveBlock(block, "down")
                nodeDown = Node(gameDown)
                h2 = nodeDown.heuristic()
                heuristicValues.append([nodeDown,h2])
            
            if gameRight.ableToMove(block, "right"):
                gameRight.moveBlock(block, "right")
                nodeRight = Node(gameRight)
                h3 = nodeRight.heuristic()
                heuristicValues.append([nodeRight,h3])
            
            if gameLeft.ableToMove(block, "left"):
                gameLeft.moveBlock(block,"left")
                nodeLeft = Node(gameLeft)
                h4 = nodeLeft.heuristic()
                heuristicValues.append([nodeLeft,h4])

            bestHeuristic = 100000000
            for i in range(len(heuristicValues)):
                if (heuristicValues[i][1] < bestHeuristic):
                    bestHeuristic = heuristicValues[i][1]
                    bestOption = heuristicValues[i][0]

        return self.greedy(bestOption.game, moves)
            
    #def a_star(self, identifier):


    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item



class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()