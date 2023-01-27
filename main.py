
import sys
import json
import pygame

from state import InitialStateFactory
from attackPiece import Attack
from draw import Draw
from scripts import printBboard
from constants import *


class App:
    def __init__(self):
        pygame.init()
        self.gameState = None
        self.draw = Draw()
        # MISC state
        self.selectedSquare = None
        self.toDeploy = []
        self.initStates()


    def initStates(self):
        Attack.init()
        while True: 
            initType = input("Normal init (n) or Filled board (f): ")
            if initType == "f":
                self.gameState = InitialStateFactory.TEST_PRESET()
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


    def deployment(self):
        mx, my = pygame.mouse.get_pos()
        square = 10 * ((WIN_HEIGHT - my) // TILE_HEIGHT) + (mx // TILE_WIDTH)
        if not self.gameState.board.isOccupied(square):
            res = self.gameState.board.placePiece(square, f"{self.toDeploy[-1]}s")
            if res:
                self.toDeploy.pop()

        if len(self.toDeploy) == 0:
            self.gameState.setPhase(Phase.PLAYING)
        else:
            print(f"Place {self.toDeploy[0]}")


    def playing(self):
        mx, my = pygame.mouse.get_pos()
        square = 10 * ((WIN_HEIGHT - my) // TILE_HEIGHT) + (mx // TILE_WIDTH)
        if self.gameState.board.getPieceAtTile(square) != "None":
            if self.selectedSquare != None:
                self.selectedSquare = None if self.gameState.board.movePiece(self.selectedSquare, square) else square
            else:
                self.selectedSquare = square
        else:
            self.selectedSquare = None


    def mainloop(self):
        while True:
            for event in pygame.event.get():
                # Mouse 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.gameState.phase == Phase.DEPLOYMENT: 
                        self.deployment()
                    elif self.gameState.phase == Phase.PLAYING:
                        self.playing()
                    else:
                        print("Unknown Phase.")
                    
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            self.draw.drawBoard(self.gameState.board.bboards) # Render board and pieces.


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

