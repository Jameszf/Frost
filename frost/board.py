
from typing import Dict, List

from frost.customTypes import Bitboard
from frost.bitboard import getBit, clearBit, setBit, fBitscan
from frost.attackPiece import Attack
from frost.scripts import printBboard


class Board:
    """
    This class only contains information about piece placement and
    provides methods for their modifying them. attackPiece.py and
    board.py are both semi-coupled together (TODO reduce coupling if
    possible). For metadata about a game being played is stored in
    GameState objects defined in state.py

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

    def __init__(self, bboards: Dict[str, Bitboard]):
        self.bboards: Dict[str, Bitboard] = bboards


    def getPieceAtTile(self, square: int) -> str:
        """
        Determines if a piece occupies a specific square. If one does,
        return its piece key (keys can be found in Board.KEYS).
        """
        for key in Board.KEYS:
            if getBit(self.bboards[key], square):
                return key
        return "None"


    def isOccupied(self, square: int) -> bool:
        """
        Checks if a particular board square is occupied.
        """
        occ: Bitboard = self.getOccBboard()
        return getBit(occ, square) != 0


    def oppositeColors(self, square1: int, square2: int) -> bool:
        """
        Checks if pieces on two squares are opposite colors. This is
        used for during captures.
        """
        p1: str = self.getPieceAtTile(square1)
        p2: str = self.getPieceAtTile(square2)
        return p1[0] != p2[0]


    def getOccBboard(self) -> Bitboard:
        """
        Combines all Bitboards to give a Bitboard with the positions
        of all the pieces.
        """
        occBboard: Bitboard = 0
        for key in Board.KEYS:
            occBboard |= self.bboards[key]
        return occBboard


    def getColorAttkSet(self, color: str) -> Bitboard:
        """
        Creates a attackset of all the pieces of a specific color.
        """
        pieceTypes: List[str] = ["Pawns", "Bishops", "Knights", "Queens", "Rooks", "Kings"]
        pieceKeys: List[str] = [f"{color}{pType}" for pType in pieceTypes]
        attkSet: Bitboard = 0
        for pType in pieceKeys:
            bboard: Bitboard = self.bboards[pType]
            while bboard != 0:
                idx: int = fBitscan(bboard)
                attkSet |= Attack.genAttkPiece(self.bboards, idx)
                bboard = clearBit(bboard, idx)
        return attkSet


    def movePiece(self, start: int, dest: int) -> bool:
        """
        Primary function called for piece movement during playing phase. This
        handles illegal move checks, basic piece movement, and captures.

        TODO Tidy up logic and separate concerns.
        """
        startPieceKey: str = self.getPieceAtTile(start)
        destPieceKey: str = self.getPieceAtTile(dest)
        if startPieceKey:
            moveMap: int = Attack.genAttkPiece(self.bboards, start, startPieceKey)
            if startPieceKey[1:] == "Pawns":
                moveMap &= self.getOccBboard()
                moveMap |= 0x401 << start if startPieceKey[0] == "w" else 0x8020000000000000000000000 >> (99 - start)
            printBboard(moveMap)
            if getBit(moveMap, dest) and not (self.isOccupied(dest) and not self.oppositeColors(start, dest)):
                if self.isOccupied(dest) and self.oppositeColors(start, dest):
                    self.bboards[destPieceKey] = clearBit(self.bboards[destPieceKey], dest)
                self.bboards[startPieceKey] = setBit(clearBit(self.bboards[startPieceKey], start), dest)
                return True
        return False


    def placePiece(self, square: int, pType: str) -> bool:
        """
        Primary function for piece placement during deployment phase.
        Will prevent king placement if the square is attacked.
        """
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
