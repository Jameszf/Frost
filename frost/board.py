
from typing import Dict, List

from frost.constants import *
from frost.bitboard import getBit, clearBit, setBit, fBitscan
from frost.attackPiece import Attack
from frost.scripts import printBboard


class Board:
    KEYS = ["wPawns", "wKnights", "wBishops", "wRooks", "wQueens", "wKings",
                  "bPawns", "bKnights", "bBishops", "bRooks", "bQueens", "bKings"]

    def __init__(self, bboards: Dict[str, int]):
        self.bboards: Dict[str, int] = bboards


    def getPieceAtTile(self, square: int) -> str:
        for key in Board.KEYS:
            if getBit(self.bboards[key], square):
                return key
        return "None"


    def getPieceColorAtTile(self, square: int) -> str:
        for key in Board.KEYS:
            if getBit(self.bboards[key], square):
                return key[0]
        return "N"


    def isOccupied(self, square: int) -> int:
        occ: int = self.getOccBboard()
        return getBit(occ, square)


    def canCapture(self, square1: int, square2: int) -> bool:
        p1: str = self.getPieceAtTile(square1)
        p2: str = self.getPieceAtTile(square2)
        return p1[0] != p2[0]


    def getOccBboard(self) -> int:
        occBboard: int = 0
        for key in Board.KEYS:
            occBboard |= self.bboards[key]
        return occBboard


    def getColorAttkSet(self, color: str) -> int:
        pieceTypes: List[str] = [f"{color}{pType}" for pType in ["Pawns", "Bishops", "Knights", "Queens", "Rooks", "Kings"]]
        attkSet: int = 0
        for pType in pieceTypes:
            bboard: int = self.bboards[pType]
            while bboard != 0:
                idx: int = fBitscan(bboard)
                attkSet |= Attack.genAttkPiece(self.bboards, idx)
                bboard = clearBit(bboard, idx)
        return attkSet


    def movePiece(self, start: int, dest: int) -> bool:
        startPKey: str = self.getPieceAtTile(start)
        destPKey: str = self.getPieceAtTile(dest)
        if startPKey:
            moveMap: int = 0 if startPKey[1:] == "Pawns" else Attack.genAttkPiece(self.bboards, start)
            if getBit(moveMap, dest) and not (self.isOccupied(dest) and not self.canCapture(start, dest)):
                if self.isOccupied(dest) and self.canCapture(start, dest):
                    self.bboards[destPKey] = clearBit(self.bboards[destPKey], dest)
                self.bboards[startPKey] = setBit(clearBit(self.bboards[startPKey], start), dest)
                return True
        return False


    def placePiece(self, square: int, pType: str) -> bool:
        if pType[1:] == "Kings":
            oppColor: str = "w" if pType[0] == "b" else "b"
            attkSet: int = self.getColorAttkSet(oppColor)
            print(f"ATTACK SET OF {oppColor}")
            printBboard(attkSet)
            if not getBit(attkSet, square):
                self.bboards[pType] = setBit(self.bboards[pType], square)
                return True
            else:
                return False
        else:
            self.bboards[pType] = setBit(self.bboards[pType], square)
            return True
