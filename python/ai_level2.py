from __future__ import division
from operator import attrgetter
import ai_methods as m
import random as rnd
from common import *
from gamestate import Gamestate
from outcome import Outcome, rolls


outcome_success = Outcome(dict((key, rolls(1, 6)) for key in board))
outcome_failure = Outcome(dict((key, rolls(6, 1)) for key in board))


def get_values_and_score(gamestate, original_gamestate):

    values = get_action_values(gamestate, original_gamestate)
    player1_score = evaluate_action_values(values["player1"])
    player2_score = evaluate_action_values(values["player2"])
    score = player1_score - player2_score

    return values, score


def find_action_scores(actions, original_gamestate):

    gamestate_document = original_gamestate.to_document()

    for action in actions:

        potential_gamestate = Gamestate.from_document(gamestate_document)

        if action.is_attack():

            action.chance_of_win = m.chance_of_win(potential_gamestate, action.unit, action.target_unit, action)
            potential_gamestate.do_action(action, outcome_success)
            action.values_success, action.score_success = get_values_and_score(potential_gamestate, original_gamestate)

            potential_gamestate = Gamestate.from_document(gamestate_document)
            potential_gamestate.do_action(action, outcome_failure)
            action.values_failure, action.score_failure = get_values_and_score(potential_gamestate, original_gamestate)

            action.score = action.chance_of_win * action.score_success + \
                (1 - action.chance_of_win) * action.score_failure

        else:
            potential_gamestate.do_action(action, {})
            action.values, action.score = get_values_and_score(potential_gamestate, original_gamestate)

    return actions


def evaluate_action_values(values):
    return sum(value for value in values["gained"].values()) - sum(value for value in values["lost"].values())


def get_action_values(gamestate, original_gamestate):

    def get_values_unit_player(unit, position, gamestate):

        friendly_units = units_excluding_position(gamestate.player_units, position)
        all_units = dict(friendly_units.items() + gamestate.enemy_units.items())

        values = {}

        return values

    def get_values_unit_opponent(unit, position, gamestate):

        friendly_units = units_excluding_position(gamestate.player_units, position)
        all_units = dict(friendly_units.items() + gamestate.enemy_units.items())

        values = {}

        return values

    def give_back_bribed_units():
        for position, unit in gamestate.enemy_units.items():
            if hasattr(unit, "bribed"):
                gamestate.player_units()[position] = gamestate.enemy_units().pop(position)

        for position, unit in gamestate.player_units.items():
            if hasattr(unit, "bribed"):
                gamestate.enemy_units()[position] = gamestate.player_units().pop(position)

    def fill_values():

        new_player1 = set(gamestate.player_units) - set(original_gamestate.player_units)
        old_player1 = set(original_gamestate.player_units) - set(gamestate.player_units)

        new_player2 = set(gamestate.enemy_units) - set(original_gamestate.enemy_units)
        old_player2 = set(original_gamestate.enemy_units) - set(gamestate.enemy_units)

        for position in new_player1:
            values["player1"]["gained"] = get_values_unit_player(gamestate.player_units[position], position,
                                                                 gamestate)

        for position in old_player1:
            values["player1"]["lost"] = get_values_unit_player(original_gamestate.player_units[position], position,
                                                               gamestate)

        for key in values["player1"]["gained"].keys():
            if key in values["player1"]["lost"].keys():
                del values["player1"]["gained"][key]
                del values["player1"]["lost"][key]

        for position in new_player2:
            values["player2"]["gained"] = get_values_unit_opponent(gamestate.enemy_units[position], position,
                                                                   gamestate)

        for position in old_player2:
            values["player2"]["lost"] = get_values_unit_opponent(original_gamestate.enemy_units[position], position,
                                                                 gamestate)

    values = {"player1": {"gained": {}, "lost": {}}, "player2": {"gained": {}, "lost": {}}}

    give_back_bribed_units()

    fill_values()

    return values


def get_action(actions, gamestate):

    gamestate_copy = gamestate.copy()
    actions_copy = [action.copy() for action in actions]

    actions_copy = find_action_scores(actions_copy, gamestate_copy)
    rnd.shuffle(actions_copy)
    actions_copy.sort(key=attrgetter("score"), reverse=True)

    return actions_copy[0]


def get_upgrade(game):
    return 0