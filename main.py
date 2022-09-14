
import sys
import json
import pygame

import state
import draw
import board
from scripts import printBboard
from constants import *



def main():
	pygame.init()
	state.init()

	clock = pygame.time.Clock()

	# Event loop.
	selSq = None
	while True:
		for event in pygame.event.get():
			# Mouse 
			if event.type == pygame.MOUSEBUTTONDOWN:
				mx, my = pygame.mouse.get_pos()
				sq = 10 * ((WIN_HEIGHT - my) // TILE_HEIGHT) + (mx // TILE_WIDTH)
				if board.getPieceAtTile(sq) != "None":
					if selSq != None:
						print("Possible movePiece()")
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
