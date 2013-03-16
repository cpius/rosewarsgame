from __future__ import division


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


def zoc(unit, position, enemy_units):
    """ Returns whether an enemy unit can exert ZOC on a friendly unit """
    return position in enemy_units and unit.type in enemy_units[position].zoc


def surrounding_tiles(position):
    """ Returns the 8 surrounding tiles"""
    return set(direction.move(position) for direction in eight_directions)


def four_forward_tiles(position, forward_position):
    """ Returns the 4 other nearby tiles in the direction towards forward_position. """
    return surrounding_tiles(position) & surrounding_tiles(forward_position)


def two_forward_tiles(position, forward_position):
    """ Returns the 2 other nearby tiles in the direction towards forward_position. """
    return set(direction.move(position) for direction in eight_directions) & \
           set(direction.move(forward_position) for direction in directions)


def get_direction(position, forward_position):
    """ Returns the direction would take you from position to forward_position. """
    return Direction(-position[0] + forward_position[0], -position[1] + forward_position[1])


def distance(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def find_all_friendly_units_except_current(current_unit_position, p):
    return dict((position, p[0].units[position]) for position in p[0].units if position != current_unit_position)


def out_of_board_vertical(position):
    return position[1] < 1 or position[1] > 8


def out_of_board_horizontal(position):
    return position[0] < 1 or position[0] > 5


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
                   for surrounding_position in surrounding_tiles(position)):
                unit.is_crusading = True
            else:
                if hasattr(unit, "is_crusading"):
                    del unit.is_crusading

    initialize_crusader()


def initialize_turn(gamestate):

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

    def resolve_bribe(unit, opponent_units, player_units):
        if hasattr(unit, "bribed"):
            player_units[position] = opponent_units.pop(position)
            unit.just_bribed = True
            del player_units[position].bribed

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units().items():
        unit.used = False
        unit.xp_gained_this_round = False
        initialize_abilities(unit)

    for opponent_unit_position, opponent_unit in gamestate.opponent_units().items():
        opponent_unit.used = False
        resolve_bribe(opponent_unit, gamestate.opponent_units(), gamestate.player_units())

    return gamestate.opponent_units(), gamestate.player_units(), gamestate.current_player()
