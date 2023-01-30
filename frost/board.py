
from frost.constants import *
from frost.bitboard import getBit, clearBit, setBit, fBitscan
from frost.attackPiece import Attack
from frost.scripts import printBboard


class Board:
    KEYS = ["wPawns", "wKnights", "wBishops", "wRooks", "wQueens", "wKings",
                  "bPawns", "bKnights", "bBishops", "bRooks", "bQueens", "bKings"]

    def __init__(self, bboards):
        self.bboards = bboards


    def getPieceAtTile(self, square):
        for key in Board.KEYS:
            if getBit(self.bboards[key], square):
                return key


    def getPieceColorAtTile(self, square):
        for key in Board.KEYS:
            if getBit(self.bboards[key], square):
                return key[0]


    def isOccupied(self, square):
        occ = self.getOccBboard()
        return getBit(occ, square)


    def canCapture(self, square1, square2):
        p1 = self.getPieceAtTile(square1)
        p2 = self.getPieceAtTile(square2)
        return p1[0] != p2[0]


    def getOccBboard(self):
        occBboard = 0
        for key in Board.KEYS:
            occBboard |= self.bboards[key]
        return occBboard


    def getColorAttkSet(self, color):
        pieceTypes = ["Pawns", "Bishops", "Knights", "Queens", "Rooks", "Kings"]
        pieceTypes = [f"{color}{pType}" for pType in pieceTypes]
        attkSet = 0
        for pType in pieceTypes:
            bboard = self.bboards[pType]
            while bboard != 0:
                idx = fBitscan(bboard)
                attkSet |= Attack.genAttkPiece(self.bboards, idx)
                bboard = clearBit(bboard, idx)
        return attkSet


    def movePiece(self, start, dest):
        startPKey = self.getPieceAtTile(start)
        destPKey = self.getPieceAtTile(dest)
        if startPKey:
            moveMap = 0 if startPKey[1:] == "Pawns" else Attack.genAttkPiece(self.bboards, start)
            if getBit(moveMap, dest) and not (self.isOccupied(dest) and not self.canCapture(start, dest)):
                if self.isOccupied(dest) and self.canCapture(start, dest):
                    self.bboards[destPKey] = clearBit(self.bboards[destPKey], dest)
                self.bboards[startPKey] = setBit(clearBit(self.bboards[startPKey], start), dest)
                return True
        return False


    def placePiece(self, square, pType):
        if pType[1:] == "Kings":
            oppColor = "w" if pType[0] == "b" else "b"
            attkSet = self.getColorAttkSet(oppColor)
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
