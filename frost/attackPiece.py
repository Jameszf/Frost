
import json
from typing import Dict, List

import frost.board
from frost.bitboard import rBitscan, fBitscan, getBit
from frost.scripts import printBboard


class Attack:
    __notAFile: int = 0xFFBFEFFBFEFFBFEFFBFEFFBFE
    __notJFile: int = 0x7FDFF7FDFF7FDFF7FDFF7FDFF
    __notABFiles: int = 0xFF3FCFF3FCFF3FCFF3FCFF3FC
    __notIJFiles: int = 0x3FCFF3FCFF3FCFF3FCFF3FCFF
    __inBounds: int = 0xFFFFFFFFFFFFFFFFFFFFFFFFF
    __rayTable: Dict[str, List[int]] = {}

    @staticmethod
    def init() -> None:
        with open("./frost/attackRays.json", "r") as f:
            Attack.__rayTable = json.load(f)

    @staticmethod
    def isNegDir(rDir: str) -> bool:
	    return rDir == "W" or rDir == "SW" or rDir == "S" or rDir == "SE"

    @staticmethod
    def genBlckAttkRay(occBboard: int, sq: int, rayDir: str) -> int:
	    blockers: int = (occBboard & Attack.__rayTable[rayDir][sq]) ^ (1 << sq)
	    blckRay: int = Attack.__rayTable[rayDir][sq]
	    if blockers != 0:
		    fstBlockerSq: int = rBitscan(blockers) if Attack.isNegDir(rayDir) else fBitscan(blockers)
		    rmRay: int = Attack.__rayTable[rayDir][fstBlockerSq] ^ (1 << fstBlockerSq)
		    blckRay ^= rmRay
	    return blckRay

    @staticmethod
    def genKingAttkPiece(sq: int) -> int:
        north: int = (0x400 << sq) & Attack.__inBounds
        south: int = 0x20000000000000000000000 >> (99 - sq)
        east: int = (0x2 << sq) & Attack.__notAFile
        west: int = (0x4000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        northEast: int = (0x800 << sq) & Attack.__notAFile
        northWest: int = (0x1000000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        southEast: int = (0x80000000000000000000000 >> (100 - sq)) & Attack.__notAFile
        southWest: int = (0x10000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        kingSq: int = 1 << sq
        return kingSq | north | south | east | west | northEast | northWest | southEast | southWest


    @staticmethod
    def genKnightAttkPiece(sq: int) -> int:
        noNoEa: int = (0x200000 << sq) & Attack.__notAFile
        noNoWe: int = (0x400000000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        noEaEa: int = (0x1000 << sq) & Attack.__notABFiles
        soEaEa: int = (0x100000000000000000000000 >> (100 - sq)) & Attack.__notABFiles
        soSoEa: int = (0x200000000000000000000 >> (100 - sq)) & Attack.__notAFile
        soSoWe: int = (0x40000000000000000000 >> (99 - sq)) & Attack.__notJFile
        soWeWe: int = (0x8000000000000000000000 >> (99 - sq)) & Attack.__notIJFiles
        noWeWe: int = (0x800000000000000000000000000 >> (99 - sq)) & Attack.__notIJFiles
        knightSq: int = 1 << sq
        return knightSq | noNoEa | noNoWe | noEaEa | soEaEa | soSoEa | soSoWe | soWeWe | noWeWe

    @staticmethod
    def genPawnAttkPiece(sq: int) -> int:
        northEast: int = (0x800 << sq) & Attack.__notAFile
        northWest: int = (0x1000000000000000000000000000 >> (99 - sq)) & Attack.__notJFile
        return northEast | northWest

    @staticmethod
    def __getPieceAtTile(bboards: Dict[str, int], square: int) -> str:
        for key in bboards.keys():
            if getBit(bboards[key], square):
                return key

    @staticmethod
    def __getOccBoard(bboards: Dict[str, int]) -> str:
        occBboard: int = 0
        for key in bboards.keys():
            occBboard |= bboards[key]
        return occBboard

    @staticmethod
    def genAttkPiece(bboards: Dict[str, int], sq: int) -> int:
        print(f"Generating Attack Piece Bitboard for piece at square #{sq}")
        print(f"Piece occupying that tile: {Attack.__getPieceAtTile(bboards, sq)}")

        pType: str = Attack.__getPieceAtTile(bboards, sq)
        pType = pType[1:] if pType else "None"

        # Sliding pieces
        attkPiece: int = 0
        if pType == "Queens" or pType == "Rooks" or pType == "Bishops":
            rDir: Dict[str, List[str]] = {
                "Queens": ["NW", "N", "NE", "E", "SE", "S", "SW", "W"],
                "Rooks": ["N", "E", "S", "W"],
                "Bishops": ["NW", "NE", "SE", "SW"]
            }
            for rd in rDir[pType]:
                blckRay: int = Attack.genBlckAttkRay(Attack.__getOccBoard(bboards), sq, rd)
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

