from __future__ import division
from operator import attrgetter
import random as rnd
from common import *
from gamestate import Gamestate
from outcome import Outcome, rolls
import math
from itertools import product
from dictdiffer import DictDiffer
import battle
import os


class AI():
    def __init__(self):
        level = get_setting("AI_level")
        if level == 1:
            self.select_action = get_select_action_function(score_actions_simple)
            self.select_upgrade = select_upgrade
        elif level == 2:
            self.select_action = get_select_action_function(score_actions_considering_one_action)
            self.select_upgrade = select_upgrade
        elif level == 3:
            self.select_action = get_select_action_function(score_actions_considering_two_actions)
            self.select_upgrade = select_upgrade

success = Outcome(dict((key, rolls(1, 6)) for key in board))
failure = Outcome(dict((key, rolls(6, 1)) for key in board))

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
            if a.is_attack():
                out.write("Chance of success: " + str(round(a.chance * 100)) + "%\n\n")
                if hasattr(a, "a2_if_win"):
                    out.write("- Second action if win: " + str(a.a2_if_win) + " -\n")
                    if a.a2_if_win.is_attack():
                        out.write("Chance of success: " + str(round(a.a2_if_win.chance * 100)) + "%\n\n")
                        write_attack_results(a.a2_if_win)
                    else:
                        write_factors(a.a2_if_win.factors)
                        out.write("\n")

                    out.write("- Second action if loss: " + str(a.a2_if_loss) + " -\n")
                    if a.a2_if_loss.is_attack():
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
                    if a.a2.is_attack():
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


def score_actions_considering_one_more_action(g0, g1):
    actions = g1.get_actions()
    for a in actions:
        if a.is_attack():
            g2_win = one_action_forward(a, g1, success)
            g2_loss = one_action_forward(a, g1, failure)
            a.chance = chance_of_win(g0, a.unit, a.target_unit, a)
            a.factors_if_win = get_differences(g0, g2_win)
            a.factors_if_loss = get_differences(g0, g2_loss)
            a.score = a.chance * get_score(a.factors_if_win) + (1 - a.chance) * get_score(a.factors_if_loss)
        else:
            g2 = one_action_forward(a, g1)
            a.factors = get_differences(g0, g2)
            a.score = get_score(a.factors)
    return actions


def score_actions_considering_two_actions(g0):
    actions = g0.get_actions()
    for a in actions:
        if a.is_attack():
            g1_if_win = one_action_forward(a, g0, success)
            g1_if_loss = one_action_forward(a, g0, failure)
            a.chance = chance_of_win(g0, a.unit, a.target_unit, a)
            if g1_if_win.actions_remaining:
                a.a2_if_win = max(score_actions_considering_one_more_action(g0, g1_if_win), key=attrgetter("score"))
                a.a2_if_loss = max(score_actions_considering_one_more_action(g0, g1_if_loss), key=attrgetter("score"))
                a.score = a.chance * a.a2_if_win.score + (1 - a.chance) * a.a2_if_loss.score
            else:
                a.factors_if_win = get_differences(g0, g1_if_win)
                a.factors_if_loss = get_differences(g0, g1_if_loss)
                a.score = a.chance * get_score(a.factors_if_win) + (1 - a.chance) * get_score(a.factors_if_loss)
        else:
            g1 = one_action_forward(a, g0)
            if g1.actions_remaining:
                a.a2 = max(score_actions_considering_one_more_action(g0, g1), key=attrgetter("score"))
                a.score = a.a2.score
            else:
                a.factors = get_differences(g0, g1)
                a.score = get_score(a.factors)
    return actions


def get_differences(g0, g1):
    def get_unit_factors(unit, position, gamestate, backline):
        def get_backline_value():
            def get_coloumn_blocks():
                columns = [position.column + i for i in [-1, 0, 1] if position.column + i in [1, 2, 3, 4, 5]]
                coloumn_blocks = []
                for column in columns:
                    blocks = 0
                    for enemy_position, enemy_unit in gamestate.enemy_units.items():
                        if (enemy_position.column == column and enemy_position.row > position.row) or \
                            ((enemy_position.column == column - 1 or enemy_position.column == column + 1) and
                             enemy_position.row >= position.row and enemy_unit.zoc and unit.type in enemy_unit.zoc):
                            blocks += 1
                    coloumn_blocks.append(blocks)
                return coloumn_blocks

            def get_moves_to_backline(unit, position):
                if backline == 8:
                    return math.ceil((8 - position.row) / unit.movement)
                else:
                    return math.ceil(position.row / unit.movement)

            moves_to_backline = get_moves_to_backline(unit, position)
            coloumn_blocks = get_coloumn_blocks()

            if moves_to_backline == 0:
                return "Backline"

            if unit.has_extra_life():
                if moves_to_backline < 4:
                    return str(int(moves_to_backline)) + " move(s) from backline, extra life"

            if moves_to_backline == 1 and coloumn_blocks[1] <= 1:
                defence = unit.defence
                if defence > 3:
                    defence = 4
                return "1 move(s) from backline, defence " + str(defence)

            if moves_to_backline == 2:
                defence = unit.defence
                if defence > 3:
                    defence = 4
                return "2 move(s) from backline, defence " + str(defence)

        def get_unit_value():
            if unit.name in ["Archer", "Pikeman", "Catapult", "Ballista", "Knight", "Light Cavalry"]:
                return "Basic unit"
            else:
                return "Special unit"

        factors = []
        for function in [get_backline_value, get_unit_value]:
            factor = function()
            if factor:
                factors.append(factor)
        return factors

    def give_back_bribed_units():
        for position, unit in g1.enemy_units.items():
            if hasattr(unit, "bribed"):
                g1.player_units[position] = g1.enemy_units.pop(position)

    def fill_values():

        player_difference = DictDiffer(g1.player_units, g0.player_units)
        opponent_difference = DictDiffer(g1.enemy_units, g0.enemy_units)

        for pos in player_difference.added():
            factors["player"]["gain"] += get_unit_factors(g1.player_units[pos], pos, g1, 8)
        for pos in player_difference.changed():
            pass
        for pos in player_difference.removed():
            factors["player"]["loss"] += get_unit_factors(g0.player_units[pos], pos, g1, 8)

        for pos in opponent_difference.added():
            factors["opponent"]["gain"] += get_unit_factors(g1.enemy_units[pos], pos, g1, 1)
        for pos in opponent_difference.changed():
            pass
        for pos in opponent_difference.removed():
            factors["opponent"]["loss"] += get_unit_factors(g0.enemy_units[pos], pos, g1, 1)

    def remove_duplicates(player_factors):

        rmlist = []
        for factor in player_factors["loss"]:
            if factor in player_factors["gain"]:
                player_factors["gain"].remove(factor)
                rmlist.append(factor)

        for element in rmlist:
            player_factors["loss"].remove(element)

    factors = {"player": {"gain": [], "loss": []}, "opponent": {"gain": [], "loss": []}}

    give_back_bribed_units()

    fill_values()

    remove_duplicates(factors["player"])

    return factors


def get_score(factors):
    return sum(values[e][0] for e in factors["player"]["gain"]) - \
        sum(values[e][0] for e in factors["player"]["loss"]) - \
        sum(values[e][1] for e in factors["opponent"]["gain"]) + \
        sum(values[e][1] for e in factors["opponent"]["loss"])


def chance_of_win(gamestate, attacking_unit, defending_unit, action):

    attack_rating = battle.get_attack_rating(attacking_unit, defending_unit, action, gamestate.player_units)
    defence_rating = battle.get_defence_rating(attacking_unit, defending_unit, attack_rating, action, gamestate.enemy_units)

    if attack_rating < 0:
        attack_rating = 0

    if attack_rating > 6:
        attack_rating = 6

    if defence_rating < 0:
        defence_rating = 0

    if defence_rating > 6:
        defence_rating = 6

    chance_of_attack_successful = attack_rating / 6

    chance_of_defence_unsuccessful = (6 - defence_rating) / 6

    return chance_of_attack_successful * chance_of_defence_unsuccessful


def score_actions_simple(g):

    actions = g.get_actions()
    go_for = rnd.choice(["attack", "move_forward"])

    if go_for == "attack":
        for a in actions:
            if a.is_attack():
                a.score = chance_of_win(g, a.unit, a.target_unit, a)
                if a.double_cost:
                    a.score /= 2
            else:
                a.score = 0

    elif go_for == "move_forward":
        for action in actions:
            action.score = action.end_at.row
            if action.end_at.row > action.start_at.row:
                action.score += 1
            if action.is_attack():
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
        if get_setting("Document_AI_decisions") and get_setting("AI_level") > 1:
            document_actions(actions_copy, game)
        return next(action for action in game.gamestate.get_actions() if action == actions_copy[0])
    return select_action


def select_upgrade(gamestate):
    return 0
