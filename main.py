
import sys
import json
import pygame

import state
import draw
import board
from scripts import printBboard
from constants import *



def customInit():
	initType = input("Normal init (n) or Filled board (f): ")

	if initType == "f":
		state.init(emptyBoard=False)
		state.playingPhase()
	else:
		state.init(emptyBoard=True)



def main():
	pygame.init()
	customInit()

	clock = pygame.time.Clock()

	# Event loop.
	selSq = None
	toDeploy = ["wRook", "wRook", "wRook", "bRook", "bRook", "bRook",
				"wBishop", "wBishop", "wBishop", "bBishop", "bBishop", "bBishop",
				"wKnight", "wKnight", "bKnight", "bKnight",
				"wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn",
				"bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn",
				"wQueen", "bQueen",
				"wKing", "bKing"]

	if state.phase == "deployment": print(f"Place {toDeploy[0]}")

	while True:
		for event in pygame.event.get():
			# Mouse 
			if event.type == pygame.MOUSEBUTTONDOWN:
				mx, my = pygame.mouse.get_pos()
				sq = 10 * ((WIN_HEIGHT - my) // TILE_HEIGHT) + (mx // TILE_WIDTH)
				if state.phase == "deployment":
					if not board.isOccupied(sq):
						board.placePiece(sq, f"{toDeploy[0]}s")
						toDeploy.pop(0)

						if len(toDeploy) == 0:
							state.playingPhase()
						else:
							print(f"Place {toDeploy[0]}")
					else:
						print("Square is occupied!")
				else:
					if board.getPieceAtTile(sq) != "None":
						if selSq != None:
							selSq = None if board.movePiece(selSq, sq) else sq
						else:
							selSq = sq
					else:
						selSq = None
					

			if event.type == pygame.QUIT:
				pygame.display.quit()
				sys.exit()
		
		state.screen.fill(GREEN) # Clear previous frame.
		draw.drawBoard() 
		pygame.display.flip() # Render new frame.
		clock.tick(60) # Locked to 60 FPS.



if __name__ == "__main__":
	main()
