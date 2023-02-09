
from typing import Dict, List

from frost.bitboard import getBit, clearBit, setBit, fBitscan
from frost.attackPiece import Attack
from frost.scripts import printBboard


class Board:
    """
    BOARD DESIGN
    The squares are numbered as follows on the board,
    90 91 92 93 94 95 96 97 98 99
    80 81 82 83 84 85 86 87 88 89
    70 71 72 73 74 75 76 77 78 79
    60 61 62 63 64 65 66 67 68 69
    50 51 52 53 54 55 56 57 58 59
    40 41 42 43 44 45 46 47 48 49
    30 31 32 33 34 35 36 37 38 39
    20 21 22 23 24 25 26 27 28 29
    10 11 12 13 14 15 16 17 18 19
     0  1  2  3  4  5  6  7  8  9

    and numbered as follows on a bitboard,
    (MSB) [99][98][97] ... [2][1][0] (LSB).

    Cardinal directions are defined as:
      N
    W . E
      S
    """
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
            moveMap: int = Attack.genAttkPiece(self.bboards, start, startPKey)
            if startPKey[1:] == "Pawns":
                moveMap &= self.getOccBboard()
                moveMap |= 0x401 << start if startPKey[0] == "w" else 0x8020000000000000000000000 >> (99 - start)
            printBboard(moveMap)
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
