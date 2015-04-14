from gamestate.gamestate_library import Position
from collections import Counter
import math
from ai.ai_library import Player
from gamestate.gamestate_module import Unit
from game.game_library import read_json
from gamestate.action_getter import UnitActions


class FactorScorer:
    def __init__(self):
        self.values = self.read_values()

    @staticmethod
    def read_values():
        return read_json("./ai/values.json")

    def get_score(self, factors):
        score = 0
        for factor, value in factors[Player.player].items():
            score += self.values[factor][0] * value
        for factor, value in factors[Player.opponent].items():
            score -= self.values[factor][1] * value
        return score


def get_moves_to_backline(unit, position, backline):
    if backline == 8:
        return math.ceil((8 - position.row) / unit.movement)
    else:
        return math.ceil(position.row / unit.movement)


def get_unit_factors(unit, position, gamestate, backline):

    def get_backline_factor():
        moves_to_backline = get_moves_to_backline(unit, position, backline)

        if moves_to_backline == 1:
            gamestate_copy = gamestate.copy()
            gamestate_copy.board.units = gamestate_copy.board.units[::-1]
            unit_actions = UnitActions(unit, position, gamestate_copy, gamestate.bonus_tiles)
            possible_actions = unit_actions.get_all_actions()
            if any(action.end_at.row == backline for action in possible_actions):
                if unit.has_extra_life:
                    return "1 action from backline, extra life"
                else:
                    return "1 action from backline"

        if moves_to_backline <= 3 and unit.has_extra_life:
            return str(moves_to_backline) + " move(s) from backline, extra life"

        if moves_to_backline <= 2 and not unit.has_extra_life:
            return str(moves_to_backline) + " move(s) from backline, defence " + str(unit.defence)

    factors = Counter()

    if position.row == backline:
        factors["Backline"] += 1
        return factors

    if unit.unit in [Unit.Archer, Unit.Ballista, Unit.Catapult, Unit.Knight, Unit.Light_Cavalry, Unit.Pikeman]:
        factors["Basic unit"] += 1
    else:
        factors["Special unit"] += 1

    backline_factor = get_backline_factor()
    if backline_factor:
        factors[backline_factor] += 1

    return factors


def get_factors(gamestate):
    factors = {Player.player: Counter(), Player.opponent: Counter()}
    for pos, unit in gamestate.player_units.items():
        factors[Player.player] += get_unit_factors(unit, pos, gamestate, 8)
    for pos, unit in gamestate.enemy_units.items():
        factors[Player.opponent] += get_unit_factors(unit, pos, gamestate, 1)

    return factors


def get_differences(factors_1, factors_2):
    differences = {}
    for player in list(Player):
        a = factors_1[player].copy()
        a.subtract(factors_2[player])
        differences[player] = a

    return differences

