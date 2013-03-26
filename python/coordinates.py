class Coordinates(object):
    def __init__(self, coordinates, interface):
        self.add_x = coordinates[0]
        self.add_y = coordinates[1]
        self.unit_width = interface.unit_width
        self.unit_padding_width = interface.unit_padding_width
        self.unit_height = interface.unit_height
        self.unit_padding_height = interface.unit_padding_height
        self.x_border = interface.x_border
        self.y_border_top = interface.y_border_top
        self.y_border_bottom = interface.y_border_bottom

    def get(self, position):
        if position[1] >= 5:
            y_border = self.y_border_top
        else:
            y_border = self.y_border_bottom

        x = int((position[0] - 1) * (self.unit_width + self.unit_padding_width) + self.x_border +
                self.add_x)
        y = int((8 - position[1]) * (self.unit_height + self.unit_padding_height) + y_border + self.add_y)

        return x, y
