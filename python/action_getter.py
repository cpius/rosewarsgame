from __future__ import division
import settings
from action import Action
import collections
import functools
from common import *
from action import MoveOrStay


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj):
        return functools.partial(self.__call__, obj)


def find_all_friendly_units_except_current(current_unit_position, player_units):
    return dict((position, player_units[position]) for position in player_units if position != current_unit_position)


def add_target_reference(action, enemy_units, player_units):
    if action.is_attack():
        action.target_reference = enemy_units[action.attack_position]
    elif action.is_ability():
        if action.ability_position in enemy_units:
            action.target_reference = enemy_units[action.ability_position]
        elif action.ability_position in player_units:
            action.target_reference = player_units[action.ability_position]

    for sub_action in action.sub_actions:
        add_target_reference(sub_action, enemy_units, player_units)


def get_actions(gamestate):

    def can_use_unit(unit):
        return not (unit.is_used() or unit.is_frozen() or unit.get_recently_bribed())

    def moving_allowed(unit_position):
        return not any(position for position in adjacent_tiles(unit_position) if
                       position in gamestate.units[1] and hasattr(gamestate.units[1][position], "melee_freeze"))

    def can_attack_with_unit(unit):
        return not (gamestate.get_actions_remaining() == 1 and hasattr(unit, "double_attack_cost")) \
            and not unit.is_attack_frozen()

    if getattr(gamestate, "extra_action"):
        return get_extra_actions(gamestate)

    actions = []

    for position, unit in gamestate.player_units().items():
        if can_use_unit(unit):

            friendly_units = find_all_friendly_units_except_current(position, gamestate.player_units())

            moves, attacks, abilities = get_unit_actions(unit, position, friendly_units, gamestate.opponent_units(),
                                                         gamestate.player_units())

            if can_attack_with_unit(unit) and moving_allowed(position):
                actions += moves + attacks + abilities

            if not can_attack_with_unit(unit) and moving_allowed(position):
                actions += moves + abilities

            if can_attack_with_unit(unit) and not moving_allowed(position):
                return attacks + abilities

    for action in actions:
        add_unit_references(gamestate, action)
        action.action_number = gamestate.action_number + 1

    return actions


def get_action(gamestate, action_document):
    start_position = position_to_tuple(action_document["start_position"])
    if not start_position in gamestate.player_units():
        return None

    attack_position = position_to_tuple(action_document["attack_position"])
    if attack_position and not attack_position in gamestate.opponent_units():
        return None

    action = Action(
        start_position,
        position_to_tuple(action_document["end_position"]),
        attack_position,
        position_to_tuple(action_document["ability_position"]),
        action_document["move_with_attack"],
        action_document["ability"])
    add_unit_references(gamestate, action)

    return action


def add_unit_references(gamestate, action):
    action.unit_reference = gamestate.player_units()[action.start_position]
    add_target_reference(action, gamestate.opponent_units(), gamestate.player_units())
    for sub_action in action.sub_actions:
        sub_action.unit_reference = gamestate.player_units()[action.start_position]


def get_extra_actions(gamestate):

    def get_actions_swiftness():
        moveset = generate_extra_moveset(unit, position, units)
        moves = move_actions(position, moveset | {position})

        return moves, [], []

    def get_actions_samurai():
        def melee_attacks_list_samurai_second(unit, start_position, moveset, enemy_units, movement_remaining):
            attacks = []
            for position, new_position, move_with_attack in attack_generator(unit, moveset | {start_position},
                                                                             enemy_units):
                if move_with_attack == 1:
                    if movement_remaining > 0:
                        attacks.append(Action(start_position, end_position=position, attack_position=new_position,
                                              move_with_attack=MoveOrStay.MOVE))
                else:
                    attacks.append(Action(start_position, end_position=position, attack_position=new_position,
                                          move_with_attack=MoveOrStay.STAY))
            return attacks

        attacks = melee_attacks_list_samurai_second(unit, position, {position}, gamestate.opponent_units(),
                                                    unit.get_movement_remaining())

        moveset = generate_extra_moveset(unit, position, units)
        moves = move_actions(position, moveset)

        return moves, attacks, []

    extra_actions = []

    for position, unit in gamestate.player_units().items():
        if unit.has_extra_action():
            friendly_units = find_all_friendly_units_except_current(position, gamestate.player_units())
            units = dict(friendly_units.items() + gamestate.opponent_units().items())

            opponent_units = gamestate.opponent_units()
            unit.zoc_blocks = frozenset(position for position,
                                        opponent_unit in opponent_units.items() if unit.type in opponent_unit.get_zoc())

            if unit.is_swift():
                moves, attacks, abilities = get_actions_swiftness()
            elif unit.is_samurai():
                moves, attacks, abilities = get_actions_samurai()
            else:
                moves, attacks, abilities = [], [], []

            extra_actions = moves + attacks + abilities

    for action in extra_actions:
        action.unit_reference = gamestate.player_units()[action.start_position]
        add_target_reference(action, gamestate.opponent_units(), gamestate.player_units())

    return extra_actions


def get_unit_actions(unit, position, friendly_units, enemy_units, player_units):

    unit.zoc_blocks = frozenset(position for position, enemy_unit in enemy_units.items()
                                if unit.type in enemy_unit.get_zoc())

    movement = unit.movement
    if any(position for position in surrounding_tiles(position) if position in friendly_units
           if hasattr(friendly_units[position], "cavalry_charging")):
        movement += 1

    units = merge_units(friendly_units, enemy_units)

    if unit.name not in settings.allowed_special_units:
        if unit.range == 1:
            moves, attacks = melee_actions(unit, position, units, enemy_units, movement)
            return moves, attacks, []
        else:
            moves, attacks = ranged_actions(unit, position, units, enemy_units)
            return moves, attacks, []

    else:
        return get_special_unit_actions(unit, position, units, enemy_units, player_units, movement)


def generate_extra_moveset(unit, position, units):
    return moves_set(position, frozenset(units), unit.zoc_blocks, unit.get_movement_remaining(),
                     unit.get_movement_remaining())


def generate_moveset(unit, position, units):
    return moves_set(position, frozenset(units), unit.zoc_blocks, unit.movement, unit.movement)


def generate_movesets(unit, position, units, movement):
    return moves_sets(position, frozenset(units), unit.zoc_blocks, movement, movement)


def zoc_block(position, direction, zoc_blocks):
    """ Returns whether an enemy unit exerting ZOC prevents you from going in 'direction' from 'position'. """
    return any(perpendicular_position in zoc_blocks for perpendicular_position in direction.perpendicular(position))


def adjacent_tiles_the_unit_can_move_to(position, units, zoc_blocks):
    for direction in directions:
        new_position = direction.move(position)
        if new_position in board and new_position not in units:
            if not zoc_block(position, direction, zoc_blocks):
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

    if movement_remaining != total_movement:
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
    """Returns all the tiles a unit can move to, in one set. """

    if movement_remaining == 0:
        return {position}

    if movement_remaining != total_movement:
        moveset = {position}
    else:
        moveset = set()

    for new_position in adjacent_tiles_the_unit_can_move_to(position, units, zoc_blocks):
        moveset |= moves_set(new_position, units, zoc_blocks, total_movement, movement_remaining - 1)

    return moveset


@memoized
def ranged_attacks_set(position, enemy_units, range_remaining):
    """ Returns all the tiles a ranged unit can attack, in a set."""

    attackset = set()

    if position in enemy_units:
        attackset.add(position)

    if range_remaining > 0:
        for new_position in adjacent_tiles(position):
            attackset |= ranged_attacks_set(new_position, enemy_units, range_remaining - 1)

    return attackset


def abilities_set(unit, position, units, possible_targets, range_remaining):
    """ Returns all the tiles an ability unit can target, in a set."""

    abilityset = set()

    if position in possible_targets:
        abilityset.add(position)

    if range_remaining > 0:
        for new_position in adjacent_tiles(position):
            abilityset |= abilities_set(unit, new_position, units, possible_targets, range_remaining - 1)

    return abilityset


def move_actions(start_position, moveset):
    return [Action(start_position, end_position=position) for position in moveset]


def ranged_attack_actions(start_position, attackset):
    return [Action(start_position, attack_position=position, move_with_attack=MoveOrStay.STAY)
            for position in attackset]


def attack_generator(unit, moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to. """
    for position in moveset:
        for direction in directions:
            new_position = direction.move(position)
            if new_position in enemy_units:
                if not zoc_block(position, direction, unit.zoc_blocks):
                    yield position, new_position, MoveOrStay.MOVE
                yield position, new_position, MoveOrStay.STAY


def attack_generator_no_zoc_check(moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to, without accounting for ZOC """
    for position in moveset:
        for direction in directions:
            new_position = direction.move(position)
            if new_position in enemy_units:
                yield position, new_position


def melee_attack_actions(unit, start_position, moveset, enemy_units):
    return [Action(start_position, end_position=end_position, attack_position=attack_position,
                   move_with_attack=move_with_attack) for end_position, attack_position,
            move_with_attack in attack_generator(unit, moveset, enemy_units)]


def melee_actions(unit, position, units, enemy_units, movement):

    moveset_with_leftover, moveset_no_leftover = generate_movesets(unit, position, units, movement)
    attacks = melee_attack_actions(unit, position, moveset_with_leftover | {position}, enemy_units)
    moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

    return moves, attacks


def ranged_actions(unit, position, units, enemy_units):
    attackset = ranged_attacks_set(position, frozenset(enemy_units), unit.range)
    moveset = generate_moveset(unit, position, units)
    attacks = ranged_attack_actions(position, attackset)
    moves = move_actions(position, moveset)

    return moves, attacks


def ability_actions(start_position, abilityset, ability):
    return [Action(start_position, ability_position=position, ability=ability) for position in abilityset]


def get_special_unit_actions(unit, position, units, enemy_units, player_units, movement):

    def melee_units(unit, position, units, enemy_units, movement):

        def rage(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):

            attacks = []
            for end_position, attack_position, move_with_attack in attack_generator(unit,
                                                                                    moveset_with_leftover | {position},
                                                                                    enemy_units):
                attacks.append(Action(position, end_position=end_position, attack_position=attack_position,
                                      move_with_attack=move_with_attack))
            for end_position, attack_position in attack_generator_no_zoc_check(moveset_no_leftover, enemy_units):
                attacks.append(Action(position, end_position=end_position, attack_position=attack_position,
                                      move_with_attack=MoveOrStay.STAY))

            moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def berserking(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):

            moveset_with_leftover_berserk, moveset_no_leftover_berserk = moves_sets(position, frozenset(units),
                                                                                    unit.zoc_blocks, 4, 4)

            attacks = melee_attack_actions(unit, position, moveset_with_leftover_berserk | {position}, enemy_units)

            moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def longsword(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):

            def get_attack(position, end_position, attack_position, move_with_attack):
                attack = Action(position, end_position=end_position, attack_position=attack_position,
                                move_with_attack=move_with_attack)
                for forward_position in four_forward_tiles(end_position, attack_position):
                    if forward_position in enemy_units:
                        attack.sub_actions.append(Action(position, end_position=end_position,
                                                         attack_position=forward_position, move_with_attack=MoveOrStay.STAY))
                return attack

            attacks = [get_attack(position, end_position, attack_position, move_with_attack) for end_position,
                       attack_position,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | {position}, enemy_units)]

            moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def triple_attack(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):

            def get_attack(start_position, end_position, attack_position, move_with_attack):
                attack = Action(start_position, end_position=end_position, attack_position=attack_position,
                                move_with_attack=move_with_attack)
                for forward_position in two_forward_tiles(end_position, attack_position):
                    if forward_position in enemy_units:
                        attack.sub_actions.append(Action(start_position, end_position=end_position,
                                                         attack_position=forward_position, move_with_attack=MoveOrStay.STAY))
                return attack

            attacks = [get_attack(position, end_position, attack_position, move_with_attack) for end_position,
                       attack_position,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | {position}, enemy_units)]

            moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def defence_maneuverability(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):
            extended_moveset_no_leftover = set()
            for move_position in moveset_no_leftover:
                extended_moveset_no_leftover.add(move_position)
                for direction in directions[2:]:
                    new_position = direction.move(move_position)
                    if new_position in board and new_position not in units:
                        extended_moveset_no_leftover.add(new_position)

            attacks = melee_attack_actions(unit, position, moveset_with_leftover | {position}, enemy_units)
            moves = move_actions(position, moveset_with_leftover | extended_moveset_no_leftover)

            return moves, attacks

        # Calculate this on the fly instead
        #def get_attacks_push(attacks):
        #    for attack in attacks:
        #        push_direction = get_direction(attack.end_position, attack.attack_position)
        #        for sub_attack in attack.sub_actions:
        #            sub_attack.push = True
        #            sub_attack.push_direction = push_direction
        #        attack.push = True
        #        attack.push_direction = push_direction
        #
        #    return attacks

        moveset_with_leftover, moveset_no_leftover = generate_movesets(unit, position, units, movement)
        attacks = melee_attack_actions(unit, position, moveset_with_leftover | {position}, enemy_units)
        moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

        for attribute in ["rage", "berserking", "longsword", "triple_attack", "defence_maneuverability"]:
            if hasattr(unit, attribute):
                moves, attacks = locals()[attribute](unit, position, moveset_with_leftover, moveset_no_leftover,
                                                     enemy_units)

        #if hasattr(unit, "push"):
        #    attacks = get_attacks_push(attacks)

        return moves, attacks

    def ranged_units(unit, position, units, enemy_units):
        return ranged_actions(unit, position, units, enemy_units)

    def ability_units(unit, position, enemy_units, player_units):

        abilities = []

        for ability in unit.abilities:

            if ability in ["sabotage", "poison"]:
                possible_targets = enemy_units

            elif ability in ["improve_weapons", "improve_weapons_II_A", "improve_weapons_II_B"]:
                possible_targets = [target_position for target_position, target_unit in player_units.items()
                                    if target_unit.attack and target_unit.range == 1]

            elif ability == "bribe":
                possible_targets = [target_position for target_position, target_unit in enemy_units.items()
                                    if not target_unit.get_bribed() and not target_unit.get_recently_bribed()]
            else:
                possible_targets = []

            abilityset = ranged_attacks_set(position, frozenset(possible_targets), unit.range)
            abilities += ability_actions(position, abilityset, ability)

        return abilities

    def no_attack_units(unit, position, units, enemy_units):

        def scouting():
            moveset = moves_set(position, frozenset(units), frozenset([]), unit.movement, unit.movement)
            return move_actions(position, moveset)

        moveset = generate_moveset(unit, position, units)
        moves = move_actions(position, moveset)

        for attribute in ["scouting"]:
            if hasattr(unit, attribute):
                moves = locals()[attribute]()

        return moves

    if unit.abilities:
        abilities = ability_units(unit, position, enemy_units, player_units)
    else:
        abilities = []

    if unit.attack:
        if unit.range == 1:
            moves, attacks = melee_units(unit, position, units, enemy_units, movement)
        else:
            moves, attacks = ranged_units(unit, position, units, enemy_units)

    else:
        moves = no_attack_units(unit, position, units, enemy_units)
        attacks = []

    return moves, attacks, abilities
