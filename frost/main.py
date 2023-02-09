
import sys
import json
import pygame
from typing import List

from frost.state import InitialStateFactory, GameState
from frost.attackPiece import Attack
from frost.draw import Draw
from frost.scripts import printBboard
from frost.customTypes import *


# class EventHandler:


class App:
    """
    Primary class for one game instance. This includes game logic, window,
    and (eventually) an computer engine instance. Each App instance's processes
    (such as rendering and event handling) would be separated from one another.
    """
    def __init__(self) -> None:
        pygame.init()
        self.gameState: GameState
        self.draw: Draw = Draw()
        # Development phase state variables.
        self.toDeploy: List[str] = []
        # Playing phase state variables.
        self.selectedSquare: int = -1
        self.mouseDown: bool = False
        self.dragging: bool = True
        self.initStates()


    def initStates(self) -> None:
        """
        Prompt user for a desired board setup and initialize their corresponding initial states.
        """
        Attack.init()
        while True: 
            initType: str = input("Normal init (n) or Filled board (f): ")
            if initType == "f": # Setup with filled board
                self.gameState = InitialStateFactory.TEST_PRESET()
                self.draw.syncPieces(self.gameState.board.bboards)
                break
            elif initType == "n": # Normal Setup
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
        """
        Handles events for deployment phase. This handler will try to place a piece whenever MOUSEBUTTONDOWN
        event is emitted. Piece placement order is determined by self.toDeploy. Once all pieces are placed
        (i.e. len(self.toDeploy) == 0) then playing phase will start.

        TODO make this into a class (EventHandler).
        """
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
        """
        Event handler during playing phase. Currently handles square selection, piece dragging,
        and piece moves/captures. Does not respond to any keyboard inputs.

        event :: A pygame event emitted during runtime of program.

        TODO make this into a class (EventHandler).
        """
        mouseX: int
        mouseY: int
        mouseX, mouseY = pygame.mouse.get_pos()
        square: int  = 10 * ((Draw.WIN_HEIGHT - mouseY) // Draw.TILE_HEIGHT) + (mouseX // Draw.TILE_WIDTH)

        if event.type == pygame.MOUSEBUTTONDOWN: # Square selection.
            self.mouseDown = True
            if self.gameState.board.getPieceAtTile(square) != "None": # Square unoccupied
                if self.selectedSquare != -1 and self.selectedSquare != square:
                    self.gameState.board.movePiece(self.selectedSquare, square)
                    self.selectedSquare = -1
                    self.draw.syncPieces(self.gameState.board.bboards)
                else:
                    self.selectedSquare = square
            else:
                self.selectedSquare = -1

        elif event.type == pygame.MOUSEMOTION: # Dragging pieces.
            if self.mouseDown and self.selectedSquare != -1:
                # Reposition visual piece to be centered on cursor during a drag.
                # This does not change board (state of the piece is still on square before start of the drag).
                newX = mouseX - Draw.TILE_WIDTH // 2
                newY = mouseY - Draw.TILE_HEIGHT // 2 
                self.draw.moveVisualPiece(self.selectedSquare, newX, newY) 
                self.draw.drawPieceLast(self.selectedSquare)
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP: # End of drag.
            print("Mouse Up")
            self.mouseDown = False
            if self.dragging:
                print(square)
                if self.gameState.board.movePiece(self.selectedSquare, square):
                    # Successful drag -> sync pieces with updated board state.
                    print("Successful drag")
                    self.draw.syncPieces(self.gameState.board.bboards)
                else:
                    # Unsuccessful drag -> send visual piece back to original square (before the drag).
                    print("Unsuccesful drag")
                    originalX = (self.selectedSquare % Draw.BOARD_TILES) * Draw.TILE_WIDTH
                    originalY = (Draw.BOARD_TILES - 1 - self.selectedSquare // Draw.BOARD_TILES) * Draw.TILE_HEIGHT
                    self.draw.moveVisualPiece(self.selectedSquare, originalX, originalY)
                self.dragging = False
                self.selectedSquare = -1
                    

    def mainloop(self) -> None:
        """
        Main program loop. Every game tick the following happens:
         1. Handle events + Update game state.
         2. Draw board and new game state (maximum: 60fps).
        """
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

