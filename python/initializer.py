from __future__ import division
import common


class Direction:
    """ An object direction is one move up, down, left or right.
    The class contains methods for returning the tile going one step in the direction will lead you to,
    and for returning the tiles you should check for zone of control.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, position):
        return position.column + self. x, position.row + self.y

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


def zoc(unit, position, enemy_units):
    """ Returns whether an enemy unit can exert ZOC on a friendly unit """
    return position in enemy_units and unit.type in enemy_units[position].get_zoc()


def get_direction(position, forward_position):
    """ Returns the direction would take you from position to forward_position. """
    return Direction(-position[0] + forward_position[0], -position[1] + forward_position[1])


def distance(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def find_all_friendly_units_except_current(current_unit_position, p):
    return dict((position, p[0].units[position]) for position in p[0].units if position != current_unit_position)


def out_of_board_vertical(position):
    return position.row < 1 or position.row > 8


def out_of_board_horizontal(position):
    return position.column < 1 or position.column > 5


#global variables
_action = 0
board = set((column, row) for column in range(1, 6) for row in range(1, 9))
directions = [Direction(0, -1), Direction(0, +1), Direction(-1, 0), Direction(1, 0)]
eight_directions = [Direction(i, j) for i in[-1, 0, 1] for j in [-1, 0, 1] if not i == j == 0]


def initialize_action(gamestate):

    def initialize_crusader():
        for position, unit in gamestate.player_units().items():
            if any(surrounding_position in gamestate.player_units()
                   and hasattr(gamestate.player_units()[surrounding_position], "crusading") and unit.range == 1
                   for surrounding_position in common.surrounding_tiles(position)):
                unit.variables["is_crusading"] = True
            else:
                if hasattr(unit, "is_crusading"):
                    del unit.variables["is_crusading"]

    initialize_crusader()


def initialize_turn(gamestate):

    def resolve_bribe(unit, opponent_units, player_units):
        if unit.get_bribed():
            player_units[position] = opponent_units.pop(position)
            unit.set_recently_bribed()
            player_units[position].remove_bribed()

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units().items():
        unit.remove_used()
        unit.remove_xp_gained_this_turn()
        unit.decrement_frozen()
        unit.decrement_attack_frozen()
        unit.remove_sabotaged()
        unit.remove_sabotaged_II()
        unit.remove_improved_weapons()
        unit.decrease_improved_weapons_II_A()
        unit.remove_improved_weapons_II_B()
        unit.remove_recently_bribed()

    for opponent_unit_position, opponent_unit in gamestate.opponent_units().items():
        opponent_unit.variables["used"] = False
        resolve_bribe(opponent_unit, gamestate.opponent_units(), gamestate.player_units())
