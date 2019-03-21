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
        "*** YOUR CODE HERE ***"
        """
        The evaluation function's return value depends on the distance of the
        closest food from the new pacman position and the new score after the 
        action is taken.
        
        """

        # Avoid stoping
        if action == Directions.STOP:
            return -9999999

        foodList = newFood.asList()

        # This move will win the game
        if len(foodList) == 0:
            return 9999999

        # Check if a ghost is too close
        for i in range(successorGameState.getNumAgents() - 1): # -1 to exclude pacman agent
            if manhattanDistance(newPos,successorGameState.getGhostPosition(i+1)) <=1:
                return -9999999

        foodDistance = [manhattanDistance(pos,newPos) for pos in foodList]
        return -min(foodDistance) + 10*successorGameState.getScore()

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

def terminalTest(gameState):
    return gameState.isWin() or gameState.isLose()

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
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
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions
        minimaxValues = [self.minValue(gameState.generateSuccessor(0,action),1) for action in legalMoves]

        maxMinimax = max(minimaxValues)
        bestIndices = [index for index in range(len(minimaxValues)) if minimaxValues[index] == maxMinimax]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def maxValue(self, gameState, iteration):
        """
        Returns the maximum of the minimax values of the GameStates that pacman can lead to.
        """
        if terminalTest(gameState) or iteration >= self.depth*gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(0)
        minimaxValues = [self.minValue(gameState.generateSuccessor(0,action),iteration + 1) for action in legalMoves]
        
        return max(minimaxValues)

    def minValue(self, gameState, iteration):
        """
        Returns the minimum of the minimax values of the GameStates that a ghost can lead to.
        """
        numAgents = gameState.getNumAgents()
        if terminalTest(gameState) or iteration >= self.depth*numAgents:
            return self.evaluationFunction(gameState)

        agent = iteration % numAgents

        legalMoves = gameState.getLegalActions(agent)
        if agent == numAgents - 1: # The last agent calls maxValue
            minimaxValues = [self.maxValue(gameState.generateSuccessor(agent,action),iteration + 1) for action in legalMoves]
        else:
            minimaxValues = [self.minValue(gameState.generateSuccessor(agent,action),iteration + 1) for action in legalMoves]
        return min(minimaxValues)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions

        minimaxValues = []
        a = -float('inf')
        b = float('inf')
        v = -float('inf')
        bestAction = Directions.STOP
        for action in legalMoves:
            minimax = self.minValue(gameState.generateSuccessor(0,action),1,a,b)
            minimaxValues.append(minimax)
            if minimax > v:
                v = minimax
                bestAction = action
            a = max(a, minimax)
            
        bestIndices = [index for index in range(len(minimaxValues)) if minimaxValues[index] == v]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def maxValue(self, gameState, iteration, a, b):
        """
        Returns the maximum of the minimax values of the GameStates that pacman can lead to.
        """
        if terminalTest(gameState) or iteration >= self.depth*gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(0)
        v = -float('inf')
        for action in legalMoves:
            v = max(v,self.minValue(gameState.generateSuccessor(0,action),iteration + 1, a, b))
            if v > b:
                return v
            a = max(a,v)
        return v

    def minValue(self, gameState, iteration, a, b):
        """
        Returns the minimum of the minimax values of the GameStates that a ghost can lead to.
        """
        numAgents = gameState.getNumAgents()
        if terminalTest(gameState) or iteration >= self.depth*numAgents:
            return self.evaluationFunction(gameState)

        agent = iteration % numAgents

        legalMoves = gameState.getLegalActions(agent)
        v = float('inf')
        for action in legalMoves:
            if agent == numAgents - 1:
                v = min(v,self.maxValue(gameState.generateSuccessor(agent,action),iteration + 1, a, b))
            else:
                v = min(v,self.minValue(gameState.generateSuccessor(agent,action),iteration + 1, a, b))
            if v < a:
                return v
            b = min(b,v)
        return v

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
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions
        expectimaxValues = [self.expectValue(gameState.generateSuccessor(0,action),1) for action in legalMoves]

        maxExpectimax = max(expectimaxValues)
        bestIndices = [index for index in range(len(expectimaxValues)) if expectimaxValues[index] == maxExpectimax]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def maxValue(self, gameState, iteration):
        """
        Returns the maximum of the expectimax values of the GameStates that pacman can lead to.
        """
        if terminalTest(gameState) or iteration >= self.depth*gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(0)
        expectimaxValues = [self.expectValue(gameState.generateSuccessor(0,action),iteration + 1) for action in legalMoves]
        
        return max(expectimaxValues)

    def expectValue(self, gameState, iteration):
        """
        Returns the average of the expectimax values of the GameStates that a ghost can lead to, since every move has the same propability.
        """
        numAgents = gameState.getNumAgents()
        if terminalTest(gameState) or iteration >= self.depth*numAgents:
            return self.evaluationFunction(gameState)

        agent = iteration % numAgents

        legalMoves = gameState.getLegalActions(agent)
        if agent == numAgents - 1:
            expectimaxValues = [self.maxValue(gameState.generateSuccessor(agent,action),iteration + 1) for action in legalMoves]
        else:
            expectimaxValues = [self.expectValue(gameState.generateSuccessor(agent,action),iteration + 1) for action in legalMoves]
        return sum(expectimaxValues) / float(len(expectimaxValues))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
        This evaluation function is similar to the function of q1, with
        the difference that now the scared time of ghosts is taken into
        concideration.
    
        This way pacman can get better scores by eating ghosts instead
        of avoiding them.

        In order for him to do that, I made the evaluation value depend 
        on the distance to the closest capsule and sum of the ghosts' 
        scared times.
    """
    "*** YOUR CODE HERE ***"
    pacmanPosition = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsuleList = currentGameState.getCapsules()

    if len(foodList) == 0:
        return 9999999

    # Check if a ghost is too close
    ghostNear=False
    for i in range(currentGameState.getNumAgents() - 1): # -1 to exclude pacman agent
        if manhattanDistance(pacmanPosition,currentGameState.getGhostPosition(i+1)) <=1:
            return -9999999

    foodDistance = [manhattanDistance(pos,pacmanPosition) for pos in foodList]
    capsuleDistance = [manhattanDistance(pos,pacmanPosition) for pos in capsuleList]
    scaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]

    if capsuleDistance:
        return -min(capsuleDistance) + sum(scaredTimes) - min(foodDistance) + currentGameState.getScore()
    else :
        return -min(foodDistance) + currentGameState.getScore()


# Abbreviation
better = betterEvaluationFunction

