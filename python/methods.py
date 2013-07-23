import json
from gamestate_module import Gamestate


def position_to_string(position):
    if position:
        columns = list(" ABCDE")
        return columns[position[0]] + str(position[1])


def position_to_tuple(position_string):
    if position_string:
        if len(position_string) != 2:
            return None

        column = ord(position_string[0]) - 64  # In ASCII A, B, C, D, E is 65, 66, 67, 68, 69
        row = int(position_string[1])
        return column, row


def merge_units(units1, units2):
    all_units = units1.copy()
    all_units.update(units2)
    return all_units


def load_gamestate_from_file(path):
    document = json.loads(open(path).read())
    return Gamestate.from_document(document)
