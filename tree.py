# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

import utilities
import collections
import copy
import queue
import levels
from queue import PriorityQueue

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


    # usar visited (como no depth)
    def breadthFirst(self, initState):

        if initState.checkWin():
            return initState

        states = [initState]

        i = 0
        while i < len(states):

            newChildren = states[i].checkAllGameChilds()
            #child = [[board, moves, direction]]
            for child in newChildren:
                if child[0].checkWin():
                    return child[0]
                elif child[0] not in states:
                    states.append(child[0])
            i += 1

    def depthFirst(self, initState):

        if initState.checkWin():
            return initState

        visited = []
        states = Stack()
        states.push(initState)

        while not states.isEmpty():

            visited.append(states.peek())

            newChildren = states.peek().checkAllGameChilds()
            newChildren.reverse()
            states.pop()

            for child in newChildren:

                if child[0].checkWin():
                    return child[0]
                elif child[0] not in visited:
                    states.push(child[0])

    #limited depth
    def limitedDepthSearch(self, initState, limit):
        if initState.checkWin():
            return initState

        visited = []
        states = Stack()
        states.push([initState, 0])

        while not states.isEmpty():

            value = states.peek()[1] + 1
            if value > limit:
                states.pop()
                continue

            newChildren = states.peek()[0].checkAllGameChilds()
            newChildren.reverse()
            states.pop()

            for child in newChildren:

                if child[0].checkWin():
                    return child[0]
                elif child[0] not in visited:
                    states.push([child[0], value])

    def uniform_cost_search(self, initState):
        front = [[0, initState]]
        expanded = []

        while front:
            i = 0
            for j in range(1,len(front)):
                if front[i][0] > front[j][0]:
                    i = j
            path = front[i]
            front = front[:i] + front[i+1:]
            endnode = path[-1]
            if endnode.checkWin():
                break
            if endnode in expanded: continue
            for k in endnode.checkAllGameChilds():
                if k[0] in expanded: continue
                newpath = [path[0] + 1] + path[1:] + [k[0]]
                front.append(newpath)
                expanded.append(endnode)
        print("Solution:")
        print(utilities.printBoard(path[len(path)-1].board))

    #falta quando parar nos casos que chega a um dead state    
    def greedy(self, visited, initState):

        if initState.checkWin():
            return initState

        states = [initState]
        heuristicValue = 1000
        nextState = None

        i = 0
        while(i < len(states)):

            newChildren = states[i].checkAllGameChilds()
            #child = [[board, moves, direction]]

            for child in newChildren:
                
                if child[0].checkWin():
                    return child[0]

                tempHeuristic = child[0].heuristic()

                if(tempHeuristic < heuristicValue):
                    heuristicValue = tempHeuristic
                    nextState = copy.deepcopy(child[0])

            i += 1

        if(nextState in visited):
            print("Couldn't find solution")
            return nextState
        else: 
            visited.append(nextState)
            return self.greedy(visited, nextState)


    def a_star(self, initState):
        front = [[initState.heuristic(), initState]]
        expanded = []

        while front:
            i = 0
            for j in range(1,len(front)):
                if front[i][0] > front[j][0]:
                    i = j
            path = front[i]
            front = front[:i] + front[i+1:]
            endnode = path[-1]
            if endnode.checkWin():
                break
            if endnode in expanded: continue
            for k in endnode.checkAllGameChilds():
                if k[0] in expanded: continue
                newpath = [path[0] + k[0].heuristic() - endnode.heuristic()] + path[1:] + [k[0]]
                front.append(newpath)
                expanded.append(endnode)
        print("Solution:")
        print(utilities.printBoard(path[len(path)-1].board))

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)