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
        self.movesArray = []

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, game, parent=None):

        node = Node(game)
        self[node.identifier] = node

        if parent is not None:
            self[parent].add_child(node.identifier)
        
        return node

    def breadth_first(self, start, moves):
        moves += 1
        currentLevel = start
        nextLevel = []

        for state in start:
            for block in state.blocks:
                if state.ableToMove(block, "up"):
                    newState = state
                    newState.moveBlock(block, "up")
                    if newState.checkWin():
                        return newState
                    else:
                        nextLevel.append(newState)
                if state.ableToMove(block, "down"):
                    newState = state
                    newState.moveBlock(block, "down")
                    if newState.checkWin():
                        return newState
                    else:
                        nextLevel.append(newState)
                if state.ableToMove(block, "right"):
                    newState = state
                    newState.moveBlock(block, "right")
                    if newState.checkWin():
                        return newState
                    else:
                        nextLevel.append(newState)
                if state.ableToMove(block, "left"):
                    newState = state
                    newState.moveBlock(block, "left")
                    if newState.checkWin():
                        return newState
                    else:
                        nextLevel.append(newState)
        self.breadth_first(nextLevel, moves)



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

    #Para aplicar será necessário criar uma instância de tree(root) e depois chamar a função
    #Ainda não testei, tenho de instalar a merda do pygame
    def greedy(self, game, id):
        
        if(game.checkWin()): return game
        
        node = self[id]
        currentGame = node.game()
        bestOption = None

        for block in currentGame.blocks:

            gameUp = currentGame, gameDown = currentGame, gameRight = currentGame, gameLeft = currentGame
            up = gameUp.tryMoveBlock(block, "up")
            down = gameDown.tryMoveBlock(block, "down")
            right = gameRight.tryMoveBlock(block, "right")
            left = gameLeft.tryMoveBlock(block, "left")

            heuristicValues = []

            if(up == 1): 
                nodeUp = Node(gameUp)
                h1 = nodeUp.heuristic()
                heuristicValues.append([nodeUp,h1])

            if(down == 1): 
                nodeDown = Node(gameDown)
                h2 = nodeDown.heuristic()
                heuristicValues.append([nodeDown,h2])

            if(right == 1): 
                nodeRight = Node(gameRight)
                h3 = nodeRight.heuristic()
                heuristicValues.append([nodeRight,h3])

            if(left == 1): 
                nodeLeft = Node(gameLeft)
                h4 = nodeLeft.heuristic()
                heuristicValues.append([nodeLeft,h4])

            bestHeuristic = 100000000
            for i in range(len(heuristicValues)):
                if (heuristicValues[i][1] < bestHeuristic):
                    bestHeuristic = heuristicValues[i][1]
                    bestOption = heuristicValues[i][0]

        self.add_node(bestOption.game(), node)

        return self.greedy(bestOption.game(), bestOption.identifier())
            
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