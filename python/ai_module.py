import imp


class AI(object):
    """
    Creates an AI of a certain type, which can make the two decisions a player has to make in a game:
    - Make an action
    - Make a second part of an action (with Samurai or Chariot)
    - Put a counter on a unit with two experience points
    
    The locations are transformed so that the player the AI is playing for has backline on row 1.
    """

    def __init__(self, name):

        ai_type = imp.load_source(name, "ai_" + name.lower() + ".py")
        self.get_action = ai_type.get_action
        self.put_counter = ai_type.put_counter
        self.name = name

    def select_action(self, gamestate):

        gamestate = gamestate.copy()

        if gamestate.players[0].backline == 8:
            gamestate = get_transformed_gamestate(gamestate)
            transform_action = get_transformed_action
        else:
            transform_action = get_same_action

        actions = gamestate.get_actions()

        if actions:
            action = self.get_action(actions, gamestate)
            return transform_action(action)
        else:
            return None

    def add_counters(self, gamestate):

        self.put_counter(gamestate)


class Direction:
    """ A object direction is one move up, down, left or right.
    The class contains methods for returning the tile you will
    go to after the move, and for returning the tiles you should check for zone of control.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, position):
        return position[0] + self. x, position[1] + self.y

    def perpendicular(self, position):
        return (position[0] + self.y, position[1] + self.x), (position[0] - self.y, position[1] - self.x)


def transform_position(position):
    if position:
        return position[0], 9 - position[1]
    else:
        return None


def get_transformed_direction(direction):

    if direction.y == -1:
        return Direction(0, 1)

    if direction.y == 1:
        return Direction(0, -1)

    return direction


def get_transformed_action(action):

    action.start_position = transform_position(action.start_position)
    action.end_position = transform_position(action.end_position)
    action.attack_position = transform_position(action.attack_position)

    for sub_action in action.sub_actions:
        action.sub_action = get_transformed_action(sub_action)
    if hasattr(action, "push"):
        action.push_direction = get_transformed_direction(action.push_direction)

    return action


def get_same_action(action):

    return action


def get_transformed_gamestate(gamestate):

    new_units_players = []
    for units_player in gamestate.units:
        new_units = {}
        for position, unit in units_player.items():
            new_units[transform_position(position)] = unit

        new_units_players.append(new_units)

    gamestate.units = new_units_players

    for player in gamestate.players:
        player.backline = 9 - player.backline

    return gamestate
