
import typing 

from frost.board import Board
from frost.constants import *


class InitialStateFactory:
    def NORMAL():
        gameState: GameState = InitialStateFactory.__BASE("./frost/emptyBoard.txt")
        gameState.turn = Turn.WHITE
        gameState.phase = Phase.DEPLOYMENT
        return gameState

    def TEST_PRESET():
        gameState: GameState = InitialStateFactory.__BASE("./frost/randomBoard.txt")
        gameState.turn = Turn.WHITE
        gameState.phase = Phase.PLAYING
        return gameState
        
    def __BASE(boardFile):
        state: GameState = GameState()
        with open(boardFile, "r") as f:
            bboards: Dict[str, int] = {}
            for pType in Board.KEYS:
                bboards[pType] = int(f.readline()[:-2], 2)
            state.board = Board(bboards)
        return state


class GameState:
    def __init__(self):
        self.board: Board = None
        self.turn: str = None
        self.phase: str = None

    def toggleTurn(self):
        self.turn = Turn.WHITE if self.turn == Turn.BLACK else Turn.BLACK
        
    def setPhase(self, phase):
        self.phase = phase
    
