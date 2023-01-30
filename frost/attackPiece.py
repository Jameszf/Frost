
import json
import frost.board

from frost.bitboard import rBitscan, fBitscan, getBit
from frost.scripts import printBboard


class Attack:
    __notAFile = 0xFFBFEFFBFEFFBFEFFBFEFFBFE
    __notJFile = 0x7FDFF7FDFF7FDFF7FDFF7FDFF
    __notABFiles = 0xFF3FCFF3FCFF3FCFF3FCFF3FC
    __notIJFiles = 0x3FCFF3FCFF3FCFF3FCFF3FCFF
    __inBounds = 0xFFFFFFFFFFFFFFFFFFFFFFFFF
    __rayTable = {}


    def init():
        with open("./frost/attackRays.json", "r") as f:
            Attack.__rayTable = json.load(f)


    def isNegDir(rDir):
	    return rDir == "W" or rDir == "SW" or rDir == "S" or rDir == "SE"


    def genBlckAttkRay(occBboard, sq, rayDir):
	    blockers = (occBboard & Attack.__rayTable[rayDir][sq]) ^ (1 << sq)
	    blckRay = Attack.__rayTable[rayDir][sq]
	    if blockers != 0:
		    fstBlockerSq = rBitscan(blockers) if Attack.isNegDir(rayDir) else fBitscan(blockers)
		    rmRay = Attack.__rayTable[rayDir][fstBlockerSq] ^ (1 << fstBlockerSq)
		    blckRay ^= rmRay
	    return blckRay


    def genKingAttkPiece(sq):
        north = (0x400 << sq) & Attack.__inBounds
        south = 0x20000000000000000000000 >> (99 - sq)
        east = (0x2 << sq) & Attack.__notAFile
        west = (0x4000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        northEast = (0x800 << sq) & Attack.__notAFile
        northWest = (0x1000000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        southEast = (0x80000000000000000000000 >> (100 - sq)) & Attack.__notAFile
        southWest = (0x10000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        kingSq = 1 << sq
        return kingSq | north | south | east | west | northEast | northWest | southEast | southWest



    def genKnightAttkPiece(sq):
        noNoEa = (0x200000 << sq) & Attack.__notAFile
        noNoWe = (0x400000000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        noEaEa = (0x1000 << sq) & Attack.__notABFiles
        soEaEa = (0x100000000000000000000000 >> (100 - sq)) & Attack.__notABFiles
        soSoEa = (0x200000000000000000000 >> (100 - sq)) & Attack.__notAFile
        soSoWe = (0x40000000000000000000 >> (99 - sq)) & Attack.__notJFile
        soWeWe = (0x8000000000000000000000 >> (99 - sq)) & Attack.__notIJFiles
        noWeWe = (0x800000000000000000000000000 >> (99 - sq)) & Attack.__notIJFiles
        knightSq = 1 << sq
        return knightSq | noNoEa | noNoWe | noEaEa | soEaEa | soSoEa | soSoWe | soWeWe | noWeWe



    def genPawnAttkPiece(sq):
        northEast = (0x800 << sq) & Attack.__notAFile
        northWest = (0x1000000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        return northEast | northWest


    def __getPieceAtTile(bboards, square):
        for key in bboards.keys():
            if getBit(bboards[key], square):
                return key


    def __getOccBoard(bboards):
        occBboard = 0
        for key in bboards.keys():
            occBboard |= bboards[key]
        return occBboard


    def genAttkPiece(bboards, sq):
        print(f"Generating Attack Piece Bitboard for piece at square #{sq}")
        print(f"Piece occupying that tile: {Attack.__getPieceAtTile(bboards, sq)}")

        pType = Attack.__getPieceAtTile(bboards, sq)
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
                blckRay = Attack.genBlckAttkRay(Attack.__getOccBoard(bboards), sq, rd)
                attkPiece |= blckRay
        elif pType == "Knights":
            attkPiece = Attack.genKnightAttkPiece(sq)
        elif pType == "Pawns":
            attkPiece = Attack.genPawnAttkPiece(sq)
        elif pType == "Kings":
            attkPiece = Attack.genKingAttkPiece(sq)
        else:
            pass

        print("Attack Piece generated")
        printBboard(attkPiece)
        return attkPiece

