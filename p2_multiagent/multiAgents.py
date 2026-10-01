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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        #Eval food 
        newFood = successorGameState.getFood().asList()
        closest_food = float('inf')
        for dist in newFood:
            food_dist = util.manhattanDistance(dist, newPos)
            if (food_dist < closest_food):
                closest_food = food_dist

        for dist in successorGameState.getGhostPositions():
            ghost_dist = util.manhattanDistance(dist, newPos)
            if (ghost_dist <= 2):
                return float('-inf')

        return successorGameState.getScore() + 1.0/closest_food
        #return ghost_dist
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #use current gameState -> self.depth and self.evaluationFunction to find the best action
        bestScore = float('-inf')
        bestAction = None
        #return the max bc pacman goes first & return action
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = self.value(successor, 1, 0)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction
 
        #util.raiseNotDefined()
 
    def value (self, gameState, currAgent, currDepth):
         #base case: game is over or reached certain depth 
         if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
             return self.evaluationFunction(gameState)
         # agent 0 is pacman -> max
         if currAgent == 0:
             return self.maxVal(gameState, currAgent, currDepth)
         # agents >= 1 are ghosts -> min
         return self.minVal(gameState, currAgent, currDepth)
 
    def minVal(self, gameState, currAgent, currDepth):
        #initalize v
        v = float('inf')
        #for each successor: v = min(v, value(successor))
        for action in gameState.getLegalActions(currAgent):
            #calculate the next agent and depth
            successor = gameState.generateSuccessor(currAgent, action)
            nextAgent = (currAgent + 1) % gameState.getNumAgents() # use mod to go back to pacman after all ghosts
            nextDepth = currDepth + (1 if nextAgent == 0 else 0) # only add if the next agent is pacman because that means it wrapped around to create a new depth
            #take the min
            v = min(v, self.value(successor, nextAgent, nextDepth))
        return v

    def maxVal(self, gameState, currAgent, currDepth):
        #initalize v neg inf
        v = float('-inf')
        for action in gameState.getLegalActions(currAgent):
            successor = gameState.generateSuccessor(currAgent, action)
            nextAgent = (currAgent + 1) % gameState.getNumAgents()
            nextDepth = currDepth + (1 if nextAgent == 0 else 0)
            #taking max
            v = max(v, self.value(successor, nextAgent, nextDepth))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #initilaizing vlaues
        alpha = float('-inf')
        beta = float('inf')
        bestScore = float('-inf')
        bestAction = None

        #do same as the minimax but remember to keep track of alpha and beta
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = self.value(successor, 1, 0, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            #alpha = max(alpha, v)
            alpha = max(alpha, score)
        return bestAction
            
        #util.raiseNotDefined()

    def value(self, gameState, currAgent, currDepth, alpha, beta):
        #this is all the same as the minimax but with alpha and beta
        if (gameState.isLose() or gameState.isWin() or currDepth == self.depth):
            return self.evaluationFunction(gameState)
        if currAgent == 0:
            return self.maxVal(gameState, currAgent, currDepth, alpha, beta)
        # agents >= 1 are ghosts -> min
        return self.minVal(gameState, currAgent, currDepth, alpha, beta)

    def minVal(self, gameState, currAgent, currDepth, alpha, beta):
        v = float('inf')
        for action in gameState.getLegalActions(currAgent):
            successor = gameState.generateSuccessor(currAgent, action)
            nextAgent = (currAgent + 1) % gameState.getNumAgents()
            nextDepth = currDepth + (1 if nextAgent == 0 else 0)
            v = min(v, self.value(successor, nextAgent, nextDepth, alpha, beta))
            #prune if the current value is worse than alpha ( NO EQUALS!!!!!!!!!!!!!!!!!!!!!!!!!!)
            if v < alpha:
                return v
            #update beta to min of the current beta and current value
            beta = min(beta, v)
        return v

    def maxVal(self, gameState, currAgent, currDepth, alpha, beta):
        #everything flipped from min
        v = float('-inf')
        for action in gameState.getLegalActions(currAgent):
            successor = gameState.generateSuccessor(currAgent, action)
            nextAgent = (currAgent + 1) % gameState.getNumAgents()
            nextDepth = currDepth + (1 if nextAgent == 0 else 0)
            v = max(v, self.value(successor, nextAgent, nextDepth, alpha, beta))
            #prune if the current value is BETTER than beta
            if v >beta:
                return v
            #update alpha to MAX
            alpha = max(alpha, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        maxDepth = (self.depth) * (gameState.getNumAgents())
        
        return self.expectimax(gameState, "expect", maxDepth, 0)[0]
        #util.raiseNotDefined()

    def expectimax(self, gameState, action, depth, agentIndex):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return (action, self.evaluationFunction(gameState))

        if agentIndex == 0:
            return self.maxValue(gameState, action, depth, agentIndex)
        else:
            return self.expValue(gameState, action, depth, agentIndex)

    def maxValue(self, gameState, action, depth, agentIndex):
        bestAction = ("max", -(float('inf')))

        for laction in gameState.getLegalActions(agentIndex):
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            succAction = None
            if depth != self.depth * gameState.getNumAgents():
                succAction = action
            else:
                succAction = laction
            succValue = self.expectimax(gameState.generateSuccessor(agentIndex, laction), succAction, depth - 1, nextAgent)
            bestAction = max(bestAction, succValue, key = lambda x:x[1])

        return bestAction
    
    def expValue(self,gameState,action,depth,agentIndex):
        lActions = gameState.getLegalActions(agentIndex)
        averageScore = 0
        prob = 1.0/len(lActions)
        for laction in lActions:
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            bestAction = self.expectimax(gameState.generateSuccessor(agentIndex, laction), action, depth - 1, nextAgent)
            averageScore += bestAction[1] * prob

        return (action, averageScore)


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = 0
    
    foodLeft = currentGameState.getNumFood()
    foodLeftMult = 10
    score += 1.0 / (foodLeft * foodLeftMult)
    #Look at how much food is left
    
    return score
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction