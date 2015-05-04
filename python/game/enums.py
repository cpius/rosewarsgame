from enum import Enum


class Intelligence(Enum):
    Human = 1
    AI_level1 = 2
    AI_level2 = 3
    AI_level3 = 4
    Network = 5


class Opponent(Enum):
    HotSeat = 1
    AI = 2
    Internet = 3
    Load = 4
