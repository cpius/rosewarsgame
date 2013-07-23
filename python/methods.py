def convert_position_to_string(position):
    columns = list(" ABCDE")
    return columns[position[0]] + str(position[1])


def convert_position_to_tuple(position_string):
    if len(position_string) != 2:
        return None

    column = ord(position_string[0]) - 64  # In ASCII A, B, C, D, E is 65, 66, 67, 68, 69
    row = int(position_string[1])
    return column, row