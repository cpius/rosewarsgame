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

    def move(self, pos):
        return pos[0] + self. x, pos[1] + self.y

    def perpendicular(self, pos):
        return (pos[0] + self.y, pos[1] + self.x), (pos[0] - self.y, pos[1] - self.x)

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
board = set((i, j) for i in range(1, 6) for j in range(1, 9))
directions = [Direction(0, -1), Direction(0, +1), Direction(-1, 0), Direction(1, 0)]
eight_directions = [Direction(i, j) for i in[-1, 0, 1] for j in [-1, 0, 1] if not i == j == 0]


def surrounding_tiles(pos):
    """ Returns the 8 surrounding tiles"""
    return set(direction.move(pos) for direction in eight_directions)


def four_forward_tiles(pos, forward_pos):
    """ Returns the 4 other nearby tiles in the direction towards forward_pos. """
    return surrounding_tiles(pos) & surrounding_tiles(forward_pos)


def two_forward_tiles(pos, forward_pos):
    """ Returns the 2 other nearby tiles in the direction towards forward_pos. """
    return set(direction.move(pos) for direction in eight_directions) & \
           set(direction.move(forward_pos) for direction in directions)


def get_direction(pos, forward_pos):
    """ Returns the direction would take you from pos to forward_pos. """
    return Direction(-pos[0] + forward_pos[0], -pos[1] + forward_pos[1])


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_all_friendly_units_except_current(current_unit_position, player_units):
    return dict((pos, player_units[pos]) for pos in player_units if pos != current_unit_position)


def add_target_ref(action, enemy_units, player_units):
    if action.is_attack:
        action.target_ref = enemy_units[action.attackpos]
    elif action.is_ability:
        if action.attackpos in enemy_units:
            action.target_ref = enemy_units[action.attackpos]
        elif action.attackpos in player_units:
            action.target_ref = player_units[action.attackpos]

    for sub_action in action.sub_actions:
        add_target_ref(sub_action, enemy_units, player_units)


def add_modifiers(attacks, player_units):
    def flag_bearing_bonus():
        for attack in attacks:
            if player_units[attack.startpos].range == 1:
                friendly_units = find_all_friendly_units_except_current(attack.startpos, player_units)
                for direction in directions:
                    adjacent_pos = direction.move(attack.endpos)
                    if adjacent_pos in friendly_units and hasattr(friendly_units[adjacent_pos], "flag_bearing"):
                        attack.high_morale = True

    for modifier in [flag_bearing_bonus]:
        modifier()


def get_actions(enemy_units, player_units, player):

    def can_use_unit(unit):
        return not (unit.used or hasattr(unit, "frozen") or hasattr(unit, "just_bribed"))

    def can_attack_with_unit(unit):
        return not (player.actions_remaining == 1 and hasattr(unit, "double_attack_cost")) \
            and not hasattr(unit, "attack_frozen")

    if hasattr(player, "extra_action"):
        return get_extra_actions(enemy_units, player_units, player)

    actions = []

    for pos, unit in player_units.items():
        if can_use_unit(unit):

            friendly_units = find_all_friendly_units_except_current(pos, player_units)
            units = dict(friendly_units.items() + enemy_units.items())

            moves, attacks, abilities = get_unit_actions(unit, pos, units, enemy_units, player_units)

            add_modifiers(attacks, player_units)

            if can_attack_with_unit(unit):
                actions += moves + attacks + abilities
            else:
                actions += moves + abilities

    for action in actions:
        action.unit_ref = player_units[action.startpos]
        add_target_ref(action, enemy_units, player_units)

    return actions


def get_unit_actions(unit, pos, units, enemy_units, player_units):

    unit.zoc_blocks = frozenset(pos for pos, enemy_unit in enemy_units.items() if unit.type in enemy_unit.zoc)

    if unit.name not in settings.special_units:
        if unit.range == 1:
            moves, attacks = melee_actions(unit, pos, units, enemy_units)
            return moves, attacks, []
        else:
            moves, attacks = ranged_actions(unit, pos, units, enemy_units)
            return moves, attacks, []

    else:
        return get_special_unit_actions(unit, pos, units, enemy_units, player_units)


def generate_moveset(unit, pos, units):
    return moves_set(pos, frozenset(units), unit.zoc_blocks, unit.movement, unit.movement)

def generate_movesets(unit, pos, units):
    return moves_sets(pos, frozenset(units), unit.zoc_blocks, unit.movement, unit.movement)


def get_extra_actions(enemy_units, player_units, player):

    def charioting():
        moveset = generate_moveset(unit, pos, units)
        moves = move_actions(pos, moveset | {pos})

        return moves, [], []

    def samuraiing():
        def melee_attacks_list_samurai_second(unit, startpos, moveset, enemy_units, movement_remaining):
            attacks = []
            for pos, newpos, move_with_attack in attack_generator(unit, moveset | {startpos}, enemy_units):
                if not move_with_attack:
                    attacks.append(Action(startpos, pos, newpos, True, False))
                else:
                    if movement_remaining > 0:
                        attacks.append(Action(startpos, pos, newpos, True, True))
            return attacks

        attacks = melee_attacks_list_samurai_second(unit, pos, {pos}, enemy_units, unit.movement_remaining)
        moves = move_actions(pos, {pos})

        return moves, attacks, []

    extra_actions = []

    for pos, unit in player_units.items():
        if hasattr(unit, "extra_action"):
            friendly_units, enemy_units = find_all_friendly_units_except_current(pos, player_units), enemy_units
            units = dict(friendly_units.items() + enemy_units.items())

            moveset = generate_moveset(unit, pos, units)

            for attribute in ["charioting", "samuraiing"]:
                if hasattr(unit, attribute):
                    moves, attacks, abilities = locals()[attribute]()

            add_modifiers(attacks, player_units)
            extra_actions = moves + attacks + abilities

    for action in extra_actions:
        action.unit_ref = player_units[action.startpos]
        add_target_ref(action, enemy_units, player_units)

    return extra_actions


def zoc_block(pos, direction, zoc_blocks):
    """ Returns whether an enemy unit exerting ZOC prevents you from going in 'direction' from 'pos'. """
    return any(perpendicular_pos in zoc_blocks for perpendicular_pos in direction.perpendicular(pos))


def adjacent_tiles_the_unit_can_move_to(pos, units, zoc_blocks):
    for direction in directions:
        newpos = direction.move(pos)
        if newpos in board and newpos not in units:
            if not zoc_block(pos, direction, zoc_blocks):
                yield newpos


def adjacent_unoccupied_tiles(pos, units):
    for direction in directions:
        newpos = direction.move(pos)
        if newpos in board and newpos not in units:
            yield newpos


def adjacent_tiles(pos):
    for direction in directions:
        newpos = direction.move(pos)
        if newpos in board:
            yield newpos

@memoized
def moves_sets(pos, units, zoc_blocks, total_movement, movement_remaining):
    """
    Returns all the tiles a unit can move to, in two sets.

    moveset_with_leftover: The tiles it can move to, and still have leftover movement to make an attack.
    moveset_no_leftover: The tiles it can move to, with no leftover movement to make an attack.
    """

    if movement_remaining == 0:
        return set(), {pos}

    if movement_remaining != total_movement:
        moveset_with_leftover = {pos}
    else:
        moveset_with_leftover = set()
    moveset_no_leftover = set()

    for newpos in adjacent_tiles_the_unit_can_move_to(pos, units, zoc_blocks):
        movesets = moves_sets(newpos, units, zoc_blocks, total_movement, movement_remaining -1)
        moveset_with_leftover |= movesets[0]
        moveset_no_leftover |= movesets[1]

    return moveset_with_leftover, moveset_no_leftover


def adjacent_tiles_the_unit_can_move_to_old(unit, pos, enemy_units, units):
    for direction in directions:
        newpos = direction.move(pos)
        if newpos in board and newpos not in units:
            if not zoc_block_old(unit, pos, direction, enemy_units):
                yield newpos


def zoc(unit, pos, enemy_units):
    """ Returns whether an enemy unit can exert ZOC on a friendly unit """
    return pos in enemy_units and unit.type in enemy_units[pos].zoc


def zoc_block_old(unit, pos, direction, enemy_units):
    """ Returns whether an enemy unit exerting ZOC prevents you from going in 'direction' from 'pos'. """
    return any(zoc(unit, perpendicular_pos, enemy_units) for perpendicular_pos in direction.perpendicular(pos))

@memoized
def moves_set(pos, units, zoc_blocks, total_movement, movement_remaining):
    """Returns all the tiles a unit can move to, in one set. """

    if movement_remaining == 0:
        return {pos}

    if movement_remaining != total_movement:
        moveset = {pos}
    else:
        moveset = set()

    for newpos in adjacent_tiles_the_unit_can_move_to(pos, units, zoc_blocks):
        moveset |= moves_set(newpos, units, zoc_blocks, total_movement, movement_remaining -1)

    return moveset

@memoized
def ranged_attacks_set(pos, enemy_units, range_remaining):
    """ Returns all the tiles a ranged unit can attack, in a set."""

    attackset = set()

    if pos in enemy_units:
        attackset.add(pos)

    if range_remaining > 0:
        for newpos in adjacent_tiles(pos):
            attackset |= ranged_attacks_set(newpos, enemy_units, range_remaining - 1)

    return attackset


def abilities_set(unit, pos, units, possible_targets, range_remaining):
    """ Returns all the tiles an ability unit can target, in a set."""

    abilityset = set()

    if pos in possible_targets:
        abilityset.add(pos)

    if range_remaining > 0:
        for newpos in adjacent_tiles(pos):
            abilityset |= abilities_set(unit, newpos, units, possible_targets, range_remaining - 1)

    return abilityset


def move_actions(startpos, moveset):
    return [Action(startpos, pos, None, False, False) for pos in moveset]


def ranged_attack_actions(startpos, attackset):
    return [Action(startpos, startpos, pos, True, False) for pos in attackset]


def attack_generator(unit, moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to. """
    for pos in moveset:
        for direction in directions:
            newpos = direction.move(pos)
            if newpos in enemy_units:
                if not zoc_block_old(unit, pos, direction, enemy_units):
                    yield pos, newpos, True
                yield pos, newpos, False


def attack_generator_no_zoc_check(moveset, enemy_units):
    """ Generates all the tiles a unit can attack based on the places it can move to, with no accounting for ZOC """
    for pos in moveset:
        for direction in directions:
            newpos = direction.move(pos)
            if newpos in enemy_units:
                yield pos, newpos


def melee_attack_actions(unit, startpos, moveset, enemy_units):
    return [Action(startpos, endpos, attackpos, True, move_with_attack) for endpos, attackpos,
            move_with_attack in attack_generator(unit, moveset, enemy_units)]


def melee_actions(unit, pos, units, enemy_units):

    moveset_with_leftover, moveset_no_leftover = generate_movesets(unit, pos, units)
    attacks = melee_attack_actions(unit, pos, moveset_with_leftover | {pos}, enemy_units)

    moves = move_actions(pos, moveset_with_leftover | moveset_no_leftover)

    return moves, attacks


def ranged_actions(unit, pos, units, enemy_units):
    attackset = ranged_attacks_set(pos, frozenset(enemy_units), unit.range)
    moveset = generate_moveset(unit, pos, units)
    attacks = ranged_attack_actions(pos, attackset)
    moves = move_actions(pos, moveset)

    return moves, attacks


def ability_actions(startpos, abilityset, ability):
    return [Action(startpos, startpos, pos, False, False, True, ability) for pos in abilityset]


def get_special_unit_actions(unit, pos, units, enemy_units, player_units):

    def melee_units(unit, pos, units, enemy_units):

        def rage(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):

            attacks = []
            for endpos, attackpos, move_with_attack in attack_generator(unit, moveset_with_leftover | {pos},
                                                                        enemy_units):
                attacks.append(Action(pos, endpos, attackpos, True, move_with_attack))
            for endpos, attackpos in attack_generator_no_zoc_check(moveset_no_leftover, enemy_units):
                attacks.append(Action(pos, endpos, attackpos, True, False))

            moves = move_actions(pos, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def berserking(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):

            moveset_with_leftover_berserk, moveset_no_leftover_berserk = moves_sets(pos, frozenset(units), unit.zoc_blocks, 5, 5)
            # Det burde vaere 4, men virker med 5. :S

            attacks = melee_attack_actions(unit, pos, moveset_with_leftover_berserk | {pos}, enemy_units)

            moves = move_actions(pos, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def longsword(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):

            def get_attack(pos, endpos, attackpos, move_with_attack):
                attack = Action(pos, endpos, attackpos, True, move_with_attack)
                for fpos in four_forward_tiles(endpos, attackpos):
                    if fpos in enemy_units:
                        attack.sub_actions.append(Action(pos, endpos, fpos, True, False))
                return attack

            attacks = [get_attack(pos, endpos, attackpos, move_with_attack) for endpos, attackpos,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | {pos}, enemy_units)]

            moves = move_actions(pos, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def triple_attack(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):

            def get_attack(startpos, endpos, attackpos, move_with_attack):
                attack = Action(startpos, endpos, attackpos, True, move_with_attack)
                for fpos in two_forward_tiles(endpos, attackpos):
                    if fpos in enemy_units:
                        attack.sub_actions.append(Action(startpos, endpos, fpos, True, False))
                return attack

            attacks = [get_attack(pos, endpos, attackpos, move_with_attack) for endpos, attackpos,
                       move_with_attack in attack_generator(unit, moveset_with_leftover | {pos}, enemy_units)]

            moves = move_actions(pos, moveset_with_leftover | moveset_no_leftover)

            return moves, attacks

        def lancing(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):

            attacks = melee_attack_actions(unit, pos, moveset_with_leftover | {pos}, enemy_units)
            moves = move_actions(pos, moveset_with_leftover | moveset_no_leftover)

            for attack in attacks:
                if distance(attack.startpos, attack.attackpos) >= 3:
                    attack.lancing = True

            return moves, attacks

        def defence_maneuverability(unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units):
            extended_moveset_no_leftover = set()
            for mpos in moveset_no_leftover:
                extended_moveset_no_leftover.add(mpos)
                for direction in directions[2:]:
                    newpos = direction.move(mpos)
                    if newpos in board and newpos not in units:
                        extended_moveset_no_leftover.add(newpos)

            attacks = melee_attack_actions(unit, pos, moveset_with_leftover | {pos}, enemy_units)
            moves = move_actions(pos, moveset_with_leftover | extended_moveset_no_leftover)

            return moves, attacks

        def get_attacks_push(attacks):
            for attack in attacks:
                push_direction = get_direction(attack.endpos, attack.attackpos)
                for sub_attack in attack.sub_actions:
                    sub_attack.push = True
                    sub_attack.push_direction = push_direction
                attack.push = True
                attack.push_direction = push_direction

            return attacks

        moveset_with_leftover, moveset_no_leftover = generate_movesets(unit, pos, units)
        attacks = melee_attack_actions(unit, pos, moveset_with_leftover | {pos}, enemy_units)
        moves = move_actions(pos, moveset_with_leftover | moveset_no_leftover)

        for attribute in ["rage", "berserking", "longsword", "triple_attack", "defence_maneuverability", "lancing"]:
            if hasattr(unit, attribute):
                moves, attacks = locals()[attribute](unit, pos, moveset_with_leftover, moveset_no_leftover, enemy_units)

        if hasattr(unit, "push"):
            attacks = get_attacks_push(attacks)

        return moves, attacks

    def ranged_units(unit, pos, units, enemy_units):
        return ranged_actions(unit, pos, units, enemy_units)

    def ability_units(unit, pos, units, enemy_units, player_units):

        abilities = []

        for ability in unit.abilities:

            if ability in ["sabotage", "poison"]:
                possible_targets = enemy_units

            elif ability == "improve_weapons":
                possible_targets = [tpos for tpos, target_unit in player_units.items()
                                    if target_unit.attack and target_unit.range == 1]

            elif ability == "bribe":
                possible_targets = [tpos for tpos, target_unit in enemy_units.items()
                                    if not hasattr(target_unit, "bribed") and not hasattr(target_unit, "just_bribed")]
            else:
                possible_targets = []

            abilityset = abilities_set(unit, pos, units, possible_targets, unit.range)
            abilities += ability_actions(pos, abilityset, ability)

        return abilities

    def no_attack_units(unit, pos, units, enemy_units):

        def scouting():

            def moves_set_scouting(unit, pos, units, enemy_units, movement_remaining):

                if movement_remaining > 0:
                    if movement_remaining != unit.movement:
                        moveset = {pos}
                    else:
                        moveset = set()

                    for newpos in adjacent_unoccupied_tiles(pos, units):
                        moveset |= moves_set_scouting(unit, newpos, units, enemy_units, movement_remaining - 1)

                    return moveset

                else:
                    return {pos}

            moveset = moves_set_scouting(unit, pos, units, enemy_units, unit.movement)
            moves = move_actions(pos, moveset)

            return moves

        moveset = generate_moveset(unit, pos, units)
        moves = move_actions(pos, moveset)

        for attribute in ["scouting"]:
            if hasattr(unit, attribute):
                moves = locals()[attribute]()

        return moves

    if unit.abilities:
        abilities = ability_units(unit, pos, units, enemy_units, player_units)
    else:
        abilities = []

    if unit.attack:
        if unit.range == 1:
            moves, attacks = melee_units(unit, pos, units, enemy_units)
        else:
            moves, attacks = ranged_units(unit, pos, units, enemy_units)

    else:
        moves = no_attack_units(unit, pos, units, enemy_units)
        attacks = []

    return moves, attacks, abilities

