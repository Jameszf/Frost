
from boardState import getOccBboard
from gameVars import *
from scripts import printBboard


notAFile = 0xFFBFEFFBFEFFBFEFFBFEFFBFE
notJFile = 0x7FDFF7FDFF7FDFF7FDFF7FDFF
notABFiles = 0xFF3FCFF3FCFF3FCFF3FCFF3FC
notIJFiles = 0x3FCFF3FCFF3FCFF3FCFF3FCFF
inBounds = 0xFFFFFFFFFFFFFFFFFFFFFFFFF


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


def genKingAttkPiece(sq):
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
	return attkPiece
