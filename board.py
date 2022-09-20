
import state
from constants import *
from bitboard import getBit, clearBit, setBit
from attackPiece import genAttkPiece


def getPieceAtTile(sq):
	for key in BOARD_KEYS:
		if getBit(state.board[key], sq):
			return key

	return None



def getPieceColorAtTile(sq):
	for key in BOARD_KEYS:
		if getBit(state.board[key], sq):
			return key[0]



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
		occBboard |= state.board[key]

	return occBboard



def movePiece(start, dest):
	startPKey = getPieceAtTile(start)
	destPKey = getPieceAtTile(dest)

	if startPKey:
		moveMap = 0 if startPKey[1:] == "Pawns" else genAttkPiece(start)

		if getBit(moveMap, dest) and not (isOccupied(dest) and not canCapture(start, dest)):
			if isOccupied(dest) and canCapture(start, dest):
				state.board[destPKey] = clearBit(state.board[destPKey], dest)
			state.board[startPKey] = setBit(clearBit(state.board[startPKey], start), dest)
			return True
	return False


def placePiece(sq, pType):
	state.board[pType] = setBit(state.board[pType], sq)
