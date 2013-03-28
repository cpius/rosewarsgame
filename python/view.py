import pygame
import settings
from coordinates import Coordinates
import battle
import colors
import textwrap

_anti_alias = 1
_image_library = {}


class Log():
    def __init__(self, action, turn, action_number, player_color):
        self.action = action
        self.turn = turn
        self.action_number = action_number
        self.player_color = player_color


class View(object):
    def __init__(self):
        pygame.init()

        self.interface = settings.interface
        self.zoom = self.interface.zoom
        self.message_location = self.interface.message_location

        self.screen = pygame.display.set_mode(self.interface.board_size)

        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)

        self.font = pygame.font.SysFont(self.interface.normal_font_name, self.interface.normal_font_size, True)
        self.font_messages = pygame.font.SysFont(self.interface.normal_font_name,
                                                 self.interface.message_font_size, True)
        self.font_big = pygame.font.SysFont(self.interface.normal_font_name, self.interface.big_font_size, True)
        self.font_bigger = pygame.font.SysFont(self.interface.normal_font_name, self.interface.bigger_font_size, True)
        self.base_coordinates = Coordinates(self.interface.base_coordinates, self.interface)
        self.percentage_coordinates = Coordinates(self.interface.percentage_coordinates, self.interface)
        self.percentage_sub_coordinates = Coordinates(self.interface.percentage_sub_coordinates, self.interface)
        self.center_coordinates = Coordinates(self.interface.center_coordinates, self.interface)
        self.symbol_coordinates = Coordinates(self.interface.symbol_coordinates, self.interface)

        self.logbook = []
        self.maximum_number_of_logs = 5

        self.message_line_distance = 30 * self.zoom
        self.counter_size = self.interface.counter_size

    def get_position_from_mouse_click(self, coordinates):
        x = int((coordinates[0] - self.interface.x_border) /
                (self.interface.unit_width + self.interface.unit_padding_width)) + 1
        if coordinates[1] > self.interface.board_size[1] / 2:
            y = 8 - int((coordinates[1] - self.interface.y_border_bottom) /
                        (self.interface.unit_height + self.interface.unit_padding_height))
        else:
            y = 8 - int((coordinates[1] - self.interface.y_border_top) /
                        (self.interface.unit_height + self.interface.unit_padding_height))
        return x, y

    def draw_ask_about_counter(self, unit_name):
        x = self.message_location[0]
        y = self.message_location[1]
        lines = ["Select counter for", unit_name, "'a' for attack", "'d' for defence"]
        for i, line in enumerate(lines):
            line_y = y + i * self.message_line_distance
            self.write_message(line, (x, line_y))
        pygame.display.update()

    def draw_ask_about_ability(self, unit):
        x, y = self.message_location
        lines = ["Select ability:"]
        for i, ability in enumerate(unit.abilities):
            string = str(i + 1) + ". " + ability.title() + ": " + unit.descriptions[ability]
            lines += textwrap.wrap(string, self.interface.message_line_length)

        for i, line in enumerate(lines):
            line_y = y + i * self.message_line_distance
            self.write_message(line, (x, line_y))

        pygame.display.update()

    def show_unit_zoomed(self, unit):
        unit_pic = self.get_unit_pic(unit.name)
        pic = self.get_image(unit_pic, (int(236 * self.zoom), int(271 * self.zoom)))
        self.screen.blit(pic, self.interface.show_unit_coordinates)

        pygame.display.flip()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, "./replay/" + name + ".jpeg")

    def draw_game_end(self, color):
        self.write(color + " Wins", self.message_location, self.font_big)
        pygame.display.update()

    def get_image(self, path, dimensions=None):
        global _image_library

        if dimensions:
            image = pygame.image.load(path).convert()
            return pygame.transform.scale(image, dimensions)

        image = _image_library.get(path)
        if not image:
            image = pygame.image.load(path).convert()
            image = pygame.transform.scale(image, (int(image.get_size()[0] * self.zoom),
                                                   int(image.get_size()[1] * self.zoom)))
            _image_library[path] = image
        return image

    def draw_counters(self, unit, position):
        counters_drawn = 0

        if unit.attack_counters:
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            self.draw_attack_counters(unit, position, counter_coordinates, font_coordinates)
            counters_drawn += 1
        if unit.defence_counters or hasattr(unit, "sabotaged"):
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            self.draw_defence_counters(unit, position, counter_coordinates, font_coordinates)
            counters_drawn += 1
        if unit.blue_counters:
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            font_coordinates = self.get_font_coordinates(counters_drawn)
            self.draw_blue_counters(unit, position, counter_coordinates, font_coordinates)
            counters_drawn += 1
        if unit.yellow_counters:
            counter_coordinates = self.get_counter_coordinates(counters_drawn)
            self.draw_yellow_counters(unit, position, counter_coordinates)

    def get_counter_coordinates(self, counters_drawn):
        return {
            0: Coordinates(self.interface.first_counter_coordinates, self.interface),
            1: Coordinates(self.interface.second_counter_coordinates, self.interface),
            2: Coordinates(self.interface.third_counter_coordinates, self.interface),
            3: Coordinates(self.interface.third_counter_coordinates, self.interface)
        }[counters_drawn]

    def get_font_coordinates(self, counters_drawn):
        return {
            0: Coordinates(self.interface.first_font_coordinates, self.interface),
            1: Coordinates(self.interface.second_font_coordinates, self.interface),
            2: Coordinates(self.interface.third_font_coordinates, self.interface),
            3: Coordinates(self.interface.third_counter_coordinates, self.interface)
        }[counters_drawn]

    def draw_attack_counters(self, unit, position, counter_coordinates, font_coordinates):
        self.draw_bordered_circle(counter_coordinates.get(position), self.counter_size, colors.brown)
        if unit.attack_counters != 1:
            self.write(str(unit.attack_counters), font_coordinates.get(position), self.font)

    def draw_defence_counters(self, unit, position, counter_coordinates, font_coordinates):
        if hasattr(unit, "sabotaged"):
            defence_counters = -1
        else:
            defence_counters = unit.defence_counters

        self.draw_bordered_circle(counter_coordinates.get(position), self.counter_size, colors.light_grey)

        if defence_counters > 1:
            counter_text = str(defence_counters)
        elif defence_counters < 0:
            counter_text = "x"
        else:
            counter_text = None

        if counter_text:
            self.write(counter_text, font_coordinates.get(position), self.font)

    def draw_yellow_counters(self, unit, position, counter_coordinates):
        if unit.yellow_counters:
            self.draw_bordered_circle(counter_coordinates.get(position), self.counter_size, colors.yellow)

    def draw_blue_counters(self, unit, position, counter_coordinates, font_coordinates):
        if unit.blue_counters:
            self.draw_bordered_circle(counter_coordinates.get(position), self.counter_size, colors.blue)

            if unit.blue_counters > 1:
                self.write(str(unit.blue_counters), font_coordinates.get(position), self.font)

    def draw_symbols(self, unit, position):
        coordinates = Coordinates(self.interface.first_symbol_coordinates, self.interface)
        if unit.xp == 1:
            self.draw_xp(position, coordinates)
            coordinates = Coordinates(self.interface.second_symbol_coordinates, self.interface)
        if hasattr(unit, "bribed"):
            self.draw_bribed(position, coordinates)
            coordinates = Coordinates(self.interface.second_symbol_coordinates, self.interface)
        if hasattr(unit, "is_crusading"):
            self.draw_crusading(position, coordinates)

    def draw_xp(self, position, coordinates):
        pic = self.get_image(self.interface.star_icon)
        self.screen.blit(pic, coordinates.get(position))

    def draw_bribed(self, position, coordinates):
        pic = self.get_image(self.interface.ability_icon)
        self.screen.blit(pic, coordinates.get(position))

    def draw_crusading(self, position, coordinates):
        pic = self.get_image(self.interface.crusading_icon)
        self.screen.blit(pic, coordinates.get(position))

    def draw_unit(self, unit, position, color, selected=False):
        unit_pic = self.get_unit_pic(unit.name)
        dimensions = (int(self.interface.unit_width), int(self.interface.unit_height))
        pic = self.get_image(unit_pic, dimensions)

        self.screen.blit(pic, self.base_coordinates.get(position))

        base = self.base_coordinates.get(position)

        if selected:
            dimensions = (self.interface.unit_width, self.interface.unit_height)
            self.draw_rectangle(dimensions, base, self.interface.selected_shading)

        self.draw_unit_box(base, color)

        self.draw_counters(unit, position)
        self.draw_symbols(unit, position)

    def draw_game(self, gamestate, start_position=None, actions=()):

        pic = self.get_image(self.interface.board_image)
        self.screen.blit(pic, (0, 0))

        for position, unit in gamestate.units[0].items():
            if actions and position == start_position:
                self.draw_unit(unit, position, gamestate.current_player().color, selected=True)
            else:
                self.draw_unit(unit, position, gamestate.current_player().color)

        for position, unit in gamestate.units[1].items():
            self.draw_unit(unit, position, gamestate.players[1].color)

        coordinates = Coordinates((0, 0), self.interface)

        attacks, moves, abilities = [], [], []
        for action in actions:
            if action.is_attack:
                attacks.append(action)
            elif action.is_ability:
                abilities.append(action)
            else:
                moves.append(action)

        unit_dimensions = (self.interface.unit_width, self.interface.unit_height)

        move_locations, attack_locations, ability_locations, sub_attack_locations = set(), set(), set(), set()

        for action in moves:
            location = coordinates.get(action.end_position)
            if location not in move_locations:
                move_locations.add(location)
                self.draw_rectangle(unit_dimensions, location, self.interface.move_shading)

        for action in attacks:
            location = coordinates.get(action.attack_position)
            if location not in attack_locations:
                attack_locations.add(location)
                self.draw_rectangle(unit_dimensions, location, self.interface.attack_shading)
                string = str(int(round(action.chance_of_win * 100))) + "%"
                location = self.percentage_coordinates.get(action.attack_position)
                self.write(string, location, self.font, colors.dodger_blue)

        for action in abilities:
            location = coordinates.get(action.attack_position)
            if location not in ability_locations:
                ability_locations.add(location)
                location = coordinates.get(action.attack_position)
                self.draw_rectangle(unit_dimensions, location, self.interface.ability_shading)

        for attack in attacks:
            for sub_attack in attack.sub_actions:
                location = coordinates.get(sub_attack.attack_position)
                if location not in sub_attack_locations and location not in attack_locations:
                    sub_attack_locations.add(location)
                    self.draw_rectangle(unit_dimensions, location, self.interface.attack_shading)
                    string = str(int(round(sub_attack.chance_of_win * 100))) + "%"
                    location = self.percentage_sub_coordinates.get(sub_attack.attack_position)
                    self.write(string, location, self.font, colors.yellow)

        self.draw_right()

        pygame.display.update()

    def draw_action(self, action, gamestate):

        log = Log(action, gamestate.turn, gamestate.get_actions_remaining(), gamestate.current_player().color)
        self.logbook.append(log)

        if len(self.logbook) > self.maximum_number_of_logs:
            self.logbook.pop(0)

        pygame.draw.circle(self.screen, colors.black, self.center_coordinates.get(action.start_position), 10)
        self.draw_line(action.start_position, action.end_position)

        if action.is_attack:
            self.draw_line(action.end_position, action.attack_position)

            if action.move_with_attack:
                pic = self.get_image(self.interface.move_attack_icon)
            else:
                pic = self.get_image(self.interface.attack_icon)

            if hasattr(action, "high_morale"):
                pic = self.get_image(self.interface.high_morale_icon)
                coordinates = Coordinates(self.interface.first_symbol_coordinates, self.interface)
                self.screen.blit(pic, coordinates.get(action.end_position))

            self.screen.blit(pic, self.symbol_coordinates.get(action.attack_position))

        elif action.is_ability:
            self.draw_line(action.end_position, action.attack_position)
            pic = self.get_image(self.interface.ability_icon)
            self.screen.blit(pic, self.symbol_coordinates.get(action.attack_position))

        else:
            pic = self.get_image(self.interface.move_icon)
            self.screen.blit(pic, self.symbol_coordinates.get(action.end_position))

        self.draw_log()

        pygame.display.update()

    def get_unit_pic(self, name):
        return "./" + self.interface.unit_folder + "/" + name.replace(" ", "_") + ".jpg"

    def refresh(self):
        pygame.display.flip()

    def draw_log(self):
        zoom = self.zoom
        log_heights = 64 * zoom

        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)

        for index, log in enumerate(self.logbook):

            action = log.action
            base_x = int(391 * zoom)
            base_y = int(index * log_heights)
            base = (base_x, base_y)

            self.draw_turn_box(log, *base)

            line_thickness = int(3 * zoom)
            line_start = (base_x, base_y + log_heights - line_thickness / 2)
            line_end = (int(self.interface.board_size[1] * self.zoom), base_y + log_heights - line_thickness / 2)
            pygame.draw.line(self.screen, colors.black, line_start, line_end, line_thickness)

            symbol_location = (base_x + 118 * zoom, base_y + 12 * zoom)

            if action.is_attack:
                self.draw_attack(action, base, symbol_location, log)

            elif action.is_ability:

                attacking_unit = action.unit_reference
                defending_unit = action.target_reference

                pic = self.get_image(self.interface.ability_icon)
                self.screen.blit(pic, symbol_location)

                if log.player_color == "Green":
                    self.draw_unit_right(attacking_unit.name, "Green", 0, *base)
                    self.draw_unit_right(defending_unit.name, "Red", 1, *base)
                elif log.player_color == "Red":
                    self.draw_unit_right(attacking_unit.name, "Red", 0, *base)
                    self.draw_unit_right(defending_unit.name, "Green", 1, *base)

            else:
                moving_unit = action.unit_reference

                pic = self.get_image(self.interface.move_icon)
                self.screen.blit(pic, symbol_location)

                if log.player_color == "Green":
                    self.draw_unit_right(moving_unit.name, "Green", 0, *base)
                elif log.player_color == "Red":
                    self.draw_unit_right(moving_unit.name, "Red", 0, *base)

    def draw_attack(self, action, base, symbol_location, log):
        attacking_unit = action.unit_reference
        defending_unit = action.target_reference
        outcome = get_outcome(attacking_unit, defending_unit, action)

        self.draw_outcome(outcome, *base)

        pic = self.get_image(self.interface.attack_icon)
        self.screen.blit(pic, symbol_location)

        if log.player_color == "Green":
            self.draw_unit_right(attacking_unit.name, "Green", 0, *base)
            self.draw_unit_right(defending_unit.name, "Red", 1, *base)
        elif log.player_color == "Red":
            self.draw_unit_right(attacking_unit.name,  "Red", 0, *base)
            self.draw_unit_right(defending_unit.name, "Green", 1, *base)

    def draw_right(self):
        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)
        self.draw_log()

    def draw_outcome(self, outcome, base_x, base_y):
        location = (base_x + 230 * self.zoom, base_y + 5 * self.zoom)
        self.write(outcome, location, self.font_bigger)

    def draw_turn_box(self, log, base_x, base_y):
        box_width, box_height = 40 * self.zoom, 62 * self.zoom
        position_and_size = (base_x, base_y, box_width, box_height)

        if log.player_color == "Green":
            border_color = self.interface.green_player_color
        else:
            border_color = self.interface.red_player_color

        pygame.draw.rect(self.screen, border_color, position_and_size)

        current_action = 2 - log.action_number
        string = str(current_action)
        location = (base_x + 7 * self.zoom, base_y)
        self.write(string, location, self.font_bigger)

    def draw_unit_right(self, unit_name, color, index, base_x, base_y):

        resize = 0.6 * self.zoom
        location = (base_x + (65 + index * 100) * self.zoom, base_y + 4 * self.zoom )
        unit_pic = self.get_unit_pic(unit_name)
        pic = self.get_image(unit_pic)
        pic = pygame.transform.scale(pic, (int(self.interface.unit_width * resize),
                                           int(self.interface.unit_height * resize)))
        self.screen.blit(pic, location)

    def draw_line(self, start_position, end_position):
        start_coordinates = self.center_coordinates.get(start_position)
        end_coordinates = self.center_coordinates.get(end_position)
        pygame.draw.line(self.screen, colors.black, start_coordinates, end_coordinates, 5)

    def write_message(self, string, pos):
        label = self.font_messages.render(string, _anti_alias, colors.black)
        self.screen.blit(label, pos)

    def write(self, string, pos, font, color=colors.black):
        label = font.render(string, _anti_alias, color)
        self.screen.blit(label, pos)

    def draw_message(self, string):
        self.write_message(string, self.message_location)

    def draw_rectangle(self, dimensions, location, color):
        rectangle = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
        rectangle.fill(color)
        self.screen.blit(rectangle, location)

    def draw_bordered_circle(self, position, size, color):
        pygame.draw.circle(self.screen, colors.black, position, size + 2)
        pygame.draw.circle(self.screen, color, position, size)

    def draw_unit_box(self, base, color):

        def increase_corners(corners, inc):

            corner1 = (corners[0][0] - inc, corners[0][1] - inc)
            corner2 = (corners[1][0] + inc, corners[1][1] - inc)
            corner3 = (corners[2][0] + inc, corners[2][1] + inc)
            corner4 = (corners[3][0] - inc, corners[3][1] + inc)

            return [corner1, corner2, corner3, corner4]

        if color == "Red":
            border_color = self.interface.red_player_color
        else:
            border_color = self.interface.green_player_color

        corner1 = (base[0], base[1])
        corner2 = (base[0] + self.interface.unit_width, base[1])
        corner3 = (base[0] + self.interface.unit_width, base[1] + self.interface.unit_height)
        corner4 = (base[0], base[1] + self.interface.unit_height)

        base_corners = [corner1, corner2, corner3, corner4]

        pygame.draw.lines(self.screen, colors.black, True, base_corners)

        thickness = int(5 * self.zoom)

        for i in range(1, thickness):
            middle_corners = increase_corners(base_corners, i)
            pygame.draw.lines(self.screen, border_color, True, middle_corners)

        outer_corners = increase_corners(base_corners, thickness)
        pygame.draw.lines(self.screen, colors.black, True, outer_corners)


def get_outcome(attacking_unit, defending_unit, action):

    attack = battle.get_attack_rating(attacking_unit, defending_unit, action)
    defence = battle.get_defence_rating(attacking_unit, defending_unit, attack)

    if action.rolls[0] <= attack:
        if action.rolls[1] <= defence:
            return "Defend"
        else:
            return" Win"
    else:
        return " Miss"
