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
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    # MAKE SURE THESE WORK FOR QUESTION 1
    # python pacman.py -l tinyMaze -p SearchAgent
    # python pacman.py -l mediumMaze -p SearchAgent
    # python pacman.py -l bigMaze -z .5 -p SearchAgent

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    stop = Directions.STOP

    # If start state is the goal, stop and move nowhere
    if (problem.isGoalState(problem.getStartState())):
        return [stop]

    from util import Stack
    stack = Stack()
    tempList = problem.getSuccessors(problem.getStartState())
    for successor in tempList:
        stack.push(successor)

    # Created a list of visited nodes
    visited = [problem.getStartState()]
    # Create a list of steps to take
    steps = []

    # Start with appending the steps to every node explored.
    # Don't worry about the backtracking yet - the nodes will handle it
    # Main key* Figure out how to track where to remove nodes (after backtracking)

    print "\nNow printing stack"
    while (not stack.isEmpty()):
        #Pop the first item from the stack
        tempItem = stack.pop()

        #first check if the node is goal, if so - skip the other steps and quit
        if (problem.isGoalState(tempItem[0])):
            break
        #Set that node to visited, since we are now evaluating it
        if not(tempItem[0] in visited):
            visited.append(tempItem[0])
        tempList = (problem.getSuccessors(tempItem[0]))
        print tempList
        if (tempList):
            for successor in tempList:
                if not(successor[0] in visited):
                    stack.push(successor)
    print "\nDone printing stack"

    print "\nPrinting visited"
    for node in visited:
        print node
    # print "Sucessor of successor(s):", problem.getSuccessors((5,4))

    return steps
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
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
