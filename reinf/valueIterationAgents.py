# valueIterationAgents.py
# -----------------------
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

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        """
        python autograder.py -q q1
        python gridworld.py -a value -i 100 -k 10
        python gridworld.py -a value -i 5
        """

        # For every iteration specified, since range stops at self.iterations - 1
        for x in range(0, self.iterations):
          newIteration = util.Counter()
          # For every state in the MDP
          for currState in self.mdp.getStates():
            # If the state is terminal, set equal to 0
            if self.mdp.isTerminal(currState):
              newIteration[currState] = 0
            else:
              # Set highest to -inf for initializing comparison of highest value
              highest = float("-inf")
              # For each possible action from the current state
              for action in self.mdp.getPossibleActions(currState):
                totalValue = 0
                transitions = self.mdp.getTransitionStatesAndProbs(currState, action)
                # Iterate through the lists together
                for trans in transitions:
                  # Prob * CurrReward + y*nextState's value
                  totalValue += trans[1] * (self.mdp.getReward(currState, action, trans[0])
                                         + self.discount*self.values[trans[0]])
                highest = max(highest, totalValue)
                newIteration[currState] = highest
          self.values = newIteration

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # Computes the q-value itself, used in both computeQvaluefromvalues and computeactionfromvalues
    def computeReward(self, state, action):
      transitions = self.mdp.getTransitionStatesAndProbs(state, action)
      reward = 0
      for trans in transitions:
        # trans[1] is the probability of that state
        # get the reward of transitioning to the new state trans[0]
        # get discount specified * current value of trans[0]
        reward += trans[1]*(self.mdp.getReward(state, action, trans[0]) + self.discount*self.values[trans[0]])
      return reward

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        
        return self.computeReward(state, action)

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        # If terminal state, return none
        if self.mdp.isTerminal(state):
          return None

        # highest is a value to compare the best reward.
        # returnAction is a var to contain the action to be returned
        highest = float("-inf")
        returnAction = None
        for action in self.mdp.getPossibleActions(state):
          reward = self.computeReward(state, action)
          if reward > highest:
            returnAction = action
            highest = reward
        return returnAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
