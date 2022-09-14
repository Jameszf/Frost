
import json
import pygame

from constants import *



# GAME STATE
# =====================================================================================
def init():
	global sheet, screen, attkRayTbl, board
	with open("attackRays.json", "r") as f:
		attkRayTbl = json.load(f)

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

	screen = pygame.display.set_mode(WIN_SIZE)

	# Load pieces sprite sheet.
	sheet = pygame.image.load("assets/pieces.png").convert_alpha()
	sheet = pygame.transform.smoothscale(sheet, SHEET_SIZE)


