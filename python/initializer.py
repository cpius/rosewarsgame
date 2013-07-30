from __future__ import division


def initialize_turn(gamestate):

    def resolve_bribe(unit, opponent_units, player_units):
        if unit.get("bribed"):
            player_units[position] = opponent_units.pop(position)
            unit.set_recently_bribed()
            player_units[position].remove_bribed()

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units().items():
        for attr in ["used", "sabotage", "sabotage_II", "improved_weapons", "improved_weapons_II_B", "recently_bribed"]:
            unit.remove(attr)
        for attr in ["frozen", "attack_frozen", "improved_weapons_II_A"]:
            unit.decrement(attr)

    for opponent_unit_position, opponent_unit in gamestate.opponent_units().items():
        opponent_unit.remove("used")
        resolve_bribe(opponent_unit, gamestate.opponent_units(), gamestate.player_units())
