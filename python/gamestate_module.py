from __future__ import division
import action_doer
import initializer
import action_getter
import saver
import settings
import ai_module


class Gamestate:
    
    def __init__(self, player1, player1_units, player2, player2_units, turn= 1):
        self.turn = turn
        self.units = [player1_units, player2_units]
        self.players = [player1, player2]

    def do_action(self, action):
        self.units[1], self.units[0], self.players[0] = \
            action_doer.do_action(action, self.units[1], self.units[0], self.players[1], self.players[0])

    def initialize_turn(self):
        self.units[1], self.units[0], self.players[0] = \
            initializer.initialize_turn(self.units[1], self.units[0], self.players[0])

    def initialize_action(self):
        self.units[0] = initializer.initialize_action(self.units[0])

    def get_actions(self):
        if hasattr(self.players[0], "extra_action"):
            return action_getter.get_extra_actions(self.units[1], self.units[0], self.players[0])
        else:
            return action_getter.get_actions(self.units[1], self.units[0], self.players[0])

    def copy(self):
        saved_gamestate = save_gamestate(self)
        return load_gamestate(saved_gamestate)

    def __eq__(self, other):
        pass  # Write function here

    def set_ais(self):
        if settings.player1_ai != "Human":
            self.players[0].ai = ai_module.AI(settings.player1_ai)
        else:
            self.players[0].ai = "Human"

        if settings.player2_ai != "Human":
            self.players[1].ai = ai_module.AI(settings.player2_ai)
        else:
            self.players[1].ai = "Human"

    def turn_shift(self):
        if self.players[0].color == "Green":
            self.turn += 1
        self.units = [self.units[1], self.units[0]]
        self.players = [self.players[1], self.players[0]]
        self.initialize_turn()
        self.initialize_action()


def save_gamestate(gamestate):
    return saver.save_gamestate(gamestate)


def load_gamestate(saved_gamestate):
    return saver.load_gamestate(saved_gamestate)


def write_gamestate(gamestate, path):
    saver.write_gamestate(gamestate, path)


def read_gamestate(path):
    return saver.read_gamestate(path)