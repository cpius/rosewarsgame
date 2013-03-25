from __future__ import division
import action_doer
import initializer
import action_getter
import saver
import ai_module


class Gamestate:
    
    def __init__(self, player1, player1_units, player2, player2_units, turn=1, actions_remaining=2):
        self.turn = turn
        self.units = [player1_units, player2_units]
        self.players = [player1, player2]
        self.actions_remaining = actions_remaining

    def do_action(self, action):
        action_doer.do_action(self, action)

        if self.actions_remaining > 0:
            self.available_actions = action_getter.get_actions(self)
            if not self.available_actions:
                self.actions_remaining = 0

    def initialize_turn(self):
        initializer.initialize_turn(self)

    def initialize_action(self):
        initializer.initialize_action(self)

    def get_actions(self):
        if hasattr(self.players[0], "extra_action"):
            return action_getter.get_extra_actions(self)
        if self.actions_remaining == 1 and hasattr(self, "available_actions"):
            return self.available_actions
        else:
            return action_getter.get_actions(self)

    def copy(self):
        saved_gamestate = save_gamestate(self)
        return load_gamestate(saved_gamestate)

    def __eq__(self, other):
        pass

    def set_ais(self):
        if self.players[0].ai_name != "Human":
            self.players[0].ai = ai_module.AI(self.players[0].ai_name)
        else:
            self.players[0].ai = "Human"

        if self.players[1].ai_name != "Human":
            self.players[1].ai = ai_module.AI(self.players[1].ai_name)
        else:
            self.players[1].ai = "Human"

    def set_available_actions(self):
        self.available_actions = self.get_actions()


    def turn_shift(self):
        if self.players[0].color == "Green":
            self.turn += 1
        self.units = [self.units[1], self.units[0]]
        self.players = [self.players[1], self.players[0]]
        self.initialize_turn()
        self.initialize_action()
        self.set_available_actions()

    def current_player(self):
        return self.players[0]

    def opponent_player(self):
        return self.players[1]

    def player_units(self):
        return self.units[0]

    def opponent_units(self):
        return self.units[1]

    def get_actions_remaining(self):
        return self.actions_remaining

    def set_actions_remaining(self, actions_remaining):
        self.actions_remaining = actions_remaining

    def decrement_actions_remaining(self):
        self.actions_remaining -= 1

    def recalculate_special_counters(self):
        for unit in self.units[0].itervalues():
            self.add_yellow_counters(unit)
            self.add_blue_counters(unit)

        for unit in self.units[1].itervalues():
            self.add_yellow_counters(unit)
            self.add_blue_counters(unit)

    def add_yellow_counters(self, unit):
        if hasattr(unit, "extra_life"):
            unit.yellow_counters = 1
        else:
            unit.yellow_counters = 0

    def add_blue_counters(self, unit):
        unit.blue_counters = 0
        if hasattr(unit, "frozen"):
            unit.blue_counters = unit.frozen
        if hasattr(unit, "attack_frozen"):
            unit.blue_counters = unit.attack_frozen
        if hasattr(unit, "just_bribed"):
            unit.blue_counters = 1


def save_gamestate(gamestate):
    return saver.save_gamestate(gamestate)


def load_gamestate(saved_gamestate):
    return saver.load_gamestate(saved_gamestate)


def write_gamestate(gamestate, path):
    pass


def read_gamestate(path):
    pass
