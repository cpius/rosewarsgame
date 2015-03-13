from __future__ import division
from action import Action
from common import *
from itertools import product


def get_actions(gamestate):

    is_extra_action = gamestate.is_extra_action()

    if not gamestate.get_actions_remaining() and not is_extra_action:
        return []

    actions = []
    for position, unit in gamestate.player_units.items():
        if can_use_unit(unit, is_extra_action):
            moves, attacks, abilities = get_unit_actions(unit, position, gamestate)

            if not can_attack_with_unit(gamestate, unit) or unit.attack == 0:
                attacks = []

            if melee_frozen(gamestate.enemy_units, position):
                moves = []

            actions += moves + attacks + abilities

    return actions


def get_unit_actions(unit, start_at, gamestate):

    def melee_attack_actions(moveset):
        return [Action(units, start_at=start_at, **terms) for terms in attack_generator(moveset)]

    def ranged_attack_actions(attackset):
        return [Action(units, start_at=start_at, end_at=start_at, target_at=target_at) for target_at in attackset]

    def ability_actions(abilityset, ability):
        return [Action(units, start_at=start_at, end_at=start_at, target_at=position, ability=ability) for position in abilityset]

    def move_actions(moveset):
        return [Action(units, start_at=start_at, end_at=end_at) for end_at in moveset]

    def generate_movesets(movement):
        return moves_sets(start_at, frozenset(units), zoc_blocks, movement, movement)

    def generate_extra_moveset():
        movement = unit.get_state(State.movement_remaining)
        return moves_set(start_at, frozenset(units), zoc_blocks, movement, movement)

    def attack_generator(moveset):
        """ Generates all the tiles a unit can attack based on the places it can move to. """
        for position, direction in product(moveset, directions):
            new_position = direction.move(position)
            if new_position in enemy_units:
                if not zoc_block(position, direction, zoc_blocks) and \
                        (not enemy_units[new_position].has_extra_life() or unit.has(Trait.push)):
                    yield {"end_at": position, "target_at": new_position, "move_with_attack": True}
                yield {"end_at": position, "target_at": new_position, "move_with_attack": False}

    def attack_generator_no_zoc_check(moveset):
        """ Generates all the tiles a unit can attack based on the places it can move to, without accounting for ZOC """
        for position, direction in product(moveset, directions):
            new_position = direction.move(position)
            if new_position in enemy_units:
                if enemy_units[new_position].has_extra_life() and not unit.has(Trait.push):
                    yield {"end_at": position, "target_at": new_position, "move_with_attack": False}
                else:
                    yield {"end_at": position, "target_at": new_position}

    def get_defence_maneuverability_actions():

        moveset_with_leftover, moveset_no_leftover = generate_movesets(2)
        moveset = moveset_with_leftover | moveset_no_leftover
        attacks = melee_attack_actions(moveset_with_leftover | {start_at})
        moves = move_actions(moveset)

        moves = [move for move in moves if abs(move.start_at.row - move.end_at.row) < 2]
        attacks = [attack for attack in attacks if abs(attack.start_at.row - attack.target_at.row) < 2]

        return moves, attacks

    def get_javelin_attacks():
        javelin_attacks = ranged_attack_actions(ranged_attacks_set(start_at, frozenset(enemy_units), 3))
        javelin_attacks = [attack for attack in javelin_attacks if distance(attack.end_at, attack.target_at) > 1]
        return javelin_attacks

    def get_extra_actions():

        def get_actions_combat_agility():
            for terms in attack_generator({start_at}):
                if terms["move_with_attack"]:
                    if unit.get_state(State.movement_remaining):
                        attacks.append(Action(units, start_at=start_at, **terms))
                else:
                    attacks.append(Action(units, start_at=start_at, **terms))
            return attacks

        moveset = generate_extra_moveset()
        moves = move_actions(moveset)

        attacks = []

        if unit.has(Trait.combat_agility):
            attacks = get_actions_combat_agility()
            moves = []

        if moves or attacks:
            moves.append(Action(units, start_at=start_at, end_at=start_at))  # Add an action for indicating pass on the extra action

        return moves, attacks

    def get_ride_through_attacks(attacks):
        for direction in directions:
            one_tile_away = direction.move(start_at)
            two_tiles_away = direction.move(one_tile_away)
            if one_tile_away in enemy_units and two_tiles_away in board and two_tiles_away not in units:
                attacks.append(Action(units, start_at=start_at, end_at=two_tiles_away, target_at=one_tile_away,
                               move_with_attack=False))
        return attacks

    def get_abilities():
        abilities = []
        for ability in unit.get_abilities():
            if ability in [Ability.sabotage, Ability.poison, Ability.assassinate]:
                target_positions = enemy_units
            elif ability in [Ability.improve_weapons]:
                target_positions = [pos for pos, target in player_units.items() if target.attack and target.is_melee()]
            elif ability == Ability.bribe:
                target_positions = [pos for pos, target in enemy_units.items() if not target.has(Effect.bribed)]
            else:
                target_positions = []

            abilityset = ranged_attacks_set(start_at, frozenset(target_positions), unit.range)
            if ability != Ability.assassinate or gamestate.actions_remaining == 1:
                abilities += ability_actions(abilityset, ability)

        return abilities

    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units
    units = merge_units(player_units, enemy_units)

    zoc_blocks = frozenset(position for position, enemy_unit in enemy_units.items() if unit.type in enemy_unit.zoc)

    moveset_with_leftover, moveset_no_leftover = generate_movesets(unit.movement)
    moveset = moveset_with_leftover | moveset_no_leftover
    moves = move_actions(moveset)
    if unit.is_ranged():
        attacks = ranged_attack_actions(ranged_attacks_set(start_at, frozenset(enemy_units), unit.range))
    else:
        attacks = melee_attack_actions(moveset_with_leftover | {start_at})
    abilities = get_abilities()

    if unit.has(Trait.rage):
        attacks += [Action(units, start_at=start_at, end_at=terms["end_at"], target_at=terms["target_at"], move_with_attack=False)
                    for terms in attack_generator_no_zoc_check(moveset_no_leftover)]

    if unit.has(Trait.berserking):

        moveset_with_leftover, moveset_no_leftover = moves_sets(start_at, frozenset(units), zoc_blocks, 4, 4)
        attacks = melee_attack_actions(moveset_with_leftover | {start_at})

    if unit.has(Trait.scouting):
        moves = move_actions(moves_set(start_at, frozenset(units), frozenset([]), unit.movement, unit.movement))

    if unit.has(Trait.defence_maneuverability):
        moves, attacks = get_defence_maneuverability_actions()

    if unit.has(State.extra_action):
        moves, attacks = get_extra_actions()

    if unit.has(Trait.ride_through):
        attacks = get_ride_through_attacks(attacks)

    if unit.has_javelin():
        attacks += get_javelin_attacks()

    return moves, attacks, abilities


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

    if movement_remaining <= 0:
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


def can_use_unit(unit, is_extra_action):
    is_frozen = unit.has(Effect.poisoned, 1) or unit.has(Effect.poisoned, 2)
    is_bribed = unit.has(State.recently_bribed)
    is_used = unit.has(State.used) and not unit.has(State.extra_action)

    if is_extra_action:
        return unit.has(State.extra_action) and not is_frozen and not is_bribed
    else:
        return not is_frozen and not is_bribed and not is_used


def melee_frozen(enemy_units, start_at):
    return any(pos for pos in start_at.adjacent_tiles() if unit_with_attribute_at(pos, Trait.melee_freeze, enemy_units))


def can_attack_with_unit(gamestate, unit):
    return not (gamestate.get_actions_remaining() == 1 and unit.has(Trait.double_attack_cost)) \
        and not unit.has(Effect.attack_frozen)
