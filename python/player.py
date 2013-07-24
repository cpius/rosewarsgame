import ai_module


class Player(object):
    def __init__(self, color, intelligence, player_id=None):
        self.player_id = player_id
        self.color = color
        self.intelligence = intelligence
        if intelligence not in ["Human", "Network"]:
            print intelligence
            self.ai = ai_module.AI(intelligence)

        if color == "Red":
            self.backline = 8
            self.frontline = 5
        else:
            self.backline = 1
            self.frontline = 4