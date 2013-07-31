from __future__ import division
from action import Action
from common import *


def get_actions(gamestate):

    if not gamestate.get_actions_remaining() and not gamestate.extra_action:
        return []

    actions = []

    for position, unit in gamestate.player_units.items():
        if can_use_unit(unit):

            moves, attacks, abilities = get_unit_actions(unit, position, gamestate.opponent_units(),
                                                         gamestate.player_units)

            if not can_attack_with_unit(gamestate, unit):
                attacks = []

            if melee_frozen(gamestate.opponent_units(), position):
                moves = []

            actions += moves + attacks + abilities

    return actions


def get_unit_actions(unit, start_at, enemy_units, player_units):

    def make_action(terms):
        return Action(units, start_at, **terms)

    def melee_attack_actions(moveset):
        return [make_action(terms) for terms in attack_generator(moveset)]

    def ranged_attack_actions(attackset):
        return [Action(units, start_at, target_at=target_at) for target_at in attackset]

    def move_actions(moveset):
        return [Action(units, start_at, end_at=end_at) for end_at in moveset]

    def generate_movesets(movement):
        return moves_sets(start_at, frozenset(units), zoc_blocks, movement, movement)

    def generate_extra_moveset():
        movement = unit.get(Trait.movement_remaining)
        return moves_set(start_at, frozenset(units), zoc_blocks, movement, movement)

    def attack_generator(moveset):
        """ Generates all the tiles a unit can attack based on the places it can move to. """
        for position in moveset:
            for direction in directions:
                new_position = direction.move(position)
                if new_position in enemy_units:
                    if not zoc_block(position, direction, zoc_blocks):
                        yield {"end_at": position, "target_at": new_position, "move_with_attack": True}
                    yield {"end_at": position, "target_at": new_position, "move_with_attack": False}

    def attack_generator_no_zoc_check(moveset):
        """ Generates all the tiles a unit can attack based on the places it can move to, without accounting for ZOC """
        for position in moveset:
            for direction in directions:
                new_position = direction.move(position)
                if new_position in enemy_units:
                    yield {"end_at": position, "target_at": new_position}

    def rage():
        attacks = [make_action(terms) for terms in attack_generator(moveset_with_leftover | {start_at})] + \
                  [make_action(terms) for terms in attack_generator_no_zoc_check(moveset_no_leftover)]

        return moves, attacks

    def berserking():
        moveset_with_leftover, moveset_no_leftover = moves_sets(start_at, frozenset(units), zoc_blocks, 4, 4)
        attacks = [make_action(terms) for terms in attack_generator(moveset_with_leftover | {start_at})]
        return moves, attacks

    def defence_maneuverability():
        extended_moveset_no_leftover = set()
        for move_position in moveset_no_leftover:
            extended_moveset_no_leftover.add(move_position)
            for direction in [directions.Right, directions.Left]:
                new_position = direction.move(move_position)
                if new_position in board and new_position not in units:
                    extended_moveset_no_leftover.add(new_position)

        moves = move_actions(moveset_with_leftover | extended_moveset_no_leftover)

        return moves, attacks

    def extra_action():

        def get_actions_samurai():

            attacks = []
            for terms in attack_generator(moveset | {start_at}):
                if terms["move_with_attack"]:
                    if unit.get(Trait.movement_remaining):
                        attacks.append(Action(units, start_at, **terms))
                else:
                    attacks.append(Action(units, start_at, **terms))
            return attacks

        moveset = generate_extra_moveset()
        moves = move_actions(moveset)
        attacks = []

        if unit.has(Trait.combat_agility):
            attacks = get_actions_samurai()

        return moves, attacks

    def specialist_actions():

        abilities = []

        for ability in unit.abilities:
            if ability in [Ability.sabotage, Ability.sabotage_II]:
                target_positions = enemy_units

            elif ability in [Ability.improve_weapons, Ability.improve_weapons_II_A, Ability.improve_weapons_II_B]:
                target_positions = [pos for pos, target in player_units.items() if target.attack and target.is_melee()]

            elif ability in [Ability.bribe, Ability.bribe_II]:
                target_positions = [pos for pos, target in enemy_units.items() if not target.get(Trait.bribed) and not
                                    target.has(Trait.recently_bribed)]
            else:
                target_positions = []

            abilityset = ranged_attacks_set(start_at, frozenset(target_positions), unit.range)
            abilities += ability_actions(abilityset, ability)

        return moves, [], abilities

    def ranged_actions():
        attackset = ranged_attacks_set(start_at, frozenset(enemy_units), unit.range)
        attacks = ranged_attack_actions(attackset)

        return moves, attacks, []

    def ability_actions(abilityset, ability):
        return [Action(units, start_at, target_at=position, ability=ability) for position in abilityset]

    def scouting():
        moveset = moves_set(start_at, frozenset(units), frozenset([]), unit.movement, unit.movement)
        moves = move_actions(moveset)

        return moves, []

    zoc_blocks = frozenset(position for position, enemy_unit in enemy_units.items() if unit.type in enemy_unit.zoc)

    friendly_units = find_all_friendly_units_except_current(start_at, player_units)

    movement = unit.movement
    if cavalry_charging(start_at, friendly_units):
        movement += 1

    units = merge_units(player_units, enemy_units)

    moveset_with_leftover, moveset_no_leftover = generate_movesets(movement)
    moveset = moveset_with_leftover | moveset_no_leftover
    attacks = melee_attack_actions(moveset_with_leftover | {start_at})
    moves = move_actions(moveset)

    if unit.type == Type.Specialist:
        return specialist_actions()

    if unit.is_ranged():
        return ranged_actions()

    for trait in [Trait.extra_action, Trait.rage, Trait.berserking, Trait.scouting, Trait.defence_maneuverability]:
        if unit.has(trait):
            moves, attacks = locals()[Trait.reverse_mapping[trait]]()

    return moves, attacks, []


def zoc_block(position, direction, zoc_blocks):
    """ Returns whether an enemy unit exerting ZOC prevents you from going in 'direction' from 'position'. """
    return any(pos in zoc_blocks for pos in direction.perpendicular(position))


def adjacent_tiles_the_unit_can_move_to(position, units, zoc_blocks):
    for direction in directions:
        new_position = direction.move(position)
        if new_position in board and new_position not in units and not zoc_block(position, direction, zoc_blocks):
            yield new_position


@memoized
def moves_sets(position, units, zoc_blocks, total_movement, movement_remaining):
    """
    Returns all the tiles a unit can move to, in two sets.

    moveset_with_leftover: The tiles it can move to, and still have leftover movement to make an attack.
    moveset_no_leftover: The tiles it can move to, with no leftover movement to make an attack.
    """

    if movement_remaining == 0:
        return set(), {position}
    elif movement_remaining < total_movement:
        moveset_with_leftover = {position}
    else:
        moveset_with_leftover = set()

    moveset_no_leftover = set()

    for new_position in adjacent_tiles_the_unit_can_move_to(position, units, zoc_blocks):
        movesets = moves_sets(new_position, units, zoc_blocks, total_movement, movement_remaining - 1)
        moveset_with_leftover |= movesets[0]
        moveset_no_leftover |= movesets[1]

    return moveset_with_leftover, moveset_no_leftover


@memoized
def moves_set(position, units, zoc_blocks, total_movement, movement_remaining):
    """Returns all the tiles a unit can move to. """

    if not movement_remaining:
        return {position}
    elif movement_remaining < total_movement:
        moveset = {position}
    else:
        moveset = set()

    for new_position in adjacent_tiles_the_unit_can_move_to(position, units, zoc_blocks):
        moveset |= moves_set(new_position, units, zoc_blocks, total_movement, movement_remaining - 1)

    return moveset


@memoized
def ranged_attacks_set(position, enemy_units, range_remaining):
    """ Returns all the tiles a ranged unit can attack"""

    attackset = set()

    if position in enemy_units:
        attackset.add(position)

    if range_remaining:
        for new_position in position.adjacent_tiles():
            attackset |= ranged_attacks_set(new_position, enemy_units, range_remaining - 1)

    return attackset


def can_use_unit(unit):
    return not unit.has(Trait.frozen) and not unit.has(Trait.recently_bribed) and not \
        (unit.has(Trait.used and not unit.has(Trait.extra_action)))


def melee_frozen(enemy_units, start_at):
    return any(pos for pos in start_at.adjacent_tiles() if unit_with_trait_at(pos, Trait.melee_freeze, enemy_units))


def can_attack_with_unit(gamestate, unit):
    return not (gamestate.get_actions_remaining() == 1 and unit.has(Trait.double_attack_cost)) \
        and not unit.has(Trait.attack_frozen)


def cavalry_charging(start_at, friendly_units):
    return any(pos for pos in start_at.surrounding_tiles() if
               unit_with_trait_at(pos, Trait.cavalry_charging, friendly_units))


def merge_units(units1, units2):
    units = units1.copy()
    units.update(units2)
    return units


def unit_with_trait_at(pos, trait, units):
    return pos in units and units[pos].has(trait)
