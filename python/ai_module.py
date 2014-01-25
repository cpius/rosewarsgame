import imp


class AI(object):
    def __init__(self, name):
        ai_type = imp.load_source(name, name.lower() + ".py")
        self.get_action = ai_type.get_action
        self.get_upgrade = ai_type.get_upgrade
        self.name = name

    def select_action(self, game):
        gamestate = game.gamestate
        actions = gamestate.get_actions()

        if actions:
            return self.get_action(actions, gamestate)

    def select_upgrade(self, game):
        return self.get_upgrade(game)
