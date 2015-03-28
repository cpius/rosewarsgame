import game.ai as ai
from gamestate.gamestate_library import *


class Player(object):
    def __init__(self, color, intelligence, profile=None):
        self.profile = profile
        self.color = color
        self.intelligence = intelligence
        if intelligence == Intelligence.AI:
            self.ai = ai.AI()

        if color == "Red":
            self.backline = 8
            self.frontline = 5
        else:
            self.backline = 1
            self.frontline = 4

    @classmethod
    def from_document(cls, document):
        return cls(document["color"], enum_from_string[document["intelligence"]], document["profile"])

    def to_document(self):
        return {
            "color": self.color,
            "intelligence": self.intelligence,
            "profile": self.profile
        }
