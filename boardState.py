
from gameVars import *
from bitboard import getBit, clearBit, setBit



def getPieceAtTile(sq):
	for key in BOARD_KEYS:
		if getBit(g_board[key], sq):
			return key

	return None



def isOccupied(sq):
	occ = getOccBboard()
	return getBit(occ, sq)



def canCapture(sq1, sq2):
	p1 = getPieceAtTile(sq1)
	p2 = getPieceAtTile(sq2)

	return p1[0] != p2[0]



def getOccBboard():
	occBboard = 0
	for key in BOARD_KEYS:
		occBboard |= g_board[key]

	return occBboard



