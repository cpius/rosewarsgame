from collections import Counter
import math
from ai.ai_library import Player
from gamestate.gamestate_module import Unit
from gamestate.gamestate_library import directions, distance
from game.game_library import read_json
from gamestate.action_getter import UnitActions
from gamestate.enums import Effect, State, Trait, Ability


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
                unit.set(State.recently_bribed)
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

    def opponent_has_winning_action(self):
        return "1 action from backline" in self.factors[Player.opponent] or "1 action from backline, extra life" in self.factors[Player.opponent]


def get_moves_to_backline(unit, position, backline):
    if backline == 8:
        return math.ceil((8 - position.row) / unit.movement)
    else:
        return math.ceil((position.row - 1) / unit.movement)


def get_unit_factors(unit, position, gamestate, backline):

    def get_actions_to_backlines():
        if not can_use_unit(unit, gamestate):
            return
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
        if any(action.target_at and action.target_at.row == backline and action.move_with_attack for action in possible_actions):
            if unit.has_extra_life:
                return "1 attack from backline, extra life"
            else:
                return "1 attack from backline"

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

    if backline == 1:
        player_units = gamestate.enemy_units
        enemy_units = gamestate.player_units
    else:
        player_units = gamestate.player_units
        enemy_units = gamestate.enemy_units

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

    if unit.has_javelin:
        factors["Javelin"] += 1

    if unit.unit == Unit.Cannon:
        if unit.has(State.attack_frozen, 3):
            factors["2 counters on Cannon"] += 1
        if unit.has(State.attack_frozen, 2):
            factors["1 counter on Cannon"] += 1

    if unit.unit == Unit.Ballista:
        for enemy_position, enemy_unit in enemy_units.items():
            if distance(position, enemy_position) <= 3:
                factors["Enemy within range of Ballista"] += 1



    if unit.has(Trait.longsword):
        target_count = max(len(list((position.four_forward_tiles(direction) | {position.move(direction)}) & set(enemy_units))) for direction in directions)
        if target_count == 3:
            factors["Longswordsman can attack 3"] += 1
        if target_count >= 4:
            factors["Longswordsman can attack 4+"] += 1

    return factors


def can_use_unit(unit, gamestate):
    if unit.has(Effect.poisoned) or unit.has(State.recently_bribed):
        return False
    elif gamestate.is_extra_action():
        return unit.has(State.extra_action)
    return True
