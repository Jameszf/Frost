
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


	@staticmethod
	def makeBitboard(barray=0):
		bboard = Bitboard()
		bboard.barray = barray
		return bboard


	# Bit manipulation
	def flipBit(self, pos): self.barray ^= (1 << pos) # Flip bit at pos.
	def setBit(self, pos): self.barray |= (1 << pos) # Set bit at pos to be 1.
	def clearBit(self, pos): self.barray &= ~(1 << pos) # Set bit at pos to be 0.
	def getBit(self, pos): return (self.barray & (1 << pos)) != 0

	def union(self, bboard): self.barray |= bboard.barray
	def insect(self , bboard): self.barray &= bboard.barray
	def xor(self, bboard): self.barray ^= bboard.barray


	# bitscans
	def fbitscan(self):
		"""
		128-bit Forward bitscan implementation using De Brujin multiplication.

		Details: https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication	
		"""
		assert self.barray != 0

		index = [0, 1, 2, 8, 3, 15, 9, 22, 4, 29,
				  16, 36, 10, 43, 23, 50, 5, 33, 30,
				  57, 17, 64, 37, 71, 11, 60, 44, 78,
				  24, 85, 51, 92, 6, 20, 34, 48, 31,
				  69, 58, 90, 18, 67, 65, 99, 38, 101,
				  72, 106, 12, 40, 61, 82, 45, 103, 79,
				  113, 25, 74, 86, 116, 52, 108, 93, 120,
				  127, 7, 14, 21, 28, 35, 42, 49, 32, 56,
				  63, 70, 59, 77, 84, 91, 19, 47, 68, 89,
				  66, 98, 100, 105, 39, 81, 102, 112, 73,
				  115, 107, 119, 126, 13, 27, 41, 55, 62,
				  76, 83, 46, 88, 97, 104, 80, 111, 114,
				  118, 125, 26, 54, 75, 87, 96, 110, 117,
				  124, 53, 95, 109, 123, 94, 122, 121]
		debrujin = 0x1061438916347932A5CD9D3EAD7B77F 
		ls1b = self.barray & -self.barray
		return index[((debrujin * ls1b) & 0xFE000000000000000000000000000000) >> 121]



	def rbitscan(self):
		index = [0, 69, 1, 27, 70, 113, 2, 13, 28, 97,
				 71, 55, 114, 17, 3, 124, 14, 83, 29,
				 41, 98, 86, 72, 65, 56, 46, 115, 60,
				 18, 32, 4, 125, 111, 95, 15, 81, 84,
				 44, 30, 109, 42, 107, 99, 50, 87, 101,
				 73, 66, 52, 38, 57, 92, 47, 89, 116,
				 23, 61, 103, 19, 119, 33, 75, 5, 126,
				 68, 26, 112, 12, 96, 54, 16, 123, 82,
				 40, 85, 64, 45, 59, 31, 110, 94, 80,
				 43, 108, 106, 49, 100, 51, 37, 91, 88,
				 22, 102, 118, 74, 67, 25, 11, 53, 122,
				 39, 63, 58, 93, 79, 105, 48, 36, 90,
				 21, 117, 24, 10, 121, 62, 78, 104, 35,
				 20, 9, 120, 77, 34, 8, 76, 7, 6, 127]

		debrujin = 0x1FC47709ECA6B19CC17D25B45754379
		
		ms = self.barray
		ms |= ms >> 1
		ms |= ms >> 2
		ms |= ms >> 4
		ms |= ms >> 8
		ms |= ms >> 16
		ms |= ms >> 32
		ms |= ms >> 64

		return index[((debrujin * ms) & 0xFE000000000000000000000000000000) >> 121]
		


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
