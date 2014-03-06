from datetime import datetime
from common import *
import os
from outcome import Outcome
from gamestate import Gamestate
from action import Action
from player import Player


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

    @classmethod
    def from_log_document(cls, log_document, player_profile=None, shift_turn=False):

        initial_gamestate_document = log_document["initial_gamestate"]
        gamestate = Gamestate.from_document(initial_gamestate_document)
        if "player1" in log_document:
            player1 = Player.from_document(log_document["player1"])
            player2 = Player.from_document(log_document["player2"])
        else:
            player1 = Player("Green", "Human")
            player2 = Player("Red", "AI")

        if player_profile:
            if player1.profile == player_profile:
                player2.intelligence = player2.ai = "Network"
            elif player2.profile == player_profile:
                player1.intelligence = player1.ai = "Network"
            else:
                print player_profile, "is not playing this game."
                print "The players are:", player1.profile, "and", player2.profile
                return

        if "created_at" in log_document:
            created_at = log_document["created_at"]
        else:
            created_at = None

        game = cls([player1, player2], gamestate, created_at)
        game.gamestate = gamestate

        action_count = int(log_document["action_count"])

        game.actions = {}
        game.outcomes = {}

        for action_number in range(1, action_count + 1):
            if game.is_turn_done():
                game.shift_turn()

            action_document = log_document[str(action_number)]

            game.actions[str(action_number)] = action_document

            action = Action.from_document(gamestate.all_units(), action_document)

            options = None
            if str(action_number) + "_options" in log_document:
                options = log_document[str(action_number) + "_options"]

            game.options[str(action_number)] = options

            outcome = None
            outcome_document = None
            if action.has_outcome():
                outcome_document = log_document[str(action_number) + "_outcome"]
                outcome = Outcome.from_document(outcome_document)
                if options and "move_with_attack" in options:
                    action.move_with_attack = bool(options["move_with_attack"])

            game.outcomes[str(action_number)] = outcome_document
            game.do_action(action, outcome)

            if options and "upgrade" in options:
                upgrade = options["upgrade"]
                if not isinstance(upgrade, basestring):
                    upgrade = enum_attributes(upgrade)
                position = action.end_at
                if not position in game.gamestate.player_units:
                    position = action.target_at
                upgraded_unit = action.unit.get_upgraded_unit(upgrade)
                game.gamestate.player_units[position] = upgraded_unit

        if shift_turn:
            if game.is_turn_done():
                game.shift_turn()

        return game

    def set_network_player(self, local_player):
        for player in range(2):
            if self.players[player].profile != local_player:
                self.players[player].ai_name = "Network"
                self.players[player].ai = "Network"

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
        if outcome:
            outcome_document = outcome.to_document()
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
            gamestate_file.write(document_to_string(savegame_document))

    def save_option(self, option, option_value):
        action_count = self.gamestate.action_count
        options = dict()
        if action_count in self.options:
            options = self.options[action_count]
        options[option] = option_value
        self.options[action_count] = options

    def is_turn_done(self):
        return self.gamestate.is_turn_done()

    def to_document(self):
        return {
            "player1": self.players[0].to_document(),
            "player2": self.players[1].to_document(),
            "initial_gamestate": self.initial_gamestate.to_document(),
            "created_at": self.created_at
        }

    def is_player_human(self):
        return self.current_player().intelligence == "Human"

    def is_player_network(self):
        return self.current_player().intelligence == "Network"

    def is_enemy_network(self):
        return self.opponent_player().intelligence == "Network"

    def is_player_ai(self):
        return not (self.is_player_network() or self.is_player_human())
