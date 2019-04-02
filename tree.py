# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

import utilities
import collections
import copy
import queue
from queue import PriorityQueue

id = 0

# Class node gets the argument game which represents the class game.
# The argument game represents the state of the board.


#Class tree, holds all of the nodes at the same level to simplify search algorithms
class Tree(object):

    def __init__(self, game):
        self.__nodes = {}
        self.__solution = []


    def solution(self):
        return self.__solution

    def add_path(self, board):
        self.__solution.append(board)

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
        parents = [initState]

        i = 0
        going = True
        while i < len(states) and going:

            newChildren = states[i].checkAllGameChilds()
            #child = [[board, moves, direction]]
            for child in newChildren:
                if child[0].checkWin():
                    states.append(child[0])
                    parents.append(states[i])
                    going = False
                    break
                elif child[0] not in states:
                    states.append(child[0])
                    parents.append(states[i])
            i += 1

        temp_sol = [states[-1].board]
        parent = parents[-1]
        while parent != initState:
            temp_sol.append(parent.board)
            parent = parents[states.index(parent)]
        temp_sol.append(parent.board)
        temp_sol.reverse()
        for sol in temp_sol:
            self.add_path(sol)

    def depthFirst(self, initState):

        if initState.checkWin():
            return initState

        visited = []
        states = Stack()
        states.push(initState)
        path = []

        going = True
        while not states.isEmpty() and going:

            visited.append(states.peek())

            newChildren = states.peek().checkAllGameChilds()
            newChildren.reverse()
            states.pop()


            for child in newChildren:

                if child[0].checkWin():
                    path.append(child[0])
                    going = False
                    break
                elif child[0] not in visited:
                    states.push(child[0])

        if not going:
            while path[-1] != initState:
                for parent in visited:
                    childs = parent.gameChilds()
                    if path[-1] in childs:
                        path.append(parent)
                        break
            path.reverse()
            for sol in path:
                self.add_path(sol.board)

    def limitedDepthSearch(self, initState, limit):
        if initState.checkWin():
            return initState

        visited = []
        states = Stack()
        states.push([initState, 0])
        path = []

        going = True
        while not states.isEmpty() and going:

            value = states.peek()[1] + 1
            if value > limit:
                states.pop()
                continue

            visited.append(states.peek()[0])

            newChildren = states.peek()[0].checkAllGameChilds()
            newChildren.reverse()
            states.pop()

            for child in newChildren:

                if child[0].checkWin():
                    path.append(child[0])
                    going = False
                    break
                elif child[0] not in visited:
                    states.push([child[0], value])

        if not going:
            while path[-1] != initState:
                for parent in visited:
                    childs = parent.gameChilds()
                    if path[-1] in childs:
                        path.append(parent)
                        break

            path.reverse()
            for sol in path:
                self.add_path(sol.board)


    def progressiveDeepening(self, initState, progress):

        if initState.checkWin():
            return initState

        currentProgress = progress
        visited = []
        toBeChecked = []
        states = Stack()
        states.push([initState, 0])

        while True:

            if states.isEmpty():
                currentProgress += progress
                toBeChecked.reverse()
                for i in toBeChecked:
                    states.push(i)
                toBeChecked = []

            if states.peek()[1] == currentProgress and states.peek()[1] != 0:
                toBeChecked.append(states.peek())
                states.pop()
                continue

            visited.append(states.peek()[0])
            newChildren = states.peek()[0].checkAllGameChilds()
            newChildren.reverse()
            value = states.peek()[1] + 1
            states.pop()

            for newChild in newChildren:

                if newChild[0].checkWin():
                    return newChild[0]
                elif newChild[0] not in visited:
                    states.push([newChild[0], value])

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
        for game in path[1:]:
            self.add_path(game.board)

    def greedy(self, visited, initState):

        if initState.checkWin():
            return initState

        states = [initState]
        heuristicValue = 1000
        nextState = None

        i = 0
        going = True
        while i < len(states) and going:

            newChildren = states[i].checkAllGameChilds()
            #child = [[board, moves, direction]]

            for child in newChildren:

                if child[0].checkWin():
                    visited.append(child[0])
                    going = False
                    break

                tempHeuristic = child[0].heuristic()

                if(tempHeuristic < heuristicValue):
                    heuristicValue = tempHeuristic
                    nextState = copy.deepcopy(child[0])

            i += 1

        if(nextState in visited) and going:
            print("Couldn't find solution")

        elif going:
            visited.append(nextState)
            return self.greedy(visited, nextState)

        for sol in visited:
            self.add_path(sol.board)

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
                path.append(endnode)
                break
            if endnode in expanded: continue
            for k in endnode.checkAllGameChilds():
                if k[0] in expanded: continue
                newpath = [path[0] + k[0].heuristic() - endnode.heuristic()] + path[1:] + [k[0]]
                front.append(newpath)
                expanded.append(endnode)

        for sol in path[1:]:
            self.add_path(sol.board)

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
