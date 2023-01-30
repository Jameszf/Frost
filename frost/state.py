
from frost.board import Board
from frost.constants import *


class InitialStateFactory:
    def NORMAL():
        gameState = InitialStateFactory.__BASE("./frost/emptyBoard.txt")
        gameState.turn = Turn.WHITE
        gameState.phase = Phase.DEPLOYMENT
        return gameState

    def TEST_PRESET():
        gameState = InitialStateFactory.__BASE("./frost/randomBoard.txt")
        gameState.turn = Turn.WHITE
        gameState.phase = Phase.PLAYING
        return gameState
        
    def __BASE(boardFile):
        state = GameState()
        with open(boardFile, "r") as f:
            bboards = {}
            for pType in Board.KEYS:
                bboards[pType] = int(f.readline()[:-2], 2)
            state.board = Board(bboards)
        return state


class GameState:
    def __init__(self):
        self.board = None
        self.turn = None
        self.phase = None

    def toggleTurn(self):
        self.turn = Turn.WHITE if self.turn == Turn.BLACK else Turn.BLACK
        
    def setPhase(self, phase):
        self.phase = phase
    
