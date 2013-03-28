import colors


class Interface(object):

    base_coordinates = (0, 0)

    normal_font_name = "arial"
    normal_font_size = 18
    big_font_size = 28
    bigger_font_size = 38

    move_attack_icon = "./other/attack.gif"
    attack_icon = "./other/attack.gif"
    star_icon = "./other/star.gif"
    ability_icon = "./other/ability.gif"
    crusading_icon = "./other/flag.gif"
    high_morale_icon = "./other/flag_black.gif"
    move_icon = "./other/move.gif"


class Rectangles(Interface):
    def __init__(self, zoom):
        self.zoom = zoom

        self.board_image = "./rectangles/board.gif"
        self.unit_folder = "./rectangles/"

        self.unit_padding_width = 17 * zoom
        self.unit_padding_height = 15.13 * zoom
        self.unit_width = 53 * zoom
        self.unit_height = 72 * zoom
        self.board_size = [int(782 * zoom), int(743 * zoom)]
        self.x_border = 30 * zoom
        self.y_border_top = 26 * zoom
        self.y_border_bottom = 26 * zoom

        counter_base_x = 45 * zoom
        counter_base_y = 0 * zoom

        self.percentage_coordinates = (self.unit_width / 4, 0)
        self.percentage_sub_coordinates = (self.unit_width / 4, 0)
        self.center_coordinates = (self.unit_width / 2, self.unit_height / 2)
        self.symbol_coordinates = (self.unit_width / 2 - 15 * zoom, self.unit_height / 2 - 15 * zoom)

        self.first_symbol_coordinates = (2 * zoom, counter_base_y + 58 * zoom)
        self.second_symbol_coordinates = (18 * zoom, counter_base_y + 58 * zoom)

        self.first_counter_coordinates = (counter_base_x, counter_base_y + 58 * zoom)
        self.second_counter_coordinates = (counter_base_x, counter_base_y + 38 * zoom)
        self.third_counter_coordinates = (counter_base_x, counter_base_y + 18 * zoom)

        self.first_font_coordinates = (counter_base_x - 5 * zoom, counter_base_y + 48 * zoom)
        self.second_font_coordinates = (counter_base_x - 5 * zoom, counter_base_y + 28 * zoom)
        self.third_font_coordinates = (counter_base_x - 5 * zoom, counter_base_y + 8 * zoom)

        self.green_player_color = colors.gold
        self.red_player_color = colors.dull_red
        self.counter_circle_color = colors.black

        self.normal_font_size = int(self.normal_font_size * zoom)
        self.big_font_size = int(self.big_font_size * zoom)
        self.bigger_font_size = int(self.bigger_font_size * zoom)

        self.message_coordinates = (460 * zoom, 460 * zoom)
        self.show_unit_coordinates = (400 * zoom, 20 * zoom)
        self.right_side_rectangle = (391 * self.zoom, 0, 391 * self.zoom, 743 * self.zoom)
