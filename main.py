
import sys

import pygame
from bitarray import bitarray
from constants import *
from bitboard import Bitboard


pygame.init()


def defaultBoard():
	"""
	Generates bitboards of the starting position of a regular chess game.

	INPUT: void.
	OUTPUT: List<Bitboard>.
	"""

	piecePos = {
	    "wPawns": 0,
		"wKnights": 0,
		"wBishops": 0,
		"wRooks": 0,
		"wQueens": 0,
		"wKings": 0,
		"bPawns": 0,
		"bKnights": 0,
		"bBishops": 0,
		"bRooks": 0,
		"bQueens": 0,
		"bKings": 0,
	}
	
	return {key: Bitboard.makeBitboard(piecePos[key]) for key in BOARD_KEYS }



def drawTiles(screen):
	"""
	Draws BOARD_TILES by BOARD_TILES checkerboard on screen

	INPUT: screen (pygame display object).
	OUTPUT: void.
	"""

	for y in range(BOARD_TILES):
		for x in range(BOARD_TILES):
			if (x + y) % 2 == 0:
				color = LIGHT_TILE
			else:
				color = DARK_TILE
		
			tx = x * TILE_WIDTH
			ty = y * TILE_WIDTH
			pygame.draw.rect(screen, color, (tx, ty, tx + TILE_WIDTH, ty + TILE_HEIGHT))



def drawPieces(screen, bboards, sheet):
	"""
	Draws chess pieces according to board using sprites from sheet

	INPUT: screen (pygame display object), bboards (List<Bitboard>), sheet (pygame sprite object).
	OUTPUT: void.
	"""

	spritePos = {
		"wPawns": (5 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
		"wKnights": (3 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
		"wBishops": (2 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
		"wRooks": (4 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
		"wQueens": (TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
		"wKings": (0, 0, TILE_WIDTH, TILE_HEIGHT),

		"bPawns": (5 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
		"bKnights": (3 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
		"bBishops": (2 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
		"bRooks": (4 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
		"bQueens": (TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
		"bKings": (0, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
	}

	
	for key in BOARD_KEYS:
		for i in range(BOARD_TILES ** 2):
			if bboards[key].getBit(i):
				x = (i % 8) * TILE_WIDTH
				y = (7 - i // 8) * TILE_HEIGHT
				screen.blit(sheet, (x, y), area=spritePos[key])



def drawBoard(screen, board, sheet):
	"""
	Main rendering function of game. Rendering order MATTERS. 
	LAYERS order: tiles --> pieces.

	INPUT: screen (pygame display object), board (bitboard), sheet (pygame sprite object).
	OUTPUT: void.
	"""

	drawTiles(screen)
	drawPieces(screen, board, sheet)



def main():
	board = defaultBoard() # Get starting board state.

	screen = pygame.display.set_mode(WIN_SIZE)
	clock = pygame.time.Clock()

	# Load piece sprite sheet.
	sheet = pygame.image.load("assets/pieces.png").convert_alpha()
	sheet = pygame.transform.smoothscale(sheet, SHEET_SIZE)

	# Event loop.
	while True:
		for event in pygame.event.get():
			# Mouse 
			if event.type == pygame.MOUSEBUTTONDOWN:
				print("Mouse clicked", event)

			if event.type == pygame.QUIT:
				pygame.display.quit()
				sys.exit()
		
		screen.fill(GREEN) # Clear previous frame.
		drawBoard(screen, board, sheet) # Render new frame.
		pygame.display.flip() 
		clock.tick(60) # Locked to 60 FPS.



if __name__ == "__main__":
	main()
