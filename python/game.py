from datetime import datetime
import ai_module
import common
import os


class Game:
    def __init__(self, players, gamestate, interaction_number=0, turn=0, created_at=datetime.utcnow()):
        self.gamestate = gamestate
        self.initial_gamestate = gamestate.copy()
        self.players = players
        self.interaction_number = interaction_number
        self.turn = turn
        self.created_at = created_at

        self.actions = dict()
        self.outcomes = dict()
        self.options = dict()

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

    def do_action(self, action, outcome):
        return self.gamestate.do_action(action, outcome)

    def shift_turn(self):
        self.gamestate.shift_turn()
        if self.players[0].color == "Green":
            self.turn += 1
        self.players = [self.players[1], self.players[0]]
        self.gamestate.set_available_actions()

    def savegame_folder(self):
        return "./replay/" + str(self.created_at.strftime("%Y%m%d-%H%M%S"))

    def save(self, view, action, outcome):
        if not os.path.exists(self.savegame_folder()):
            os.makedirs(self.savegame_folder())

        action_count = self.gamestate.action_count

        self.actions[action_count] = action.to_document()
        outcome_document = outcome.to_document()
        if outcome_document:
            self.outcomes[action_count] = outcome_document

        filename = self.savegame_folder() + "/" + str(action_count)

        view.save_screenshot(filename + ".jpeg")

        savegame_document = dict()
        savegame_document["gamestate"] = self.gamestate.to_document()
        savegame_document["initial_gamestate"] = self.initial_gamestate.to_document()
        savegame_document["action_count"] = self.gamestate.action_count
        for action_number, document in self.actions.items():
            savegame_document[action_number] = document

        for action_number, document in self.outcomes.items():
            savegame_document[str(action_number) + "_outcome"] = document

        for action_number, options in self.options.items():
            savegame_document[str(action_number) + "_options"] = options

        with open(filename + ".json", 'w') as gamestate_file:
            gamestate_file.write(common.document_to_string(savegame_document))

    def save_option(self, option, option_value):
        action_count = self.gamestate.action_count
        options = dict()
        if action_count in self.options:
            options = self.options[action_count]
        options[option] = option_value
        self.options[action_count] = options

    def to_document(self):
        return {
            ""
            "player1": self.players[0].to_document(),
            "player2": self.players[1].to_document(),
            "initial_gamestate": self.initial_gamestate.to_document(),
            "created_at": self.created_at
        }
