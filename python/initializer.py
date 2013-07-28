from __future__ import division


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
