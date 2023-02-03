
from dataclasses import dataclass
import pygame

from frost.customTypes import *
from frost.bitboard import getBit


@dataclass
class VisualPiece:
    x: float
    y: float
    squareX: int
    squareY: int
    pieceType: str


class Draw:
    WIN_WIDTH: int = 600
    WIN_HEIGHT: int = 600
    BOARD_TILES: int = 10
    SHEET_ROWS: int = 2
    SHEET_COLS: int = 6
    TILE_WIDTH: int  = WIN_WIDTH // BOARD_TILES
    TILE_HEIGHT: int = WIN_HEIGHT // BOARD_TILES
    SHEET_SIZE = (SHEET_COLS * TILE_WIDTH, SHEET_ROWS * TILE_HEIGHT)
    BLACK: Color = 0, 0, 0
    WHITE: Color = 255, 255, 255
    GREEN: Color = 0, 255, 0
    DARK_TILE: Color = 148, 111, 81
    LIGHT_TILE: Color = 240, 214, 181

    def __init__(self) -> None:
        self.screen: any = pygame.display.set_mode((Draw.WIN_WIDTH, Draw.WIN_HEIGHT))
        self.clock: any = pygame.time.Clock()
        sheet = pygame.image.load("./frost/assets/pieces.png").convert_alpha()
        sheet = pygame.transform.smoothscale(sheet, Draw.SHEET_SIZE)
        self.sheet: any = sheet
        self.visualPieces: List[VisualPiece] = []


    def drawCheckerboard(self) -> None:
        """
        Draws BOARD_TILES by BOARD_TILES checkerboard on screen
        """
        color: Color
        for i in range(Draw.BOARD_TILES * Draw.BOARD_TILES):
            if (i + i // Draw.BOARD_TILES) % 2:
                color = Draw.LIGHT_TILE
            else:
                color = Draw.DARK_TILE
            self.drawTile(i, color)


    def syncPieces(self, bboards):
        self.visualPieces.clear()
        for key in bboards.keys():
            for i in range(100):
                if getBit(bboards[key], i):
                    squareX = i % Draw.BOARD_TILES
                    squareY = i // Draw.BOARD_TILES
                    x = squareX * Draw.TILE_WIDTH
                    y = (Draw.BOARD_TILES - 1 - i // Draw.BOARD_TILES) * Draw.TILE_HEIGHT
                    self.visualPieces.append(VisualPiece(x, y, squareX, squareY, key))


    def drawPieces(self):
        """
        Draws chess pieces according to board using sprites from sheet

        INPUT: screen (pygame display object), bboards (List<Bitboard>), sheet (pygame sprite object).
        OUTPUT: void.
        """
        spritePos = {
            "wPawns": (5 * Draw.TILE_WIDTH, 0, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "wKnights": (3 * Draw.TILE_WIDTH, 0, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "wBishops": (2 * Draw.TILE_WIDTH, 0, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "wRooks": (4 * Draw.TILE_WIDTH, 0, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "wQueens": (Draw.TILE_WIDTH, 0, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "wKings": (0, 0, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),

            "bPawns": (5 * Draw.TILE_WIDTH, Draw.TILE_HEIGHT, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "bKnights": (3 * Draw.TILE_WIDTH, Draw.TILE_HEIGHT, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "bBishops": (2 * Draw.TILE_WIDTH, Draw.TILE_HEIGHT, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "bRooks": (4 * Draw.TILE_WIDTH, Draw.TILE_HEIGHT, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "bQueens": (Draw.TILE_WIDTH, Draw.TILE_HEIGHT, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
            "bKings": (0, Draw.TILE_HEIGHT, Draw.TILE_WIDTH, Draw.TILE_HEIGHT),
        }
        for visualPiece in self.visualPieces:
            self.screen.blit(self.sheet, (visualPiece.x, visualPiece.y), area=spritePos[visualPiece.pieceType])


    def drawTile(self, square: int, color: Color):
        tx: int = (square % Draw.BOARD_TILES) * Draw.TILE_WIDTH
        ty: int = (Draw.BOARD_TILES - (square // Draw.BOARD_TILES) - 1) * Draw.TILE_HEIGHT
        pygame.draw.rect(self.screen, color, (tx, ty, Draw.TILE_WIDTH, Draw.TILE_HEIGHT))


    def drawBoard(self, selectedSquare: int):
        """
        Main rendering function of game. Rendering order MATTERS. 
        LAYERS order: tiles --> pieces.

        INPUT: screen (pygame display object), board (bitboard), sheet (pygame sprite object).
        OUTPUT: void.
        """
        self.screen.fill(Draw.GREEN) # Clear previous frame.
        self.drawCheckerboard()
        self.drawTile(selectedSquare, (255, 0, 0))
        self.drawPieces()
        pygame.display.flip() # Render new frame.
        self.clock.tick(60) # Locked to 60 FPS. 

