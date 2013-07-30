from __future__ import division


def initialize_turn(gamestate):

    def resolve_bribe(unit):
        if unit.has("bribed"):
            gamestate.player_units()[position] = gamestate.opponent_units().pop(position)
            unit.set("recently_bribed")
            gamestate.player_units()[position].remove("bribed")

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units().items():
        for attr in ["used", "sabotage", "sabotage_II", "improved_weapons", "improved_weapons_II_B", "recently_bribed"]:
            unit.remove(attr)
        for attr in ["frozen", "attack_frozen", "improved_weapons_II_A"]:
            unit.decrement(attr)

        resolve_bribe(unit)

