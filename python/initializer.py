from __future__ import division
from common import *


def zoc(unit, position, enemy_units):
    """ Returns whether an enemy unit can exert ZOC on a friendly unit """
    return position in enemy_units and unit.type in enemy_units[position].get_zoc()


def find_all_friendly_units_except_current(current_unit_position, p):
    return dict((position, p[0].units[position]) for position in p[0].units if position != current_unit_position)


def initialize_action(gamestate):

    def initialize_crusader():
        for position, unit in gamestate.player_units().items():
            if any(surrounding_position in gamestate.player_units()
                   and hasattr(gamestate.player_units()[surrounding_position], "crusading") and unit.range == 1
                   for surrounding_position in surrounding_tiles(position)):
                unit.variables["is_crusading"] = True
            else:
                if hasattr(unit, "is_crusading"):
                    del unit.variables["is_crusading"]

    initialize_crusader()


def initialize_turn(gamestate):

    def resolve_bribe(unit, opponent_units, player_units):
        if unit.get_bribed():
            player_units[position] = opponent_units.pop(position)
            unit.set_recently_bribed()
            player_units[position].remove_bribed()

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units().items():
        unit.remove_used()
        unit.remove_xp_gained_this_turn()
        unit.decrement_frozen()
        unit.decrement_attack_frozen()
        unit.remove_sabotaged()
        unit.remove_sabotaged_II()
        unit.remove_improved_weapons()
        unit.decrease_improved_weapons_II_A()
        unit.remove_improved_weapons_II_B()
        unit.remove_recently_bribed()

    for opponent_unit_position, opponent_unit in gamestate.opponent_units().items():
        opponent_unit.variables["used"] = False
        resolve_bribe(opponent_unit, gamestate.opponent_units(), gamestate.player_units())
