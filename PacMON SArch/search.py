# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# ELLERY LEUNG
# CSE 471 MW 9:40-10:55
# 1207157168

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

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
    """
    # MAKE SURE THESE WORK FOR QUESTION 1
    # python pacman.py -l tinyMaze -p SearchAgent
    # python pacman.py -l mediumMaze -p SearchAgent
    # python pacman.py -l bigMaze -z .5 -p SearchAgent

    # If start state is the goal, stop and move nowhere
    if (problem.isGoalState(problem.getStartState())):
        return ['Stop']

    from util import Stack
    stack = Stack()
    stack.push((problem.getStartState(), []))

    # Created a list of visited nodes
    visited = [problem.getStartState()]

    while (not stack.isEmpty()):
        #Pop the first item from the stack
        currentPos, currentPath = stack.pop()

        # print "current pos: ", currentPos, "\tdirection taken to get here: ", currentPath[-1]
        #first check if the node is goal, if so - skip the other steps and quit
        if (problem.isGoalState(currentPos)):
            return currentPath
        # Set that node to visited, since we are now evaluating it
        if (not currentPos in visited):
            visited.append(currentPos)
            
        # For every successor of the current node
        for successor in problem.getSuccessors(currentPos):
            if not(successor[0] in visited):        # If the successor hasn't been visited before, add it to stack
                newPath = list(currentPath)         # copy the current path
                newPath.append(successor[1])        # add the new direction to the path
                stack.push((successor[0], newPath)) # push onto the stack
                # print "\nold path", currentPath
                # print "new path", newPath

    # Function not implemented; will never be reached assuming there is a goal state
    util.raiseNotDefined()
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    # python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
    # python eightpuzzle.py

    # If start state is the goal, stop and move nowhere
    if (problem.isGoalState(problem.getStartState())):
        return ['Stop']

    from util import Queue
    queue = Queue()
    queue.push((problem.getStartState(), []))

    # Created a list of visited nodes
    visited = [problem.getStartState()]

    while (not queue.isEmpty()):
        #Pop the first item from the queue
        currentPos, currentPath = queue.pop()

        # if solution found, exit
        if (problem.isGoalState(currentPos)):
            return currentPath

        # print "current pos: ", currentPos, "\tdirection taken to get here: ", currentPath        
        for successor in problem.getSuccessors(currentPos): # For every successor of the current node
            if not(successor[0] in visited):        # If the successor hasn't been visited before, add it to queue
                visited.append(successor[0])        # Set that node to visited - place for successors, so that multiple nodes aren't expanded
                newPath = list(currentPath)         # copy the current path
                newPath.append(successor[1])        # add the new direction to the path
                queue.push((successor[0], newPath)) # push onto the queue

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
