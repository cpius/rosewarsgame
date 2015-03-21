from functools import lru_cache


def adjacent_tiles_the_unit_can_move_to(position, units, zoc_blocks):
    for direction, new_position in position.adjacent_moves().items():
        if new_position not in units and not zoc_block(position, direction, zoc_blocks):
            yield new_position


def zoc_block(position, direction, zoc_blocks):
    """ Returns whether an enemy unit exerting ZOC prevents you from going in 'direction' from 'position'. """
    return any(pos in zoc_blocks for pos in position.perpendicular(direction))


@lru_cache(maxsize=None)
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


@lru_cache(maxsize=None)
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


@lru_cache(maxsize=None)
def ranged_attacks_set(position, enemy_units, range_remaining):
    """ Returns all the tiles a ranged unit can attack"""

    attackset = set()

    if position in enemy_units:
        attackset.add(position)

    if range_remaining:
        for new_position in position.adjacent_tiles():
            attackset |= ranged_attacks_set(new_position, enemy_units, range_remaining - 1)

    return attackset
