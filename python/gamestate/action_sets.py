from functools import lru_cache
from gamestate.gamestate_library import adjacent_tiles_the_unit_can_move_to


@lru_cache(maxsize=None)
def moves_sets(position, units, zoc_blocks, total_movement, movement_remaining):
    """
    Returns all the tiles a unit can move to, in two sets:
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
