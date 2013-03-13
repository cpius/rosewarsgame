from __future__ import division


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


def zoc(unit, pos, enemy_units):
    """ Returns whether an enemy unit can exert ZOC on a friendly unit """
    return pos in enemy_units and unit.type in enemy_units[pos].zoc


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


def find_all_friendly_units_except_current(current_unit_position, p):
    return dict((pos, p[0].units[pos]) for pos in p[0].units if pos != current_unit_position)


def out_of_board_vertical(pos):
    return pos[1] < 1 or pos[1] > 8


def out_of_board_horizontal(pos):
    return pos[0] < 1 or pos[0] > 5



#global variables
_action = 0
board = set((i, j) for i in range(1, 6) for j in range(1, 9))
directions = [Direction(0, -1), Direction(0, +1), Direction(-1, 0), Direction(1, 0)]
eight_directions = [Direction(i, j) for i in[-1, 0, 1] for j in [-1, 0, 1] if not i == j == 0]


def initialize_action(player_units):

    def initialize_crusader():
        for pos, unit in player_units.items():
            if any(surrounding_pos in player_units and hasattr(player_units[surrounding_pos], "crusading") and
                   unit.range == 1 for surrounding_pos in surrounding_tiles(pos)):
                unit.is_crusading = True
            else:
                if hasattr(unit, "is_crusading"):
                    del unit.is_crusading

    initialize_crusader()

    return player_units


def initialize_turn(enemy_units, player_units, player):

    def initialize_abilities(unit):

        def frozen():
            if unit.frozen == 1:
                del unit.frozen
            else:
                unit.frozen -= 1

        def attack_frozen():
            if unit.attack_frozen == 1:
                del unit.attack_frozen
            else:
                unit.attack_frozen -= 1

        def sabotaged():
            del unit.sabotaged

        def improved_weapons():
            del unit.improved_weapons

        def just_bribed():
            del unit.just_bribed

        for attribute in ["frozen", "attack_frozen", "sabotaged", "improved_weapons", "just_bribed"]:
            if hasattr(unit, attribute):
                locals()[attribute]()

    def initialize_abilities_opponent(unit, enemy_units, player_units):
        if hasattr(unit, "bribed"):
            player_units[pos] = enemy_units.pop(pos)
            unit.just_bribed = True
            del player_units[pos].bribed

    player.actions_remaining = 2

    for pos, unit in player_units.items():
        unit.used = False
        unit.xp_gained_this_round = False
        initialize_abilities(unit)

    for pos, unit in enemy_units.items():
        unit.used = False
        initialize_abilities_opponent(unit, enemy_units, player_units)

    return enemy_units, player_units, player