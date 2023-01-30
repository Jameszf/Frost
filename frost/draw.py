
from dataclasses import dataclass
import pygame

from frost.constants import *
from frost.bitboard import getBit


@dataclass
class VisualPiece:
    x: float
    y: float
    squareX: int
    squareY: int
    pieceType: str


class Draw:
    def __init__(self):
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        sheet = pygame.image.load("./frost/assets/pieces.png").convert_alpha()
        sheet = pygame.transform.smoothscale(sheet, SHEET_SIZE)
        self.sheet = sheet
        self.visualPieces = []


    def drawTiles(self):
        """
        Draws BOARD_TILES by BOARD_TILES checkerboard on screen

        INPUT: screen (pygame display object).
        OUTPUT: void.
        """
        for y in range(BOARD_TILES):
            for x in range(BOARD_TILES):
                if (x + y) % 2 == 0:
                    color = LIGHT_TILE
                else:
                    color = DARK_TILE
                tx = x * TILE_WIDTH
                ty = y * TILE_WIDTH
                pygame.draw.rect(self.screen, color, (tx, ty, tx + TILE_WIDTH, ty + TILE_HEIGHT))


    def syncPieces(self, bboards):
        self.visualPieces.clear()
        for key in bboards.keys():
            for i in range(100):
                if getBit(bboards[key], i):
                    squareX = i % BOARD_TILES
                    squareY = i // BOARD_TILES
                    x = squareX * TILE_WIDTH
                    y = ((BOARD_TILES - 1) - i // BOARD_TILES) * TILE_HEIGHT
                    self.visualPieces.append(VisualPiece(x, y, squareX, squareY, key))


    def drawPieces(self):
        """
        Draws chess pieces according to board using sprites from sheet

        INPUT: screen (pygame display object), bboards (List<Bitboard>), sheet (pygame sprite object).
        OUTPUT: void.
        """
        spritePos = {
            "wPawns": (5 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
            "wKnights": (3 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
            "wBishops": (2 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
            "wRooks": (4 * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
            "wQueens": (TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT),
            "wKings": (0, 0, TILE_WIDTH, TILE_HEIGHT),

            "bPawns": (5 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            "bKnights": (3 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            "bBishops": (2 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            "bRooks": (4 * TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            "bQueens": (TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            "bKings": (0, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
        }
        for visualPiece in self.visualPieces:
            self.screen.blit(self.sheet, (visualPiece.x, visualPiece.y), area=spritePos[visualPiece.pieceType])


    def drawBoard(self):
        """
        Main rendering function of game. Rendering order MATTERS. 
        LAYERS order: tiles --> pieces.

        INPUT: screen (pygame display object), board (bitboard), sheet (pygame sprite object).
        OUTPUT: void.
        """
        self.screen.fill(GREEN) # Clear previous frame.
        self.drawTiles()
        self.drawPieces()
        pygame.display.flip() # Render new frame.
        self.clock.tick(60) # Locked to 60 FPS. 

