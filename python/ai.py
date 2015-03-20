from operator import attrgetter
import random as rnd
from common import *
from gamestate import Gamestate
from outcome import Outcome, rolls
import math
from itertools import product
from collections import Counter
import os
import battle


class AI():
    def __init__(self):
        level = get_setting("AI_level")
        if level == 1:
            self.select_action = get_select_action_function(score_actions_simple)
        elif level == 2:
            self.select_action = get_select_action_function(score_actions_considering_one_action)
        elif level == 3:
            self.select_action = get_select_action_function(score_actions_considering_two_actions)

        self.select_upgrade = select_upgrade

success = Outcome(dict((key, rolls(1, 6)) for key in board_tiles))
failure = Outcome(dict((key, rolls(6, 1)) for key in board_tiles))


values = {"Backline": [10000, 10000],
          "1 action from backline": [200, 5000],
          "1 action from backline, extra life": [280, 5000],
          "1 attack from backline": [100, 400],
          "1 attack from backline, extra_life": [140, 500],
          "1 move(s) from backline, extra life": [90, 90],
          "2 move(s) from backline, extra life": [40, 40],
          "3 move(s) from backline, extra life": [20, 20],
          "1 move(s) from backline, defence 1": [35, 35],
          "1 move(s) from backline, defence 2": [40, 40],
          "1 move(s) from backline, defence 3": [60, 60],
          "1 move(s) from backline, defence 4": [80, 80],
          "2 move(s) from backline, defence 1": [8, 8],
          "2 move(s) from backline, defence 2": [10, 10],
          "2 move(s) from backline, defence 3": [20, 20],
          "2 move(s) from backline, defence 4": [30, 30],
          "Basic unit": [40, 40],
          "Special unit": [90, 90]
          }


def document_actions(actions, game):
    def get_path():
        if not os.path.exists(game.savegame_folder()):
            os.makedirs(game.savegame_folder())

        return game.savegame_folder() + "/" + str(game.gamestate.action_count + 1) + ".txt"

    def write_factors(factors):
        for player, aspect in product(["player", "opponent"], ["gain", "loss"]):
            if factors[player][aspect]:
                out.write(player + " " + aspect + ": " + str(factors[player][aspect]) + "\n")

    def write_score(score):
        out.write("Score: " + str(round(score, 2)) + "\n")

    def write_attack_results(a):
        out.write("factors if win\n")
        write_factors(a.factors_if_win)
        out.write("\n")
        out.write("factors if loss\n")
        if any(a.factors_if_loss[player][aspect] for player, aspect in product(["player", "opponent"], ["gain", "loss"])):
            write_factors(a.factors_if_loss)
        else:
            out.write("None\n")
        out.write("\n")

    with open(get_path(), 'w') as out:
        for a in actions:
            out.write(" -- " + str(a) + " -- \n")
            if a.is_attack:
                out.write("Chance of success: " + str(round(a.chance * 100)) + "%\n\n")
                if hasattr(a, "a2_if_win"):
                    out.write("- Second action if win: " + str(a.a2_if_win) + " -\n")
                    if a.a2_if_win.is_attack:
                        out.write("Chance of success: " + str(round(a.a2_if_win.chance * 100)) + "%\n\n")
                        write_attack_results(a.a2_if_win)
                    else:
                        write_factors(a.a2_if_win.factors)
                        out.write("\n")

                    out.write("- Second action if loss: " + str(a.a2_if_loss) + " -\n")
                    if a.a2_if_loss.is_attack:
                        out.write("Chance of success: " + str(round(a.a2_if_loss.chance * 100)) + "%\n\n")
                        write_attack_results(a.a2_if_loss)
                    else:
                        write_factors(a.a2_if_loss.factors)

                    write_score(a.score)

                else:
                    write_attack_results(a)
                    write_score(a.score)

            else:
                out.write("\n")
                if hasattr(a, "a2"):
                    out.write("Second action: " + str(a.a2) + "\n")
                    if a.a2.is_attack:
                        out.write("Chance of success: " + str(round(a.a2.chance * 100)) + "%\n")
                        out.write("\n")
                        write_attack_results(a.a2)
                    else:
                        write_factors(a.a2.factors)
                    write_score(a.score)
                else:

                    write_factors(a.factors)
                    write_score(a.score)

            out.write("\n----------------------------------------------------------------------------------\n\n")


def one_action_forward(action, g0, outcome=None):
    g1 = Gamestate.copy(g0)
    action.update_references(g1)
    g1.do_action(action, outcome)
    return g1


def score_actions_considering_one_action(g0):
    return score_actions_considering_one_more_action(g0, g0)


def score_actions_considering_one_more_action(g1, g0):
    actions = g1.get_actions()
    for a in actions:
        if a.has_outcome:
            g2_win = one_action_forward(a, g1, success)
            g2_loss = one_action_forward(a, g1, failure)
            a.chance = chance_of_win(g1, a)
            g0_factors = get_gamestate_factors(g0)
            a.factors_if_win = get_differences(g0_factors, g2_win)
            a.factors_if_loss = get_differences(g0_factors, g2_loss)
            a.score = a.chance * get_score(a.factors_if_win) + (1 - a.chance) * get_score(a.factors_if_loss)
        else:
            g2 = one_action_forward(a, g1)
            g0_factors = get_gamestate_factors(g0)
            a.factors = get_differences(g0_factors, g2)
            a.score = get_score(a.factors)
    return actions


def get_gamestate_factors(g):
    factors = {"player": Counter(), "opponent": Counter()}
    for pos, unit in g.player_units.items():
        factors["player"] += get_unit_factors(unit, pos, g, 8)
    for pos, unit in g.enemy_units.items():
        factors["opponent"] += get_unit_factors(unit, pos, g, 1)

    return factors


def score_actions_considering_two_actions(g0):
    g0.ai_factors = {}
    if not any(unit.name == Unit.Crusader for unit in g0.player_units.values()):
        g0.ai_factors["No_player_Crusader"] = 1
    if not any(unit.name == "Flag Bearer" for unit in g0.player_units.values()):
        g0.ai_factors["No_FlagBearer"] = 1

    g0_factors = get_gamestate_factors(g0)

    actions = g0.get_actions()
    for a in actions:
        if a.is_attack:
            g1_if_win = one_action_forward(a, g0, success)
            g1_if_loss = one_action_forward(a, g0, failure)
            a.chance = chance_of_win(g0, a)
            if g1_if_win.actions_remaining:
                a.a2_if_win = max(score_actions_considering_one_more_action(g1_if_win, g0_factors), key=attrgetter("score"))
                a.a2_if_loss = max(score_actions_considering_one_more_action(g1_if_loss, g0_factors), key=attrgetter("score"))
                a.score = a.chance * a.a2_if_win.score + (1 - a.chance) * a.a2_if_loss.score
            else:
                a.factors_if_win = get_differences(g0_factors, g1_if_win)
                a.factors_if_loss = get_differences(g0_factors, g1_if_loss)
                a.score = a.chance * get_score(a.factors_if_win) + (1 - a.chance) * get_score(a.factors_if_loss)
        else:
            g1 = one_action_forward(a, g0)
            if g1.actions_remaining:
                a.a2 = max(score_actions_considering_one_more_action(g1, g0_factors), key=attrgetter("score"))
                a.score = a.a2.score
            else:
                a.factors = get_differences(g0_factors, g1)
                a.score = get_score(a.factors)
    return actions


def get_unit_factors(unit, position, gamestate, backline):

    enemy_units = gamestate.enemy_units

    def get_backline_value():

        def get_coloumn_blocks():
            coloumn_blocks = 0
            for row in range(position.row, backline + 1):
                if Position(position.column, row) in enemy_units:
                    coloumn_blocks += 1
                for i in [-1, +1]:
                    zoc_position = Position(position.column + i, row)
                    if zoc_position in enemy_units and unit.type in enemy_units[zoc_position].zoc:
                        coloumn_blocks += 1

            return coloumn_blocks

        moves_to_backline = get_moves_to_backline(unit, position, backline)
        coloumn_blocks = get_coloumn_blocks()

        if moves_to_backline == 0:
            return "Backline"

        if unit.has_extra_life:
            if moves_to_backline < 4:
                return str(int(moves_to_backline)) + " move(s) from backline, extra life"

        if moves_to_backline == 1 and coloumn_blocks <= 1:
            defence = unit.defence
            if defence > 3:
                defence = 4
            return "1 move(s) from backline, defence " + str(defence)

        if moves_to_backline == 2 and coloumn_blocks <= 1:
            defence = unit.defence
            if defence > 3:
                defence = 4
            return "2 move(s) from backline, defence " + str(defence)

    def get_unit_value():
        if unit.name in ["Archer", "Pikeman", "Catapult", "Ballista", "Knight", "Light Cavalry"]:
            return "Basic unit"
        else:
            return "Special unit"

    factors = Counter()
    for function in [get_backline_value, get_unit_value]:
        factor = function()
        if factor:
            factors[factor] += 1
    return factors


def get_moves_to_backline(unit, position, backline):
    if backline == 8:
        return math.ceil((8 - position.row) / unit.movement)
    else:
        return math.ceil(position.row / unit.movement)


def get_differences(g0_factors, g1):

    def give_back_bribed_units():
        for position, unit in g1.enemy_units.items():
            if hasattr(unit, "bribed"):
                g1.player_units[position] = g1.enemy_units.pop(position)

    g1_factors = {"player": Counter(), "opponent": Counter()}

    give_back_bribed_units()

    for pos, unit in g1.player_units.items():
        g1_factors["player"] += get_unit_factors(g1.player_units[pos], pos, g1, 8)

    for pos, unit in g1.enemy_units.items():
        g1_factors["opponent"] += get_unit_factors(g1.enemy_units[pos], pos, g1, 1)

    factors = {"player": {"gain": {}, "loss": {}}, "opponent": {"gain": {}, "loss": {}}}
    player_intersection = g0_factors["player"] & g1_factors["player"]
    factors["player"]["gain"] = g1_factors["player"] - player_intersection
    factors["player"]["loss"] = g0_factors["player"] - player_intersection

    opponent_intersection = g0_factors["opponent"] & g1_factors["opponent"]
    factors["opponent"]["gain"] = g1_factors["opponent"] - opponent_intersection
    factors["opponent"]["loss"] = g0_factors["opponent"] - opponent_intersection

    return factors


def get_score(factors):
    return sum(values[key][0] * value for key, value in factors["player"]["gain"].items()) -\
        sum(values[key][0] * value for key, value in factors["player"]["loss"].items()) -\
        sum(values[key][0] * value for key, value in factors["opponent"]["gain"].items()) +\
        sum(values[key][0] * value for key, value in factors["opponent"]["loss"].items())


def chance_of_win(gamestate, action):

    attack = battle.get_attack(action, gamestate)
    defence = battle.get_defence(action, attack, gamestate)

    if attack < 0:
        attack = 0
    if attack > 6:
        attack = 6
    if defence < 0:
        defence = 0
    if defence > 6:
        defence = 6

    chance_of_attack_successful = attack / 6
    chance_of_defence_unsuccessful = (6 - defence) / 6

    return chance_of_attack_successful * chance_of_defence_unsuccessful


def score_actions_simple(g):

    actions = g.get_actions()
    go_for = rnd.choice(["attack", "move_forward"])

    if go_for == "attack":
        for a in actions:
            if a.is_attack:
                a.score = chance_of_win(g, a)
                if a.double_cost:
                    a.score /= 2
            else:
                a.score = 0

    elif go_for == "move_forward":
        for action in actions:
            action.score = action.end_at.row
            if action.end_at.row > action.start_at.row:
                action.score += 1
            if action.is_attack:
                action.score += 0.25
                if action.target_at.row > action.end_at.row and action.move_with_attack:
                    action.score += 0.5

    return actions


def get_select_action_function(score_function):

    def select_action(game):
        gamestate_copy = game.gamestate.copy()
        gamestate_copy.set_available_actions()
        actions_copy = score_function(gamestate_copy)
        actions_copy.sort(key=attrgetter("score"), reverse=True)
        if get_setting("Document_ai_decisions") and get_setting("AI_level") > 1:
            document_actions(actions_copy, game)
        return next(action for action in game.gamestate.get_actions() if action == actions_copy[0])
    return select_action


def select_upgrade(gamestate):
    return 0
