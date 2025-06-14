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
        score = successorGameState.getScore()

        # Υπολογισμός της απόστασης από την κοντινότερη τροφή
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        if foodDistances:
            score += 10.0 / min(foodDistances)  # Prioritize closer food

        # Υπολογισμός της απόστασης από κάθε φάντασμα
        for i, ghostState in enumerate(newGhostStates):
            ghostDistance = manhattanDistance(newPos, ghostState.getPosition())
            if newScaredTimes[i] > 0:
                # Αν το φάντασμα είναι φοβισμένο, ενθάρρυνση για να το φάει
                if ghostDistance > 0:
                    score += 200.0 / ghostDistance
            else:
                # Αν το φάντασμα δεν είναι φοβισμένο, αποφυγή του
                if ghostDistance > 0:
                    score -= 10.0 / ghostDistance

        # Αποθάρρυνση της παύσης, εκτός αν είναι απαραίτητο
        if action == Directions.STOP:
            score -= 5.0

        return score


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
        
        bestAction = self.minimax(gameState, 0, 0)[1]
        return bestAction

    def minimax(self, gameState, agentIndex, depth):
        # Αν το παιχνίδι τελείωσε (νίκη/ήττα) ή φτάσαμε στο μέγιστο βάθος, αξιολογούμε την κατάσταση
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        # Προσδιορισμός του αριθμού των agents
        numAgents = gameState.getNumAgents()

        # Αν είναι η σειρά του Pacman (agent μεγιστοποίησης)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        # Αν είναι η σειρά των φαντασμάτων (agent ελαχιστοποίησης)
        else:
            return self.minValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        # Αρχικοποίηση της καλύτερης τιμής ως αρνητικό άπειρο
        bestValue = float('-inf')
        bestAction = None

        # Επανάληψη στις νόμιμες ενέργειες για τον Pacman
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.minimax(successor, (agentIndex + 1) % gameState.getNumAgents(), depth if agentIndex + 1 < gameState.getNumAgents() else depth + 1)[0]
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestValue, bestAction

    def minValue(self, gameState, agentIndex, depth):
        # Αρχικοποίηση της καλύτερης τιμής ως θετικό άπειρο
        bestValue = float('inf')
        bestAction = None

        # Επανάληψη στις νόμιμες ενέργειες για το φάντασμα
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.minimax(successor, (agentIndex + 1) % gameState.getNumAgents(), depth if agentIndex + 1 < gameState.getNumAgents() else depth + 1)[0]
            if value < bestValue:
                bestValue = value
                bestAction = action

        return bestValue, bestAction

        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        bestAction = self.alphaBeta(gameState, 0, 0, float('-inf'), float('inf'))[1]
        return bestAction

    def alphaBeta(self, gameState, agentIndex, depth, alpha, beta):
        # Αν το παιχνίδι τελείωσε (νίκη/ήττα) ή φτάσαμε στο μέγιστο βάθος, αξιολογούμε την κατάσταση
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        # Προσδιορισμός του αριθμού των agents
        numAgents = gameState.getNumAgents()

        # Αν είναι η σειρά του Pacman (agent μεγιστοποίησης)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth, alpha, beta)
        # Αν είναι η σειρά των φαντασμάτων (agent ελαχιστοποίησης)
        else:
            return self.minValue(gameState, agentIndex, depth, alpha, beta)

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
        bestValue = float('-inf')
        bestAction = None

        # Επανάληψη στις νόμιμες ενέργειες για τον Pacman
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.alphaBeta(successor, (agentIndex + 1) % gameState.getNumAgents(), depth if agentIndex + 1 < gameState.getNumAgents() else depth + 1, alpha, beta)[0]
            if value > bestValue:
                bestValue = value
                bestAction = action

            # Ενημέρωση του alpha και κλάδεμα αν είναι δυνατό
            alpha = max(alpha, bestValue)
            if bestValue > beta:
                break

        return bestValue, bestAction

    def minValue(self, gameState, agentIndex, depth, alpha, beta):
        bestValue = float('inf')
        bestAction = None

        # Επανάληψη στις νόμιμες ενέργειες για το φάντασμα
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.alphaBeta(successor, (agentIndex + 1) % gameState.getNumAgents(), depth if agentIndex + 1 < gameState.getNumAgents() else depth + 1, alpha, beta)[0]
            if value < bestValue:
                bestValue = value
                bestAction = action

            # Ενημέρωση του beta και κλάδεμα αν είναι δυνατό
            beta = min(beta, bestValue)
            if bestValue < alpha:
                break

        return bestValue, bestAction
        
        util.raiseNotDefined()

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
        
        bestAction = self.expectimax(gameState, 0, 0)[1]
        return bestAction

    def expectimax(self, gameState, agentIndex, depth):
        # Αν το παιχνίδι τελείωσε (νίκη/ήττα) ή φτάσαμε στο μέγιστο βάθος, αξιολογούμε την κατάσταση
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        # Προσδιορισμός του αριθμού των agents
        numAgents = gameState.getNumAgents()

        # Αν είναι η σειρά του Pacman (agent μεγιστοποίησης)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        # Αν είναι η σειρά των φαντασμάτων (κόμβος πιθανότητας)
        else:
            return self.expValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        bestValue = float('-inf')
        bestAction = None

        # Επανάληψη στις νόμιμες ενέργειες για τον Pacman
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.expectimax(successor, (agentIndex + 1) % gameState.getNumAgents(), depth if agentIndex + 1 < gameState.getNumAgents() else depth + 1)[0]
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestValue, bestAction

    def expValue(self, gameState, agentIndex, depth):
        totalValue = 0
        actions = gameState.getLegalActions(agentIndex)
        probability = 1.0 / len(actions)

        # Επανάληψη στις νόμιμες ενέργειες για το φάντασμα
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.expectimax(successor, (agentIndex + 1) % gameState.getNumAgents(), depth if agentIndex + 1 < gameState.getNumAgents() else depth + 1)[0]
            totalValue += probability * value

        return totalValue, None

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Τρέχον σκορ του παιχνιδιού
    score = currentGameState.getScore()

    # Θέση του Pacman
    pacmanPos = currentGameState.getPacmanPosition()

    # Πλέγμα τροφής
    food = currentGameState.getFood()
    foodList = food.asList()

    # Καταστάσεις φαντασμάτων
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    # Υπολογισμός της απόστασης από την κοντινότερη τροφή
    foodDistances = [manhattanDistance(pacmanPos, foodPos) for foodPos in foodList]
    if foodDistances:
        score += 10.0 / min(foodDistances)  # Higher score for closer food

    # Υπολογισμός της απόστασης από κάθε φάντασμα
    for i, ghostState in enumerate(ghostStates):
        ghostDistance = manhattanDistance(pacmanPos, ghostState.getPosition())
        if scaredTimes[i] > 0:
            # Αν το φάντασμα είναι φοβισμένο, ενθάρρυνση για να το φάει
            if ghostDistance > 0:
                score += 200.0 / ghostDistance
        else:
            # Αν το φάντασμα δεν είναι φοβισμένο, αποφυγή του
            if ghostDistance > 0:
                score -= 10.0 / ghostDistance

    # Αριθμός power pellets που απομένουν
    capsules = currentGameState.getCapsules()
    score -= 20 * len(capsules)  

    # Αριθμός τροφίμων που απομένουν
    score -= 4 * len(foodList)

    return score
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
