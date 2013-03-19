from __future__ import division
import settings
from action import Action
import collections
import functools


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

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)


class Direction:
    """ An object direction is one move up, down, left or right.
    The class contains methods for returning the tile going one step in the direction will lead you to,
    and for returning the tiles you should check for zone of control.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, position):
        return position[0] + self. x, position[1] + self.y

    def perpendicular(self, position):
        return (position[0] + self.y, position[1] + self.x), (position[0] - self.y, position[1] - self.x)

    def __repr__(self):

        if self.x == -1:
            return "Left"

        if self.x == 1:
            return "Right"

        if self.y == -1:
            return "Down"

        if self.y == 1:
            return "Up"


#global variables
_action = 0
board = set((column, row) for column in range(1, 6) for row in range(1, 9))
directions = [Direction(0, -1), Direction(0, +1), Direction(-1, 0), Direction(1, 0)]
eight_directions = [Direction(i, j) for i in[-1, 0, 1] for j in [-1, 0, 1] if not i == j == 0]


def surrounding_tiles(position):
    """ Returns the 8 surrounding tiles"""
    return set(direction.move(position) for direction in eight_directions)


def four_forward_tiles(position, forward_position):
    """ Returns the 4 other nearby tiles in the direction towards forward_position """
    return surrounding_tiles(position) & surrounding_tiles(forward_position)


def two_forward_tiles(position, forward_position):
    """ Returns the 2 other nearby tiles in the direction towards forward_position """
    return set(direction.move(position) for direction in eight_directions) & \
        set(direction.move(forward_position) for direction in directions)


def get_direction(position, forward_position):
    """ Returns the direction that would take you from position to forward_position """
    return Direction(-position[0] + forward_position[0], -position[1] + forward_position[1])


def distance(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def find_all_friendly_units_except_current(current_unit_position, player_units):
    return dict((position, player_units[position]) for position in player_units if position != current_unit_position)


def add_target_reference(action, enemy_units, player_units):
    if action.is_attack:
        action.target_reference = enemy_units[action.attack_position]
    elif action.is_ability:
        if action.attack_position in enemy_units:
            action.target_reference = enemy_units[action.attack_position]
        elif action.attack_position in player_units:
            action.target_reference = player_units[action.attack_position]

    for sub_action in action.sub_actions:
        add_target_reference(sub_action, enemy_units, player_units)


def add_modifiers(attacks, player_units):
    def flag_bearing_bonus():
        for attack in attacks:
            if player_units[attack.start_position].range == 1:
                friendly_units = find_all_friendly_units_except_current(attack.start_position, player_units)
                for direction in directions:
                    adjacent_position = direction.move(attack.end_position)
                    if adjacent_position in friendly_units and hasattr(friendly_units[adjacent_position], "flag_bearing"):
                        attack.high_morale = True

    for modifier in [flag_bearing_bonus]:
        modifier()


def get_actions(gamestate):

    def can_use_unit(unit):
        return not (unit.used or hasattr(unit, "frozen") or hasattr(unit, "just_bribed"))

    def can_attack_with_unit(unit):
        return not (gamestate.get_actions_remaining() == 1 and hasattr(unit, "double_attack_cost")) \
            and not hasattr(unit, "attack_frozen")

    if hasattr(gamestate.current_player(), "extra_action"):
        return get_extra_actions(gamestate)

    actions = []

    if gamestate.get_actions_remaining() == 0:
        return actions

    for position, unit in gamestate.player_units().items():
        if can_use_unit(unit):

            friendly_units = find_all_friendly_units_except_current(position, gamestate.player_units())
            units = dict(friendly_units.items() + gamestate.opponent_units().items())

            moves, attacks, abilities = get_unit_actions(unit,
                                                         position,
                                                         units,
                                                         gamestate.opponent_units(),
                                                         gamestate.player_units())

            add_modifiers(attacks, gamestate.player_units())

            if can_attack_with_unit(unit):
                actions += moves + attacks + abilities
            else:
                actions += moves + abilities

    for action in actions:
        action.unit_reference = gamestate.player_units()[action.start_position]
        add_target_reference(action, gamestate.opponent_units(), gamestate.player_units())

    return actions


def get_extra_actions(gamestate):

    def charioting():
        moveset = generate_extra_moveset(unit, position, units)
        moves = move_actions(position, moveset | {position})

        return moves, [], []

    def samuraiing():
        def melee_attacks_list_samurai_second(unit, start_position, moveset, enemy_units, movement_remaining):
            attacks = []
            for position, new_position, move_with_attack in attack_generator(unit,
                                                                             moveset | {start_position},
                                                                             enemy_units):
                if not move_with_attack:
                    attacks.append(Action(start_position, position, new_position, True, False))
                else:
                    if movement_remaining > 0:
                        attacks.append(Action(start_position, position, new_position, True, True))
            return attacks

        attacks = melee_attacks_list_samurai_second(unit,
                                                    position,
                                                    {position},
                                                    gamestate.opponent_units(),
                                                    unit.movement_remaining)
        moves = move_actions(position, {position})

        return moves, attacks, []

    extra_actions = []

    for position, unit in gamestate.player_units().items():
        if hasattr(unit, "extra_action"):
            friendly_units = find_all_friendly_units_except_current(position, gamestate.player_units())
            units = dict(friendly_units.items() + gamestate.opponent_units().items())

            opponent_units = gamestate.opponent_units()
            unit.zoc_blocks = frozenset(position for position,
                                        opponent_unit in opponent_units.items() if unit.type in opponent_unit.zoc)

            moves, attacks, abilities = [], [], []

            for attribute in ["charioting", "samuraiing"]:
                if hasattr(unit, attribute):
                    moves, attacks, abilities = locals()[attribute]()

            add_modifiers(attacks, gamestate.player_units())
            extra_actions = moves + attacks + abilities

    for action in extra_actions:
        action.unit_reference = gamestate.player_units()[action.start_position]
        add_target_reference(action, gamestate.opponent_units(), gamestate.player_units())

    return extra_actions


def get_unit_actions(unit, position, units, enemy_units, player_units):

    unit.zoc_blocks = frozenset(position for position, enemy_unit in enemy_units.items() if unit.type in enemy_unit.zoc)

    if unit.name not in settings.special_units:
        if unit.range == 1:
            moves, attacks = melee_actions(unit, position, units, enemy_units)
            return moves, attacks, []
        else:
            moves, attacks = ranged_actions(unit, position, units, enemy_units)
            return moves, attacks, []

    else:
        return get_special_unit_actions(unit, position, units, enemy_units, player_units)


def generate_extra_moveset(unit, position, units):
    return moves_set(position, frozenset(units), unit.zoc_blocks, unit.movement_remaining, unit.movement_remaining)


def generate_moveset(unit, position, units):
    return moves_set(position, frozenset(units), unit.zoc_blocks, unit.movement, unit.movement)


def generate_movesets(unit, position, units):
    return moves_sets(position, frozenset(units), unit.zoc_blocks, unit.movement, unit.movement)


def zoc_block(position, direction, zoc_blocks):
    """ Returns whether an enemy unit exerting ZOC prevents you from going in 'direction' from 'position'. """
    return any(perpendicular_position in zoc_blocks for perpendicular_position in direction.perpendicular(position))


def adjacent_tiles_the_unit_can_move_to(position, units, zoc_blocks):
    for direction in directions:
        new_position = direction.move(position)
        if new_position in board and new_position not in units:
            if not zoc_block(position, direction, zoc_blocks):
                yield new_position


def adjacent_unoccupied_tiles(position, units):
    for direction in directions:
        new_position = direction.move(position)
        if new_position in board and new_position not in units:
            yield new_position


def adjacent_tiles(position):
    for direction in directions:
        new_position = direction.move(position)
        if new_position in board:
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
    return [Action(start_position, position, None, False, False) for position in moveset]


def ranged_attack_actions(start_position, attackset):
    return [Action(start_position, start_position, position, True, False) for position in attackset]


def attack_generator(unit, moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to. """
    for position in moveset:
        for direction in directions:
            new_position = direction.move(position)
            if new_position in enemy_units:
                if not zoc_block(position, direction, unit.zoc_blocks):
                    yield position, new_position, True
                yield position, new_position, False


def attack_generator_no_zoc_check(moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to, without accounting for ZOC """
    for position in moveset:
        for direction in directions:
            new_position = direction.move(position)
            if new_position in enemy_units:
                yield position, new_position


def melee_attack_actions(unit, start_position, moveset, enemy_units):
    return [Action(start_position, end_position, attack_position, True, move_with_attack) for end_position,
            attack_position,
            move_with_attack in attack_generator(unit, moveset, enemy_units)]


def melee_actions(unit, position, units, enemy_units):

    moveset_with_leftover, moveset_no_leftover = generate_movesets(unit, position, units)
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
    return [Action(start_position, start_position, position, False, False, True, ability) for position in abilityset]


def get_special_unit_actions(unit, position, units, enemy_units, player_units):

    def melee_units(unit, position, units, enemy_units):

        def rage(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):

            attacks = []
            for end_position, attack_position, move_with_attack in attack_generator(unit,
                                                                                    moveset_with_leftover | {position},
                                                                                    enemy_units):
                attacks.append(Action(position, end_position, attack_position, True, move_with_attack))
            for end_position, attack_position in attack_generator_no_zoc_check(moveset_no_leftover, enemy_units):
                attacks.append(Action(position, end_position, attack_position, True, False))

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
                attack = Action(position, end_position, attack_position, True, move_with_attack)
                for forward_position in four_forward_tiles(end_position, attack_position):
                    if forward_position in enemy_units:
                        attack.sub_actions.append(Action(position, end_position, forward_position, True, False))
                return attack

            attacks = [get_attack(position, end_position, attack_position, move_with_attack) for end_position,
                       attack_position,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | {position}, enemy_units)]

            moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def triple_attack(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):

            def get_attack(start_position, end_position, attack_position, move_with_attack):
                attack = Action(start_position, end_position, attack_position, True, move_with_attack)
                for forward_position in two_forward_tiles(end_position, attack_position):
                    if forward_position in enemy_units:
                        attack.sub_actions.append(Action(start_position, end_position, forward_position, True, False))
                return attack

            attacks = [get_attack(position, end_position, attack_position, move_with_attack) for end_position,
                       attack_position,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | {position}, enemy_units)]

            moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def lancing(unit, position, moveset_with_leftover, moveset_no_leftover, enemy_units):

            attacks = melee_attack_actions(unit, position, moveset_with_leftover | {position}, enemy_units)
            moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

            for attack in attacks:
                if distance(attack.start_position, attack.attack_position) >= 3:
                    attack.lancing = True

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

        def get_attacks_push(attacks):
            for attack in attacks:
                push_direction = get_direction(attack.end_position, attack.attack_position)
                for sub_attack in attack.sub_actions:
                    sub_attack.push = True
                    sub_attack.push_direction = push_direction
                attack.push = True
                attack.push_direction = push_direction

            return attacks

        moveset_with_leftover, moveset_no_leftover = generate_movesets(unit, position, units)
        attacks = melee_attack_actions(unit, position, moveset_with_leftover | {position}, enemy_units)
        moves = move_actions(position, moveset_with_leftover | moveset_no_leftover)

        for attribute in ["rage", "berserking", "longsword", "triple_attack", "defence_maneuverability", "lancing"]:
            if hasattr(unit, attribute):
                moves, attacks = locals()[attribute](unit,
                                                     position,
                                                     moveset_with_leftover,
                                                     moveset_no_leftover,
                                                     enemy_units)

        if hasattr(unit, "push"):
            attacks = get_attacks_push(attacks)

        return moves, attacks

    def ranged_units(unit, position, units, enemy_units):
        return ranged_actions(unit, position, units, enemy_units)

    def ability_units(unit, position, enemy_units, player_units):

        abilities = []

        for ability in unit.abilities:

            if ability in ["sabotage", "poison"]:
                possible_targets = enemy_units

            elif ability == "improve_weapons":
                possible_targets = [target_position for target_position, target_unit in player_units.items()
                                    if target_unit.attack and target_unit.range == 1]

            elif ability == "bribe":
                possible_targets = [target_position for target_position, target_unit in enemy_units.items()
                                    if not hasattr(target_unit, "bribed") and not hasattr(target_unit, "just_bribed")]
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
            moves, attacks = melee_units(unit, position, units, enemy_units)
        else:
            moves, attacks = ranged_units(unit, position, units, enemy_units)

    else:
        moves = no_attack_units(unit, position, units, enemy_units)
        attacks = []

    return moves, attacks, abilities
