import pygame
from view.coordinates import Coordinates
from collections import namedtuple


class Color:
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Green = (0, 255, 0)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
    Light_blue = (20, 70, 255)
    Brown = (128, 64, 0)
    Grey = (48, 48, 48)
    Yellow = (200, 200, 0)
    Light_grey = (240, 240, 240)
    Medium_grey = (150, 150, 150)
    Dark_grey = (60, 60, 60)
    Dark_green = (60, 113, 50)
    Dark_red = (204, 0, 16)
    Gold = (150, 130, 15)
    Dull_red = (190, 55, 55)
    Dodger_blue = (30, 144, 255)


class Interface(object):

    def __init__(self, zoom):

        self.fonts = {}

        self.line_distances = {"small": 15 * zoom,
                               "medium": 20 * zoom,
                               "normal": 25 * zoom,
                               "larger": 35 * zoom,
                               "big": 40 * zoom}

        self.coordinates = {"base": Coordinates(self.base_coordinates, self),
                            "base_box": Coordinates(self.base_box_coordinates, self),
                            "center": Coordinates(self.center_coordinates, self),
                            "battle": Coordinates(self.battle_coordinates, self),
                            "flag": Coordinates(self.first_symbol_coordinates, self),
                            "percentage": Coordinates(self.percentage_coordinates, self),
                            "percentage_sub": Coordinates(self.percentage_sub_coordinates, self),
                            "top_left": Coordinates(self.top_left_coordinates, self),
                            "bottom_left": Coordinates(self.bottom_left_coordinates, self)
                            }

    def load_fonts(self, zoom):
        font_name = "arial"
        self.fonts = {"message": pygame.font.SysFont(font_name, int(18 * zoom), bold=True),
                      "very_small": pygame.font.SysFont(font_name, int(11 * zoom), bold=True),
                      "small": pygame.font.SysFont(font_name, int(14 * zoom), bold=True),
                      "medium": pygame.font.SysFont(font_name, int(16 * zoom), bold=True),
                      "normal": pygame.font.SysFont(font_name, int(18 * zoom), bold=False),
                      "larger": pygame.font.SysFont(font_name, int(25 * zoom), bold=False),
                      "experience": pygame.font.SysFont(font_name, int(18 * zoom), bold=True),
                      "big": pygame.font.SysFont(font_name, int(36 * zoom), bold=True)
                      }


class Rectangles(Interface):

    move_attack_icon = "./graphics/attack.gif"
    attack_icon = "./graphics/attack.gif"
    star_icon = "./graphics/star.gif"
    ability_icon = "./graphics/ability.gif"
    crusading_icon = "./graphics/flag.gif"
    high_morale_icon = "./graphics/flag_black.gif"
    move_icon = "./graphics/move.gif"
    rank_icons = ["./graphics/level1.gif", "./graphics/level1.gif", "./graphics/level2.gif", "./graphics/level3.gif"]
    base_coordinates = (0, 0)

    def __init__(self, zoom):

        self.board_image = "./graphics/board.gif"
        self.unit_folder = "./graphics/units"

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

        self.unit_box_width = self.unit_width + 10 * zoom
        self.unit_box_height = self.unit_height + 10 * zoom

        self.percentage_coordinates = (self.unit_width / 4, 0)
        self.percentage_sub_coordinates = (self.unit_width / 4, 0)
        self.center_coordinates = (self.unit_width / 2, self.unit_height / 2)
        self.battle_coordinates = (self.unit_width / 2 - 15 * zoom, self.unit_height / 2 - 15 * zoom)

        self.base_box_coordinates = (-5 * zoom, -5 * zoom)

        self.first_symbol_coordinates = (2 * zoom, counter_base_y + 58 * zoom)
        self.second_symbol_coordinates = (18 * zoom, counter_base_y + 58 * zoom)

        self.top_left_coordinates = (-4 * zoom, -4 * zoom)
        self.bottom_left_coordinates = (-1 * zoom, 66 * zoom)

        self.first_counter_coordinates = (counter_base_x, counter_base_y + 58 * zoom)
        self.second_counter_coordinates = (counter_base_x, counter_base_y + 38 * zoom)
        self.third_counter_coordinates = (counter_base_x, counter_base_y + 18 * zoom)

        self.first_font_coordinates = (counter_base_x - 5 * zoom, counter_base_y + 48 * zoom)
        self.second_font_coordinates = (counter_base_x - 5 * zoom, counter_base_y + 28 * zoom)
        self.third_font_coordinates = (counter_base_x - 5 * zoom, counter_base_y + 8 * zoom)

        self.green_player_color = Color.Gold
        self.red_player_color = Color.Dull_red
        self.counter_circle_color = Color.Black

        self.message_location = (410 * zoom, 420 * zoom)
        self.message_font_size = int(23 * zoom)

        self.show_unit_coordinates = (450 * zoom, 20 * zoom)
        self.right_side_rectangle = (391 * zoom, 0, 391 * zoom, 743 * zoom)
        self.left_side_rectangle = (0, 0, 391 * zoom, 743 * zoom)

        self.lower_right_rectangle = (391 * zoom, 391 * zoom, 391 * zoom, 391 * zoom)

        self.shading = pygame.Color(30, 30, 30, 200)

        self.counter_size = int(7 * zoom)

        self.message_line_length = 40 * zoom

        self.show_unit_location = (410 * zoom, 25 * zoom)

        self.upgrade_locations = [(410 * zoom, 300 * zoom), (600 * zoom, 300 * zoom)]
        self.ask_about_ability_location = (410 * zoom, 230 * zoom)

        self.upgrade_text_locations = [(410 * zoom, 400 * zoom), (600 * zoom, 400 * zoom)]

        self.small_line_distance = 18 * zoom

        super(Rectangles, self).__init__(zoom)

        Point = namedtuple('Point', ['x', 'y'])
        self.upgrade_1_area = [Point(410 * zoom, 300 * zoom), Point((410 + 118) * zoom, (300 + 165.5) * zoom)]
        self.upgrade_2_area = [Point(600 * zoom, 300 * zoom), Point((600 + 118) * zoom, (300 + 165.5) * zoom)]

        self.help_area = [Point(735 * zoom, 715 * zoom), Point(780 * zoom, 740 * zoom)]

        self.to_help_menu_area = [Point(395 * zoom, 720 * zoom), Point(490 * zoom, 740 * zoom)]

        self.help_menu = [[Point(200 * zoom, (40 + 40 * i) * zoom), Point(310 * zoom, (70 + 40 * i) * zoom)]
                          for i in range(15)] + \
                         [[Point(500 * zoom, (40 + 40 * i) * zoom), Point(610 * zoom, (70 + 40 * i) * zoom)]
                          for i in range(15)]

        self.opponent_menu = [[Point(100 * zoom, (40 + 40 * i) * zoom), Point(510 * zoom, (70 + 40 * i) * zoom)]
                              for i in range(15)]

        self.pass_action_area = [Point(535 * zoom, 365 * zoom), Point(630 * zoom, 395 * zoom)]

        self.board = [Point(0, 0), Point(391 * zoom, 743 * zoom)]
