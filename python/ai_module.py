import imp


class AI(object):
    def __init__(self, name):
        ai_type = imp.load_source(name, "ai_" + name.lower() + ".py")
        self.get_action = ai_type.get_action
        self.name = name

    def select_action(self, game):
        gamestate = game.gamestate
        actions = gamestate.get_actions()

        if actions:
            return self.get_action(actions, gamestate)
