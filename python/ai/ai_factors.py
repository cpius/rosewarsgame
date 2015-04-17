from gamestate.gamestate_library import Position
from collections import Counter
import math
from ai.ai_library import Player
from gamestate.gamestate_module import Unit
from game.game_library import read_json
from gamestate.action_getter import UnitActions
from gamestate.enums import Effect


class Factors:
    def __init__(self, gamestate):
        self.factors = {Player.player: Counter(), Player.opponent: Counter()}
        for pos, unit in gamestate.player_units.items():
            if not unit.has(Effect.bribed):
                self.factors[Player.player] += get_unit_factors(unit, pos, gamestate, 8)
            else:
                self.factors[Player.opponent] += get_unit_factors(unit, pos, gamestate, 1)
        for pos, unit in gamestate.enemy_units.items():
            if not unit.has(Effect.bribed):
                self.factors[Player.opponent] += get_unit_factors(unit, pos, gamestate, 1)
            else:
                self.factors[Player.player] += get_unit_factors(unit, pos, gamestate, 8)

        self.values = read_json("./ai/values.json")

    def subtract(self, other):
        for player in list(Player):
            self.factors[player].subtract(other.factors[player])

    def __repr__(self):
        player_strings = []
        for player in list(Player):
            items = []
            for elem, count in self.factors[player].items():
                if count != 0:
                    items.append("'" + elem + "'" + " " + str(count))
            if items:
                player_strings.append(str(player) + ": " + ", ".join(items))
        s = ". ".join(player_strings)
        if not s:
            return "%"
        else:
            return s + "."

    def get_score(self):
        score = 0
        for factor, value in self.factors[Player.player].items():
            score += self.values[factor][0] * value
        for factor, value in self.factors[Player.opponent].items():
            score -= self.values[factor][1] * value
        return score

    def is_winning(self):
        return "Backline" in self.factors[Player.player]


def get_moves_to_backline(unit, position, backline):
    if backline == 8:
        return math.ceil((8 - position.row) / unit.movement)
    else:
        return math.ceil((position.row - 1) / unit.movement)



def get_unit_factors(unit, position, gamestate, backline):

    def get_actions_to_backlines():
        gamestate_copy = gamestate.copy()
        if backline == 1:
            gamestate_copy.board.units = gamestate_copy.board.units[::-1]
            gamestate_copy.board.units[0] = {position: unit}
        unit_actions = UnitActions(unit, position, gamestate_copy, gamestate.bonus_tiles)
        unit_actions.set_zoc_blocks()
        possible_actions = unit_actions.get_all_actions()
        if any(action.end_at.row == backline for action in possible_actions):
            if unit.has_extra_life:
                return "1 action from backline, extra life"
            else:
                return "1 action from backline"

    def get_backline_factor():
        moves_to_backline = get_moves_to_backline(unit, position, backline)

        if moves_to_backline == 1:
            actions_to_backline = get_actions_to_backlines()
            if actions_to_backline:
                return actions_to_backline

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
