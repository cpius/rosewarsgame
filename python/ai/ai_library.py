from enum import Enum
from gamestate.outcome import Outcome, rolls
from gamestate.gamestate_library import board_tiles


class Player(Enum):
    player = 1
    opponent = 2


class Result(Enum):
    win = 1
    loss = 2
    noresult = 3


success = Outcome(dict((key, rolls(1, 6)) for key in board_tiles))
failure = Outcome(dict((key, rolls(6, 1)) for key in board_tiles))
