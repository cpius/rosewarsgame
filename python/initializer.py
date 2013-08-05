from __future__ import division
from common import *

remove_traits = [Trait.used, Trait.sabotaged, Trait.sabotaged_II, Trait.improved_weapons, Trait.improved_weapons_II_B,
                 Trait.recently_bribed]

decrement_traits = [Trait.frozen, Trait.attack_frozen, Trait.improved_weapons_II_A]


def initialize_turn(gamestate):

    def resolve_bribe(unit):
        if unit.is_bribed():
            gamestate.player_units[position] = gamestate.enemy_units.pop(position)
            unit.set(Trait.recently_bribed)
            gamestate.player_units[position].remove(Trait.bribed)

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units.items():
        for trait in remove_traits:
            unit.remove(trait)
        for trait in decrement_traits:
            unit.decrement(trait)

        resolve_bribe(unit)
