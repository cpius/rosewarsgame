class Player(object):
    def __init__(self, color):
        self.color = color
        if color == "Red":
            self.backline = 8
            self.frontline = 5
        else:
            self.backline = 1
            self.frontline = 4
