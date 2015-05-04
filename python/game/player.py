import ai.ai as ai
from game.enums import Intelligence


class Player(object):
    def __init__(self, color, intelligence, profile=None):
        self.profile = profile
        self.color = color
        self.intelligence = intelligence
        if intelligence == Intelligence.AI_level1:
            self.ai = ai.AI(level=1)
        elif intelligence == Intelligence.AI_level2:
            self.ai = ai.AI(level=2)
        elif intelligence == Intelligence.AI_level3:
            self.ai = ai.AI(level=3)

        if color == "Red":
            self.backline = 8
            self.frontline = 5
        else:
            self.backline = 1
            self.frontline = 4

    @classmethod
    def from_document(cls, document):
        return cls(document["color"], Intelligence[document["intelligence"]], document["profile"])

    def to_document(self):
        return {
            "color": self.color,
            "intelligence": self.intelligence,
            "profile": self.profile
        }
