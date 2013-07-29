import imp
import json
from common import CustomJsonEncoder


class AI(object):
    """
    Creates an AI of a certain type, which can make the two decisions a player has to make in a game:
    - Make an action
    - Make a second part of an action (with Samurai or Chariot)
    - Put a counter on a unit with two experience points
    
    The locations are transformed so that the player the AI is playing for has backline on row 1.
    """

    def __init__(self, name):

        ai_type = imp.load_source(name, "ai_" + name.lower() + ".py")
        self.get_action = ai_type.get_action
        self.name = name

    def select_action(self, game):
        gamestate = game.gamestate.copy()
        actions = gamestate.get_actions()
        if actions:
            return self.get_action(actions, gamestate)
