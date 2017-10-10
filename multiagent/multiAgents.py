# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):

    # python pacman.py -p ReflexAgent -l testClassic
    # python pacman.py --frameTime 0 -p ReflexAgent -k 1
    # python pacman.py --frameTime 0 -p ReflexAgent -k 2

    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Want to avoid stopping since it opens up opportunity for the ghost,
        # and stopping is usually a bad option.
        if action == 'Stop':
          return -500

        # Counter to keep track of the ghosts
        ghostCounter = 0
        while ghostCounter < len(newGhostStates):
          ghost = newGhostStates[ghostCounter]
          if (newPos == ghost.getPosition) and (newScaredTimes[ghostCounter] == 0):
            return -500
          ghostCounter += 1

        def euclideanDist(position, position2, info={}):
          "The Euclidean distance"
          xy1 = position
          xy2 = position2
          return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

        # Find the closest food        
        closest = -1
        for food in newFood.asList():
          tempDist = euclideanDist(newPos, food)
          if closest == -1:
            closest = tempDist
          elif tempDist < closest:
            closest = tempDist
        # Since closest is a min value, do 1/closest to get a more appropriate value
        closest = 1.0 / closest

        return successorGameState.getScore() + closest

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
      python autograder.py -q q2
      python autograder.py -q q2 --no-graphics
      python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
      python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
    """
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        # Recursive call of getVal
        return self.getVal(gameState, 1, 0, gameState.getNumAgents())
    
    def getVal(self, gameState, depth, currAgent, totalAgents):
      """
      Returns the best value obtained from recursive calls of getVal
      """
      # If horizon is reached, stop searching
      if depth > self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      # All agents have been iterated through, reset agents, increment depth
      newAgent = currAgent + 1
      if newAgent >= totalAgents:
        newAgent = 0
        depth += 1

      # Get all possible legal moves of the current agent
      legalMoves = []
      for legalAction in gameState.getLegalActions(currAgent):
        # Stopping is inoptimal, so do not perform these
        if legalAction != 'Stop':
          legalMoves.append(legalAction)

      # Make a list of choices from recursively calling getVal, these are possible actions to make.
      choices = []
      for action in legalMoves:
          choices.append(self.getVal(gameState.generateSuccessor(currAgent, action), depth, newAgent, totalAgents))

      # Pacman is making the first move, this is done b/c of the choices skipping
      if currAgent == 0 and depth == 1:
        highest = max(choices)
        # Make a list of the best possible choices and choose randomly
        bestChoices = []
        for i in range(len(choices)):
          if choices[i] == highest:
            bestChoices.append(i)
        chosen = random.choice(bestChoices)
        return legalMoves[chosen]
        
      # If pacman is moving (not first action), return highest evaluated option
      elif currAgent == 0:
        highest = max(choices)
        return highest
      # If other agent is moving, return lowest evaluated option
      else:
        lowest = min(choices)
        return lowest

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

