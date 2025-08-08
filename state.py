from enum import Enum, auto

class GameState(Enum):
    INTRO = auto()
    MENU = auto()
    GAME = auto()
    PAUSE = auto()
    RECORDS = auto()
    SETTINGS = auto()
    GAME_OVER = auto()
