
from enum import Enum
from typing import Tuple, List

Bitboard = int
Color = Tuple[int, int, int]

class Turn(Enum):
    BLACK = "black"
    WHITE = "white"

class Phase(Enum):
    PLAYING = "playing"
    DEPLOYMENT = "deployment"

