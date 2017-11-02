# qlearningAgents.py
# ------------------
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

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        # Since the q-values are initialized to 0, will return 0 if state unseen
        # Else will return the q-value of the state
        return self.qValues[(state, action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        # List of legal actions from given state
        legalActions = self.getLegalActions(state)

        # If terminal (no legal actions), return 0
        if len(legalActions) == 0:
          return 0
        else:
          # Used to compare maximum values
          maxValue = float("-inf")
          # For every legal action, update the max value
          for action in legalActions:
            maxValue = max(maxValue, self.getQValue(state, action))

        return maxValue

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        # List of legal actions from given state
        legalActions = self.getLegalActions(state)

        # Used to compare maximum values, and return the bestAction
        maxValue = float("-inf")
        bestAction = None
        # For every legal action, update the max value and best action
        for action in legalActions:
          tempQValue = self.getQValue(state, action)
          if tempQValue > maxValue:
            maxValue = tempQValue
            bestAction = action 

        # No need for conditional since bestAction initialized to None
        # If there are no legal actions, skip straight to return
        return bestAction

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)

        # If no legal actions (terminal), return None
        if len(legalActions) == 0:
          return None

        # If the result returns true with epsilon, perform a random action
        if util.flipCoin(self.epsilon):
          return random.choice(legalActions)
        else:
          return self.computeActionFromQValues(state)
        

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        # First part: 1-a * CurrentQValue
        newQValue = (1-self.alpha) * self.getQValue(state, action)

        # If no legal actions (terminal) in next state, sample = reward
        if len(self.getLegalActions(nextState)) == 0:
          sample = reward
        else:
          # Temporary max value to help find the max value for the nextState/nextAction
          tempMaxValue = float("-inf")
          # Iterate through all legal actions in the nextState
          for nextAction in self.getLegalActions(nextState):
            tempMaxValue = max(tempMaxValue, self.getQValue(nextState, nextAction))
          # sample = reward + y*max(Q(s',a'))
          sample = reward + (self.discount * tempMaxValue)

        # Update the value in the qValue list
        self.qValues[(state, action)] = newQValue + (self.alpha * sample)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        features = self.featExtractor.getFeatures(state, action)
        tempWeights = self.weights.copy()
        
        return features*tempWeights

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        tempWeights = self.weights.copy()      
        features = self.featExtractor.getFeatures(state, action)

        for feature in features:
          # reinit for each feature
          difference = 0
          # If no legal actions (terminal) in next state, diff = reward
          if len(self.getLegalActions(nextState)) == 0:
            difference = reward - self.getQValue(state, action)
          else:
            # Temporary max value to help find the max value for the nextState/nextAction
            tempMaxValue = float("-inf")
            # Iterate through all legal actions in the nextState
            for nextAction in self.getLegalActions(nextState):
              tempMaxValue = max(tempMaxValue, self.getQValue(nextState, nextAction))
            # diff = reward + y*max(Q(s',a'))
            difference = (reward + (self.discount * tempMaxValue)) - self.getQValue(state, action)
          # Update the weight - weight + (a * diff * featurevalue)
          tempWeights[feature] = self.weights[feature] + (self.alpha * difference * features[feature]) 
        self.weights = tempWeights.copy()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
