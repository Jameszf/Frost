
# CONSTANTS
# =====================================================================================
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 600, 600
BOARD_TILES = 10
SHEET_ROWS = 2
SHEET_COLS = 6
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = WIN_WIDTH // BOARD_TILES, WIN_HEIGHT // BOARD_TILES
SHEET_SIZE = (SHEET_COLS * TILE_WIDTH, SHEET_ROWS * TILE_HEIGHT)
BOARD_KEYS = ["wPawns", "wKnights", "wBishops", "wRooks", "wQueens", "wKings",
			  "bPawns", "bKnights", "bBishops", "bRooks", "bQueens", "bKings"]

# COLORS
# =====================================================================================
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
DARK_TILE = 148, 111, 81
LIGHT_TILE = 240, 214, 181


# GAME STATE
# =====================================================================================
g_attkRayTbl = {
	"NW": [],
	"N": [],
	"NE": [],
	"E": [],
	"SE": [],
	"S": [],
	"SW": [],
	"W": []
}

g_board = {
	"wPawns": 0,
	"wKnights": 0,
	"wBishops": 0,
	"wRooks": 0,
	"wQueens": 0,
	"wKings": 0,
	"bPawns": 0,
	"bKnights": 0,
	"bBishops": 0,
	"bRooks": 0,
	"bQueens": 0,
	"bKings": 0,
}

g_screen = None
g_sheet = None
