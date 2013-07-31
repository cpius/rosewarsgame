from __future__ import division
from common import *


def initialize_turn(gamestate):

    def resolve_bribe(unit):
        if unit.has(Trait.bribed):
            gamestate.player_units[position] = gamestate.enemy_units.pop(position)
            unit.set(Trait.recently_bribed)
            gamestate.player_units[position].remove(Trait.bribed)

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units.items():
        for attr in [Trait.used, Trait.sabotaged, Trait.sabotaged_II, Trait.improved_weapons,
                     Trait.improved_weapons_II_B, Trait.recently_bribed]:
            unit.remove(attr)
        for attr in [Trait.frozen, Trait.attack_frozen, Trait.improved_weapons_II_A]:
            unit.decrement(attr)

        resolve_bribe(unit)
