
import pygame

from constants import *
from bitboard import getBit
from board import Board


class Draw:
    def __init__(self):
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        sheet = pygame.image.load("assets/pieces.png").convert_alpha()
        sheet = pygame.transform.smoothscale(sheet, SHEET_SIZE)
        self.sheet = sheet


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



    def drawPieces(self, bboards):
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

        for key in Board.KEYS:
            for i in range(BOARD_TILES ** 2):
                if getBit(bboards[key], i):
                    x = (i % BOARD_TILES) * TILE_WIDTH
                    y = ((BOARD_TILES - 1) - i // BOARD_TILES) * TILE_HEIGHT
                    self.screen.blit(self.sheet, (x, y), area=spritePos[key])


    def drawBoard(self, bboards):
        """
        Main rendering function of game. Rendering order MATTERS. 
        LAYERS order: tiles --> pieces.

        INPUT: screen (pygame display object), board (bitboard), sheet (pygame sprite object).
        OUTPUT: void.
        """

        self.screen.fill(GREEN) # Clear previous frame.
        self.drawTiles()
        self.drawPieces(bboards)
        pygame.display.flip() # Render new frame.
        self.clock.tick(60) # Locked to 60 FPS. 

