import settings


class Coordinates(object):
    def __init__(self, coordinates):
        self.add_x = coordinates[0]
        self.add_y = coordinates[1]

    def get(self, position):
        if position[1] >= 5:
            y_border = settings.y_border_top
        else:
            y_border = settings.y_border_bottom

        x = int((position[0] - 1) * (settings.unit_width + settings.unit_padding_width) + settings.x_border + self.add_x)
        y = int((8 - position[1]) * (settings.unit_height + settings.unit_padding_height) + y_border + self.add_y)

        return x, y
