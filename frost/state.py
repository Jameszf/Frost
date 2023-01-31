
from typing import Dict

from frost.board import Board
from frost.constants import *


class GameState:
    def __init__(self) -> None:
        self.board: Board
        self.turn: Turn
        self.phase: Phase

    def toggleTurn(self) -> None:
        self.turn = Turn.WHITE if self.turn == Turn.BLACK else Turn.BLACK
        
    def setPhase(self, phase: Phase) -> None:
        self.phase = phase


class InitialStateFactory:
    @staticmethod
    def NORMAL() -> GameState:
        gameState: GameState = InitialStateFactory.__BASE("./frost/emptyBoard.txt")
        gameState.turn = Turn.WHITE
        gameState.phase = Phase.DEPLOYMENT
        return gameState

    @staticmethod
    def TEST_PRESET() -> GameState:
        gameState: GameState = InitialStateFactory.__BASE("./frost/randomBoard.txt")
        gameState.turn = Turn.WHITE
        gameState.phase = Phase.PLAYING
        return gameState
        
    @staticmethod
    def __BASE(boardFile) -> GameState:
        state: GameState = GameState()
        with open(boardFile, "r") as f:
            bboards: Dict[str, int] = {}
            for pType in Board.KEYS:
                bboards[pType] = int(f.readline()[:-2], 2)
            state.board = Board(bboards)
        return state

