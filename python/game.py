from datetime import datetime
import ai_module


class Game:
    def __init__(self, players, gamestate, interaction_number=0, turn=0, created_at=datetime.utcnow()):
        self.gamestate = gamestate
        self.players = players
        self.interaction_number = interaction_number
        self.turn = turn
        self.created_at = created_at

    def set_ais(self):
        for player in range(2):
            ai_name = self.players[player].ai_name
            if ai_name in ["Human", "Network"]:
                self.players[player].ai = ai_name
            else:
                self.players[player].ai = ai_module.AI(ai_name)

    def current_player(self):
        return self.players[0]

    def opponent_player(self):
        return self.players[1]

    def do_action(self, action):
        self.gamestate.do_action(action)

    def shift_turn(self):
        self.gamestate.shift_turn()
        if self.players[0].color == "Green":
            self.turn += 1
        self.players = [self.players[1], self.players[0]]
