# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import heapq

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        flag = False
        for index, (p, c, i) in enumerate(self.heap):
            if i[0] == item[0]:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                flag = True
                break
        #else:
            #self.push(item, priority)
        return flag

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    "*** YOUR CODE HERE ***"
    """
    start = problem.getStartState(),'Stop',0
    frontier = util.Stack()  #Create an empty Stack
    frontier.push(start)
    visited = [] # List of visited states
    previousNode = {} # This is a dictionary, that maps a node with the one it came from

    while not frontier.isEmpty():

        node = frontier.pop()
        visited.append(node[0])
        #print "Node:", node

        if problem.isGoalState(node[0]): # Use backtracking to return the solution
            result = []
            temp = node
            while temp is not start:
                result.append(temp)
                temp=previousNode[temp]
            return [x[1] for x in reversed(result)]

        for successor in problem.getSuccessors(node[0]):
            if successor[0] not in visited: # If successor is not visited
                frontier.push(successor)
                previousNode[successor] = node

    return [] # Goal was not found


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState(),'Stop',0
    if problem.isGoalState(start[0]):
        return [start]

    frontier = util.Queue()  #Create an empty Stack
    frontier.push(start)
    visitedPlus = [start[0]] # List of visited states AND states that are in the frontier. Those are the states that we dont want to visit again
    previousNode = {} # This is a dictionary, that maps a node with the one it came from

    while not frontier.isEmpty():

        node = frontier.pop()

        for successor in problem.getSuccessors(node[0]):
            if successor[0] not in visitedPlus: # If successor is not visited or is in the frontier
                visitedPlus.append(successor[0])
                previousNode[successor] = node

                if problem.isGoalState(successor[0]): # Use backtracking to return the solution
                    result = []
                    temp = successor
                    while temp is not start:
                        result.append(temp)
                        temp=previousNode[temp]
                    return [x[1] for x in reversed(result)]

                frontier.push(successor)

    return [] # Goal was not found

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState(),'Stop',0
    frontier = PriorityQueue()  #Create an empty Stack
    visited = [] # List of visited states
    frontierNodes = [start[0]]
    previousNode = {} # This is a dictionary, that maps a node with the one it came from
    pathCost = {} # Dicionary for the total cost from the start state to the node
    pathCost[start] = 0
    frontier.push(start,pathCost[start]) 

    while not frontier.isEmpty():

        node = frontier.pop()
        if node in frontierNodes:
            frontierNodes.remove(node[0])
        visited.append(node[0])

        if problem.isGoalState(node[0]): # Use backtracking to return the solution
            result = []
            temp = node
            while temp is not start:
                result.append(temp)
                temp=previousNode[temp]
            return [x[1] for x in reversed(result)]

        for successor in problem.getSuccessors(node[0]):
            if successor[0] not in frontierNodes:
                if successor[0] not in visited: # If successor is not visited and is not in the frontier
                    pathCost[successor] = pathCost[node] + successor[2]
                    frontier.push(successor,pathCost[successor]) # The priority of the successor is the cost of the path to 
                    frontierNodes.append(successor[0])           # its previous node added by the cost to get to the successor
                    previousNode[successor] = node
            else: # Successor is in the frontier
                if(frontier.update(successor,pathCost[node] + successor[2])):
                    pathCost[successor] = pathCost[node] + successor[2]
                    previousNode[successor] = node

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState(),'Stop',0
    frontier = PriorityQueue()  #Create an empty Stack
    visited = [] # List of visited states
    frontierNodes = [start[0]]
    previousNode = {} # This is a dictionary, that maps a node with the one it came from
    pathCost = {} # Dicionary for the total cost from the start state to the node

    pathCost[start] = 0 
    frontier.push(start, pathCost[start] + heuristic(start[0],problem))

    while not frontier.isEmpty():

        node = frontier.pop()
        if node in frontierNodes:
            frontierNodes.remove(node[0])
        visited.append(node[0])

        if problem.isGoalState(node[0]): # Use backtracking to return the solution
            result = []
            temp = node
            while temp is not start:
                result.append(temp)
                temp=previousNode[temp]
            return [x[1] for x in reversed(result)]

        for successor in problem.getSuccessors(node[0]):
            #if successor[0] not in [x[0] for x in frontierNodes]: 
            if successor[0] not in frontierNodes: # If successor is not visited or is in the frontier
                if successor[0] not in visited: #[x[0] for x in visited]:
                    pathCost[successor] = pathCost[node] + successor[2]
                    frontier.push(successor,pathCost[successor] + heuristic(successor[0],problem)) # The priority of successor is the cost we had in ucs
                    frontierNodes.append(successor[0])                                             # added by the heuristic function's return value.
                    previousNode[successor] = node
            else: # Successor is in the frontier
                if(frontier.update(successor,pathCost[node] + successor[2] + heuristic(successor[0],problem))):
                    pathCost[successor] = pathCost[node] + successor[2]
                    previousNode[successor] = node
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
