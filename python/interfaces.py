import colors
import pygame
from coordinates import Coordinates


class Interface(object):

    def __init__(self, zoom):

        font_name = "arial"
        self.fonts = {"message": pygame.font.SysFont(font_name, int(18 * zoom), bold=True),
                      "small": pygame.font.SysFont(font_name, int(14 * zoom), bold=True),
                      "normal": pygame.font.SysFont(font_name, int(18 * zoom), bold=True),
                      "xp": pygame.font.SysFont(font_name, int(18 * zoom), bold=True),
                      "big": pygame.font.SysFont(font_name, int(36 * zoom), bold=True)
                      }

        self.line_distances = {"small": 15 * zoom}

        self.coordinates = {"base": Coordinates(self.base_coordinates, self),
                            "center": Coordinates(self.center_coordinates, self),
                            "battle": Coordinates(self.battle_coordinates, self),
                            "flag": Coordinates(self.first_symbol_coordinates, self),
                            "percentage": Coordinates(self.percentage_coordinates, self),
                            "percentage_sub": Coordinates(self.percentage_sub_coordinates, self)
                            }


class Rectangles(Interface):

    move_attack_icon = "./other/attack.gif"
    attack_icon = "./other/attack.gif"
    star_icon = "./other/star.gif"
    ability_icon = "./other/ability.gif"
    crusading_icon = "./other/flag.gif"
    high_morale_icon = "./other/flag_black.gif"
    move_icon = "./other/move.gif"
    dice = [""]
    for i in range(1, 7):
        dice.append("./other/dice_" + str(i) + ".png")
    base_coordinates = (0, 0)

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
        self.battle_coordinates = (self.unit_width / 2 - 15 * zoom, self.unit_height / 2 - 15 * zoom)

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

        self.message_location = (410 * zoom, 420 * zoom)
        self.message_font_size = int(23 * zoom)

        self.show_unit_coordinates = (450 * zoom, 20 * zoom)
        self.right_side_rectangle = (391 * self.zoom, 0, 391 * self.zoom, 743 * self.zoom)

        self.lower_right_rectangle = (391 * self.zoom, 391 * self.zoom, 391 * self.zoom, 391 * self.zoom)

        self.move_shading = pygame.Color(0, 0, 0, 160)
        self.attack_shading = pygame.Color(130, 0, 0, 150)
        self.ability_shading = pygame.Color(0, 0, 150, 130)
        self.selected_shading = pygame.Color(0, 0, 0, 160)

        self.counter_size = int(7 * zoom)

        self.message_line_length = 40 * zoom

        self.show_unit_location = (410 * zoom, 300 * zoom)

        self.upgrade_locations = [(410 * zoom, 370 * zoom), (600 * zoom, 370 * zoom)]

        self.upgrade_text_locations = [(410 * zoom, 510 * zoom), (600 * zoom, 510 * zoom)]

        self.small_line_distance = 15 * zoom

        pygame.init()

        super(Rectangles, self).__init__(zoom)
