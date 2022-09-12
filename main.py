
import sys
import json

import pygame

from gameVars import *
from bitboard import *
from scripts import printBboard


pygame.init()


def isNegDir(rDir):
	return rDir == "W" or rDir == "SW" or rDir == "S" or rDir == "SE"



def genBlckAttkRay(rayDir, sq):
	occBboard = getOccBboard()
	blockers = (occBboard & g_attkRayTbl[rayDir][sq]) ^ (1 << sq)
	blckRay = g_attkRayTbl[rayDir][sq]

	if blockers != 0:
		# print("Blockers")
		# printBboard(blockers)
		fstBlockerSq = rBitscan(blockers) if isNegDir(rayDir) else fBitscan(blockers)
		# print(f"Bitscan result {fstBlockerSq}")
		rmRay = g_attkRayTbl[rayDir][fstBlockerSq] ^ (1 << fstBlockerSq)
		blckRay ^= rmRay

	return blckRay



def getPieceAtTile(sq):
	for key in BOARD_KEYS:
		if getBit(g_board[key], sq):
			return key

	return None


def getOccBboard():
	occBboard = 0
	for key in BOARD_KEYS:
		occBboard |= g_board[key]

	return occBboard




def genKingAttkPiece(sq):
	notAFile = 0xFFBFEFFBFEFFBFEFFBFEFFBFE
	notJFile = 0x7FDFF7FDFF7FDFF7FDFF7FDFF
	inBounds = 0xFFFFFFFFFFFFFFFFFFFFFFFFF

	north = (0x400 << sq) & inBounds
	south = 0x20000000000000000000000 >> (99 - sq)
	east = (0x2 << sq) & notAFile
	west = (0x4000000000000000000000000 >> (99 - sq)) & notJFile

	northEast = (0x800 << sq) & notAFile
	northWest = (0x1000000000000000000000000000 >> (99 - sq)) & notJFile
	southEast = (0x80000000000000000000000 >> (100 - sq)) & notAFile
	southWest = (0x10000000000000000000000 >> (99 - sq)) & notJFile

	kingSq = 1 << sq

	return kingSq | north | south | east | west | northEast | northWest | southEast | southWest



def genKnightAttkPiece(sq):
	notAFile = 0xFFBFEFFBFEFFBFEFFBFEFFBFE
	notJFile = 0x7FDFF7FDFF7FDFF7FDFF7FDFF
	notABFiles = 0xFF3FCFF3FCFF3FCFF3FCFF3FC
	notIJFiles = 0x3FCFF3FCFF3FCFF3FCFF3FCFF
	inBounds = 0xFFFFFFFFFFFFFFFFFFFFFFFFF

	noNoEa = (0x200000 << sq) & notAFile
	noNoWe = (0x400000000000000000000000000000 >> (99 - sq)) & notJFile

	noEaEa = (0x1000 << sq) & notABFiles
	soEaEa = (0x100000000000000000000000 >> (100 - sq)) & notABFiles

	soSoEa = (0x200000000000000000000 >> (100 - sq)) & notAFile
	soSoWe = (0x40000000000000000000 >> (99 - sq)) & notJFile

	soWeWe = (0x8000000000000000000000 >> (99 - sq)) & notIJFiles
	noWeWe = (0x800000000000000000000000000 >> (99 - sq)) & notIJFiles

	knightSq = 1 << sq

	return knightSq | noNoEa | noNoWe | noEaEa | soEaEa | soSoEa | soSoWe | soWeWe | noWeWe



def genPawnAttkPiece(sq):
	notAFile = 0xFFBFEFFBFEFFBFEFFBFEFFBFE
	notJFile = 0x7FDFF7FDFF7FDFF7FDFF7FDFF

	northEast = (0x800 << sq) & notAFile
	northWest = (0x1000000000000000000000000000 >> (99 - sq)) & notJFile

	return northEast | northWest




def genAttkPiece(sq):
	print(f"Generating Attack Piece Bitboard for piece at square #{sq}")
	print(f"Piece occupying that tile: {getPieceAtTile(sq)}")

	pType = getPieceAtTile(sq)
	pType = pType[1:] if pType else "None"

	# Sliding pieces
	attkPiece = 0
	if pType == "Queens" or pType == "Rooks" or pType == "Bishops":
		rDir = {
			"Queens": ["NW", "N", "NE", "E", "SE", "S", "SW", "W"],
			"Rooks": ["N", "E", "S", "W"],
			"Bishops": ["NW", "NE", "SE", "SW"]
		}
		for rd in rDir[pType]:
			blckRay = genBlckAttkRay(rd, sq)
			attkPiece |= blckRay
	elif pType == "Knights":
		attkPiece = genKnightAttkPiece(sq)
	elif pType == "Pawns":
		attkPiece = genPawnAttkPiece(sq)
	elif pType == "Kings":
		attkPiece = genKingAttkPiece(sq)
	else:
		pass
	
	print("Attack Piece generated")
	printBboard(attkPiece)



def defaultBoard():
	"""
	Generates bitboards of the starting position of a regular chess game.

	INPUT: void.
	OUTPUT: List<Bitboard>.
	"""

	global g_board

	# DEFAULT BOARD
	# return {
	#     "wPawns": 0,
	# 	"wKnights": 0,
	# 	"wBishops": 0,
	# 	"wRooks": 0,
	# 	"wQueens": 0,
	# 	"wKings": 0,
	# 	"bPawns": 0,
	# 	"bKnights": 0,
	# 	"bBishops": 0,
	# 	"bRooks": 0,
	# 	"bQueens": 0,
	# 	"bKings": 0,
	# }

	# TESTING BOARD
	board = {}
	with open("testBoard.txt", "r") as f:
		for pType in BOARD_KEYS:
			board[pType] = int(f.readline()[:-2], 2)

	g_board = board 




def drawTiles():
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
			pygame.draw.rect(g_screen, color, (tx, ty, tx + TILE_WIDTH, ty + TILE_HEIGHT))



def drawPieces():
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
			if getBit(g_board[key], i):
				x = (i % BOARD_TILES) * TILE_WIDTH
				y = ((BOARD_TILES - 1) - i // BOARD_TILES) * TILE_HEIGHT
				g_screen.blit(g_sheet, (x, y), area=spritePos[key])



def drawBoard():
	"""
	Main rendering function of game. Rendering order MATTERS. 
	LAYERS order: tiles --> pieces.

	INPUT: screen (pygame display object), board (bitboard), sheet (pygame sprite object).
	OUTPUT: void.
	"""

	drawTiles()
	drawPieces()



def loadGameVars():
	global g_sheet, g_screen, g_attkRayTbl
	with open("attackRays.json", "r") as f:
		g_attkRayTbl = json.load(f)

	defaultBoard()

	g_screen = pygame.display.set_mode(WIN_SIZE)

	# Load pieces sprite sheet.
	g_sheet = pygame.image.load("assets/pieces.png").convert_alpha()
	g_sheet = pygame.transform.smoothscale(g_sheet, SHEET_SIZE)



def main():
	loadGameVars()

	clock = pygame.time.Clock()

	# Event loop.
	while True:
		for event in pygame.event.get():
			# Mouse 
			if event.type == pygame.MOUSEBUTTONDOWN:
				print("Mouse clicked", event)
				mx, my = pygame.mouse.get_pos()
				boardx = mx // TILE_WIDTH
				boardy = (WIN_HEIGHT - my) // TILE_HEIGHT
				genAttkPiece(boardy * 10 + boardx)

			if event.type == pygame.QUIT:
				pygame.display.quit()
				sys.exit()
		
		g_screen.fill(GREEN) # Clear previous frame.
		drawBoard() # Render new frame.
		pygame.display.flip() 
		clock.tick(60) # Locked to 60 FPS.



if __name__ == "__main__":
	main()
