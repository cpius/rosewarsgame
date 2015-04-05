from view.view_display_library import get_image, pygame, Color, draw_rectangle, write, get_unit_pic
from view.coordinates import Coordinates
from view.rounded_rect import AAfilledRoundedRect
from gamestate.gamestate_library import *
import game.settings as settings


class Viewgame:

    def __init__(self, interface, screen):
        self.interface = interface
        self.screen = screen

    def draw_game(self, game, actions, shade_positions):
        self.screen.blit(get_image(self.interface.board_image), (0, 0))

        gamestate = game.gamestate.copy()
        if not game.is_player_human():
            gamestate.flip_all_units()

        self.draw_units(game)

        if not shade_positions:
            shade_positions = set()
        if actions:
            shade_positions |= self.get_shade_actions(actions)

        self.shade_tiles(shade_positions)

    def shade_tiles(self, shade_positions):
        unit_dimensions = (self.interface.unit_box_width, self.interface.unit_box_height)
        for position in shade_positions:
            location = self.interface.coordinates["base_box"].get(position)
            rectangle_style = (location[0], location[1], unit_dimensions[0], unit_dimensions[1])
            AAfilledRoundedRect(self.screen, rectangle_style, self.interface.shading, 0.2)

    def draw_units(self, game):
        for position, unit in game.gamestate.player_units.items():
            self.draw_unit(unit, position, game.current_player().color)

        for position, unit in game.gamestate.enemy_units.items():
            self.draw_unit(unit, position, game.opponent_player().color)

    @staticmethod
    def get_shade_actions(actions):
        shade_positions = set()
        for action in actions:
            if action.is_attack or action.is_ability:
                shade_positions.add(action.target_at)
            else:
                shade_positions.add(action.end_at)
        return shade_positions

    def draw_post_movement(self, action):
        pygame.draw.circle(self.screen, Color.Black, self.interface.coordinates["center"].get(action.end_at), 10)
        self.draw_line(action.end_at, action.target_at)
        pic = get_image(self.interface.move_icon)
        self.screen.blit(pic, self.interface.coordinates["battle"].get(action.target_at))

    def draw_action(self, action, flip=False):
        if flip:
            aligned_action = self.flip_action(action)
        else:
            aligned_action = action

        coordinates = self.interface.coordinates

        pygame.draw.circle(self.screen, Color.Black, coordinates["center"].get(aligned_action.start_at), 10)
        self.draw_line(aligned_action.start_at, aligned_action.end_at)

        if aligned_action.is_attack:
            self.draw_line(aligned_action.end_at, aligned_action.target_at)

            pic = get_image(self.interface.attack_icon)
            self.screen.blit(pic, coordinates["battle"].get(aligned_action.target_at))

        elif aligned_action.is_ability:
            self.draw_line(aligned_action.end_at, aligned_action.target_at)
            pic = get_image(self.interface.ability_icon)
            self.screen.blit(pic, coordinates["battle"].get(aligned_action.target_at))

        else:
            pic = get_image(self.interface.move_icon)
            self.screen.blit(pic, coordinates["battle"].get(aligned_action.end_at))

    def draw_line(self, start_position, end_position):
        start_coordinates = self.interface.coordinates["center"].get(start_position)
        end_coordinates = self.interface.coordinates["center"].get(end_position)
        pygame.draw.line(self.screen, Color.Black, start_coordinates, end_coordinates, 5)

    def shade_positions(self, positions, color=None):
        for position in positions:
            base = self.interface.coordinates["base"].get(position)
            dimensions = (self.interface.unit_width, self.interface.unit_height)
            if color:
                draw_rectangle(self.screen, dimensions, base, color)
            else:
                draw_rectangle(self.screen, dimensions, base, self.interface.shading)

    def draw_counters(self, counters, color, position, counter_coordinates, font_coordinates):
        self.draw_bordered_circle(counter_coordinates.get(position), self.interface.counter_size, color)

        if counters > 1:
            write(self.screen, str(counters), font_coordinates.get(position), self.interface.fonts["small"])

    def draw_bordered_circle(self, position, size, color):
        pygame.draw.circle(self.screen, Color.Black, position, size + 2)
        pygame.draw.circle(self.screen, color, position, size)

    def draw_symbols(self, unit, position):

        def find_base(index):
            base = self.interface.coordinates["bottom_left"].get(position)
            return base[0] + index * 4, base[1]

        def draw_box(index, color):
            base = find_base(index)
            width = 4
            height = 7
            corner1 = (base[0], base[1])
            corner2 = (base[0] + width, base[1])
            corner3 = (base[0] + width, base[1] + height)
            corner4 = (base[0], base[1] + height)
            base_corners = [corner1, corner2, corner3, corner4]
            pygame.draw.lines(self.screen, Color.Black, True, base_corners)
            draw_rectangle(self.screen, (3, 6), (base[0] + 1, base[1] + 1), color)

        total_boxes = unit.experience_to_upgrade
        blue_boxes = unit.get(State.experience) % unit.experience_to_upgrade
        for index in range(blue_boxes):
            draw_box(index, Color.Light_blue)

        for index in range(blue_boxes, total_boxes):
            draw_box(index, Color.White)

        if unit.has(Effect.bribed):
            self.draw_bribed(position)

        level = unit.unit_level
        if not unit.should_be_upgraded() and level:
            if level > 3:
                level = 3
            pic = get_image(self.interface.level_icons[level], (14, 14))
            self.screen.blit(pic, self.interface.coordinates["top_left"].get(position))

    def draw_bribed(self, position):
        pic = get_image(self.interface.ability_icon)
        self.screen.blit(pic, self.interface.coordinates["flag"].get(position))

    def draw_unit(self, unit, position, color, selected=False):
        unit_pic = get_unit_pic(self.interface, unit)
        counters_drawn = 0

        dimensions = (int(self.interface.unit_width), int(self.interface.unit_height))
        pic = get_image(unit_pic, dimensions)

        base_coordinates = Coordinates(self.interface.base_coordinates, self.interface)
        base = base_coordinates.get(position)

        self.draw_unit_box(self.screen, self.interface, base, color)

        self.screen.blit(pic, base)

        if self.get_blue_counters(unit):
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            counters = self.get_blue_counters(unit)
            self.draw_counters(counters, Color.Blue, position, counter_coordinates, font_coordinates)
            counters_drawn += 1
        if self.get_yellow_counters(unit):
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            counters = self.get_yellow_counters(unit)
            self.draw_counters(counters, Color.Yellow, position, counter_coordinates, font_coordinates)

        self.draw_symbols(unit, position)

    def draw_unit_box(self, screen, interface, base, color, resize=1):
        height = interface.unit_height * resize
        width = interface.unit_width * resize

        if color == "Red":
            border_color = interface.red_player_color
        else:
            border_color = interface.green_player_color

        thickness = int(5 * settings.zoom * resize)

        rectangle_style = [base[0], base[1], width, height]
        rectangle_style[0] -= thickness
        rectangle_style[1] -= thickness
        rectangle_style[2] += 2 * thickness
        rectangle_style[3] += 2 * thickness

        AAfilledRoundedRect(screen, rectangle_style, border_color, 0.2)

    def get_counter_coordinates(self, counters_drawn):
        return {
            0: Coordinates(self.interface.first_counter_coordinates, self.interface),
            1: Coordinates(self.interface.second_counter_coordinates, self.interface),
            2: Coordinates(self.interface.third_counter_coordinates, self.interface),
        }[counters_drawn]

    def get_font_coordinates(self, counters_drawn):
        return {
            0: Coordinates(self.interface.first_font_coordinates, self.interface),
            1: Coordinates(self.interface.second_font_coordinates, self.interface),
            2: Coordinates(self.interface.third_font_coordinates, self.interface),
        }[counters_drawn]

    @staticmethod
    def flip_action(action):
        flipped_action = action.copy()
        for attribute in ["start_at", "end_at", "target_at"]:
            if getattr(flipped_action, attribute):
                setattr(flipped_action, attribute, getattr(flipped_action, attribute).flip())
        return flipped_action

    @staticmethod
    def get_yellow_counters(unit):
        return 1 if (unit.has_extra_life or unit.has(Effect.improved_weapons)) else 0

    @staticmethod
    def get_blue_counters(unit):
        poisoned_level = unit.get(Effect.poisoned)
        frozen_level = unit.get(State.attack_frozen)
        bribed = unit.has(State.recently_bribed)

        return max(poisoned_level, frozen_level, bribed)

    def draw_ask_about_move_with_attack(self, end_at, target_at):
        dimensions = (self.interface.unit_width, self.interface.unit_height)

        base = self.interface.coordinates["base"].get(end_at)
        draw_rectangle(self.screen, dimensions, base, self.interface.shading)

        base = self.interface.coordinates["base"].get(target_at)
        draw_rectangle(self.screen, dimensions, base, self.interface.shading)
