
import sys
import json
import pygame
from typing import List

from frost.state import InitialStateFactory, GameState
from frost.attackPiece import Attack
from frost.draw import Draw
from frost.scripts import printBboard
from frost.customTypes import *


class App:
    def __init__(self) -> None:
        pygame.init()
        self.gameState: GameState
        self.draw: Draw = Draw()
        # MISC state
        self.selectedSquare: int = -1
        self.toDeploy: List[str] = []
        self.mouseDown: bool = False
        self.dragging: bool = True
        self.initStates()


    def initStates(self) -> None:
        Attack.init()
        while True: 
            initType: str = input("Normal init (n) or Filled board (f): ")
            if initType == "f":
                self.gameState = InitialStateFactory.TEST_PRESET()
                self.draw.syncPieces(self.gameState.board.bboards)
                break
            elif initType == "n":
                self.gameState = InitialStateFactory.NORMAL()
                self.toDeploy = ["bKing", "wKing",
                            "bQueen", "wQueen",
                            "bRook", "bRook", "bRook", "wRook", "wRook", "wRook",
                            "bBishop", "bBishop", "bBishop", "wBishop", "wBishop", "wBishop", 
                            "bKnight", "bKnight", "wKnight", "wKnight",
                            "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn",
                            "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn"]
                break
            else:
                print(f"Unrecognized option '{initType}'. Please choose a valid option.")


    def deployment(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx: int
            my: int
            mx, my = pygame.mouse.get_pos()
            square: int  = 10 * ((Draw.WIN_HEIGHT - my) // Draw.TILE_HEIGHT) + (mx // Draw.TILE_WIDTH)
            if not self.gameState.board.isOccupied(square):
                res: bool = self.gameState.board.placePiece(square, f"{self.toDeploy[-1]}s")
                self.draw.syncPieces(self.gameState.board.bboards)
                if res:
                    self.toDeploy.pop()

            if len(self.toDeploy) == 0:
                self.gameState.setPhase(Phase.PLAYING)
            else:
                print(f"Place {self.toDeploy[0]}")


    def playing(self, event) -> None:
        mx: int
        my: int
        mx, my = pygame.mouse.get_pos()
        square: int  = 10 * ((Draw.WIN_HEIGHT - my) // Draw.TILE_HEIGHT) + (mx // Draw.TILE_WIDTH)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseDown = True
            if self.gameState.board.getPieceAtTile(square) != "None":
                if self.selectedSquare != -1:
                    self.selectedSquare = -1 if self.gameState.board.movePiece(self.selectedSquare, square) else square
                    self.draw.syncPieces(self.gameState.board.bboards)
                else:
                    self.selectedSquare = square
            else:
                self.selectedSquare = -1
        elif event.type == pygame.MOUSEMOTION:
            if self.mouseDown and self.selectedSquare != -1:
                newX = mx - Draw.TILE_WIDTH // 2
                newY = my - Draw.TILE_HEIGHT // 2 
                self.draw.moveVisualPiece(self.selectedSquare, newX, newY)
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            print("Mouse Up")
            self.mouseDown = False
            if self.dragging:
                print(square)
                if self.gameState.board.movePiece(self.selectedSquare, square):
                    print("Successful move")
                    self.selectedSquare = -1
                    self.draw.syncPieces(self.gameState.board.bboards)
                else:
                    print("Reposition piece to original square")
                    originalX = (self.selectedSquare % Draw.BOARD_TILES) * Draw.TILE_WIDTH
                    originalY = (Draw.BOARD_TILES - 1 - self.selectedSquare // Draw.BOARD_TILES) * Draw.TILE_HEIGHT
                    self.draw.moveVisualPiece(self.selectedSquare, originalX, originalY)
                self.dragging = False
                    

    def mainloop(self) -> None:
        while True:
            for event in pygame.event.get():
                if self.gameState.phase == Phase.DEPLOYMENT:
                    self.deployment(event)
                elif self.gameState.phase == Phase.PLAYING:
                    self.playing(event)
                else:
                    print("Unknown Phase.")

                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            self.draw.drawBoard(self.selectedSquare) # Render board and pieces.


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

