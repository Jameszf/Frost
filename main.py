
import sys

import pygame
from bitarray import bitarray


pygame.init()

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 600, 600
BOARD_TILES = 10
SHEET_ROWS = 2
SHEET_COLS = 6
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = WIN_WIDTH // BOARD_TILES, WIN_HEIGHT // BOARD_TILES
SHEET_SIZE = (SHEET_COLS * TILE_WIDTH, SHEET_ROWS * TILE_HEIGHT)
BOARD_KEYS = ["wPawns", "wKnights", "wBishops", "wRooks", "wQueens", "wKings",
			  "bPawns", "bKnights", "bBishops", "bRooks", "bQueens", "bKings"]

# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
DARK_TILE = 148, 111, 81
LIGHT_TILE = 240, 214, 181



class Bitboard:
	def __init__(self):
		self.barray = 0
		self.piece_key = ""


	@staticmethod
	def make_bitboard(pos_list, piece_key):
		bboard = Bitboard()
		bboard.piece_key = piece_key

		for pos in pos_list:
			bboard.setBit(pos)

		return bboard


	def flipBit(self, pos): self.barray ^= (1 << pos) # Flip bit at pos.
	def setBit(self, pos): self.barray |= (1 << pos) # Set bit at pos to be 1.
	def clearBit(self, pos): self.barray &= ~(1 << pos) # Set bit at pos to be 0.
	def getBit(self, pos): return self.barray & (1 << pos)
		


def defaultBoard():
	"""
	Generates bitboards of the starting position of a regular chess game.

	INPUT: void.
	OUTPUT: List<Bitboard>.
	"""

	piecePos = {
	    "wPawns": [8, 9, 10, 11, 12, 13, 14, 15],
		"wKnights": [1, 6],
		"wBishops": [2, 5],
		"wRooks": [0, 7],
		"wQueens": [3],
		"wKings": [4],
		"bPawns": [48, 49, 50, 51, 52, 53, 54, 55],
		"bKnights": [57, 62],
		"bBishops": [58, 61],
		"bRooks": [56, 63],
		"bQueens": [59],
		"bKings": [60]
	}
	
	return {key: Bitboard.make_bitboard(piecePos[key], key) for key in BOARD_KEYS }



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
