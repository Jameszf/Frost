
from enum import Enum

# GUI
# =====================================================================================
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 600, 600
BOARD_TILES = 10
SHEET_ROWS = 2
SHEET_COLS = 6
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = WIN_WIDTH // BOARD_TILES, WIN_HEIGHT // BOARD_TILES
SHEET_SIZE = (SHEET_COLS * TILE_WIDTH, SHEET_ROWS * TILE_HEIGHT)

# ENUMS
# =====================================================================================
class Turn(Enum):
    BLACK = "black"
    WHITE = "white"

class Phase(Enum):
    PLAYING = "playing"
    DEPLOYMENT = "deployment"

# COLORS
# =====================================================================================
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
DARK_TILE = 148, 111, 81
LIGHT_TILE = 240, 214, 181


