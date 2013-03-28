import pygame
import settings
from coordinates import Coordinates
import battle
import colors


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
        self.message_coordinates = self.interface.message_coordinates

        self.screen = pygame.display.set_mode(self.interface.board_size)

        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)

        self.font = pygame.font.SysFont(self.interface.normal_font_name, self.interface.normal_font_size, True, False)
        self.font_big = pygame.font.SysFont(self.interface.normal_font_name, self.interface.big_font_size, True, False)
        self.font_bigger = pygame.font.SysFont(self.interface.normal_font_name, self.interface.bigger_font_size, True,
                                               False)
        self.base_coordinates = Coordinates(self.interface.base_coordinates, self.interface)
        self.percentage_coordinates = Coordinates(self.interface.percentage_coordinates, self.interface)
        self.percentage_sub_coordinates = Coordinates(self.interface.percentage_sub_coordinates, self.interface)
        self.center_coordinates = Coordinates(self.interface.center_coordinates, self.interface)
        self.symbol_coordinates = Coordinates(self.interface.symbol_coordinates, self.interface)

        self.logbook = []

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
        xpos = self.message_coordinates[0]
        ypos = self.message_coordinates[1]
        label = self.font_big.render("Select counter for", 1, colors.black)
        self.screen.blit(label, (xpos, ypos))
        label = self.font_big.render(unit_name, 1, colors.black)
        self.screen.blit(label, (xpos, ypos + 25 * self.zoom))
        label = self.font_big.render("'a' for attack", 1, colors.black)
        self.screen.blit(label, (xpos, ypos + 50 * self.zoom))
        label = self.font_big.render("'d' for defence", 1, colors.black)
        self.screen.blit(label, (xpos, ypos + 75 * self.zoom))
        pygame.display.update()

    def draw_ask_about_ability(self, ability1, ability2):
        xpos = self.message_coordinates[0]
        ypos = self.message_coordinates[1]
        label = self.font_big.render("Select ability:", 1, colors.black)
        self.screen.blit(label, (xpos, ypos))
        label = self.font_big.render("1 for " + ability1, 1, colors.black)
        self.screen.blit(label, (xpos, ypos + 25 * self.zoom))
        label = self.font_big.render("2 for " + ability2, 1, colors.black)
        self.screen.blit(label, (xpos,  ypos + 50 * self.zoom))
        pygame.display.update()

    def show_unit_zoomed(self, unit_name, color):
        unit_pic = self.get_unit_pic(unit_name, color, True)
        pic = self.get_image(unit_pic)
        self.screen.blit(pic, self.interface.show_unit_coordinates)
        pygame.display.flip()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, "./replay/" + name + ".jpeg")

    def draw_game_end(self, color):
        font = pygame.font.SysFont("monospace", 55, bold=True)
        label = font.render(color + " Wins", 1, colors.black)
        self.screen.blit(label, self.message_coordinates)
        pygame.display.update()

    def get_image(self, path, dimensions=None):
        global _image_library
        image = _image_library.get(path)
        if not image:
            image = pygame.image.load(path).convert()
            if dimensions:
                image = pygame.transform.scale(image, dimensions)
            else:
                image = pygame.transform.scale(image, (int(image.get_size()[0] * self.zoom), int(image.get_size()[1] * self.zoom)))
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
        pygame.draw.circle(self.screen, self.interface.counter_circle_color, counter_coordinates.get(position), 10, 0)
        pygame.draw.circle(self.screen, colors.brown, counter_coordinates.get(position), 8, 0)
        if unit.attack_counters != 1:
            label = self.font.render(str(unit.attack_counters), 1, colors.black)
            self.screen.blit(label, font_coordinates.get(position))

    def draw_defence_counters(self, unit, position, counter_coordinates, font_coordinates):
        if hasattr(unit, "sabotaged"):
            defence_counters = -1
        else:
            defence_counters = unit.defence_counters

        pygame.draw.circle(self.screen, self.interface.counter_circle_color, counter_coordinates.get(position), 10, 0)
        pygame.draw.circle(self.screen, colors.light_grey, counter_coordinates.get(position), 8, 0)

        counter_text = None
        if defence_counters > 1:
            counter_text = str(defence_counters)
        elif defence_counters < 0:
            counter_text = "x"

        if counter_text:
            label = self.font.render(counter_text, 1, colors.black)
            self.screen.blit(label, font_coordinates.get(position))

    def draw_yellow_counters(self, unit, position, counter_coordinates):
        if unit.yellow_counters:
            pygame.draw.circle(self.screen, self.interface.counter_circle_color, counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, colors.yellow, counter_coordinates.get(position), 8, 0)

    def draw_blue_counters(self, unit, position, counter_coordinates, font_coordinates):
        if unit.blue_counters:
            pygame.draw.circle(self.screen, self.interface.counter_circle_color, counter_coordinates.get(position), 10, 0)
            pygame.draw.circle(self.screen, colors.blue, counter_coordinates.get(position), 8, 0)

            if unit.blue_counters > 1:
                label = self.font.render(str(unit.blue_counters), 1, colors.black)
                self.screen.blit(label, font_coordinates.get(position))

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

    def draw_message(self, string):
        label = self.font_big.render(string, 1, colors.black)
        self.screen.blit(label, self.message_coordinates)

    def draw_unit(self, unit, position, color, selected=False):
        unit_pic = self.get_unit_pic(unit.name, color)
        dimensions = (int(self.interface.unit_width), int(self.interface.unit_height))
        pic = self.get_image(unit_pic, dimensions)

        self.screen.blit(pic, self.base_coordinates.get(position))

        base = self.base_coordinates.get(position)

        if selected:
            rect = pygame.Surface((self.interface.unit_width, self.interface.unit_height), pygame.SRCALPHA, 32)
            rect.fill((0, 0, 0, 160))
            self.screen.blit(rect, base)

        if color == "Red":
            border_color = self.interface.red_player_color
        else:
            border_color = self.interface.green_player_color

        base_corners = [(base[0], base[1]), (base[0] + self.interface.unit_width, base[1]),
                        (base[0] + self.interface.unit_width, base[1] + self.interface.unit_height),
                        (base[0], base[1] + self.interface.unit_height)]

        pygame.draw.lines(self.screen, colors.black, True, base_corners)

        line_count = int(5 * self.zoom)

        for i in range(1, line_count):
            middle_corners = increase_corners(base_corners, i)
            pygame.draw.lines(self.screen, border_color, True, middle_corners)

        outer_corners = increase_corners(base_corners, line_count)
        pygame.draw.lines(self.screen, colors.black, True, outer_corners)

        self.draw_counters(unit, position)
        self.draw_symbols(unit, position)

    def draw_game(self, gamestate, start_position=None, actions=()):

        pic = self.get_image(self.interface.board_image)
        self.screen.blit(pic, (0, 0))

        for position, unit in gamestate.units[0].items():
            if actions and position == start_position:
                self.draw_unit(unit, position, gamestate.current_player().color, True)
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

        for action in moves:
            rect = pygame.Surface((self.interface.unit_width, self.interface.unit_height), pygame.SRCALPHA, 32)
            rect.fill((0, 0, 0, 160))
            self.screen.blit(rect, coordinates.get(action.end_position))

        for action in attacks:
            rect = pygame.Surface((self.interface.unit_width, self.interface.unit_height), pygame.SRCALPHA, 32)
            rect.fill((130, 0, 0, 110))
            self.screen.blit(rect, coordinates.get(action.attack_position))
            label = self.font.render(str(int(round(action.chance_of_win * 100))) + "%", 1, colors.dodger_blue)
            self.screen.blit(label, self.percentage_coordinates.get(action.attack_position))

        for action in abilities:
            rect = pygame.Surface((self.interface.unit_width, self.interface.unit_height), pygame.SRCALPHA, 32)
            rect.fill((0, 0, 150, 130))
            self.screen.blit(rect, coordinates.get(action.attack_position))

        for attack in attacks:
            for sub_attack in attack.sub_actions:
                if not any(check_attack.attack_position == sub_attack.attack_position for check_attack in attacks):
                    rect = pygame.Surface((self.interface.unit_width, self.interface.unit_height), pygame.SRCALPHA, 32)
                    rect.fill((130, 0, 0, 110))
                    self.screen.blit(rect, coordinates.get(sub_attack.attack_position))
                    label = self.font.render(str(int(round(sub_attack.chance_of_win * 100))) + "%", 1, colors.yellow)
                    self.screen.blit(label, self.percentage_sub_coordinates.get(sub_attack.attack_position))

        self.draw_right()

        pygame.display.update()

    def draw_action(self, action, gamestate):

        log = Log(action, gamestate.turn, gamestate.get_actions_remaining(), gamestate.current_player().color)
        self.logbook.append(log)

        if len(self.logbook) > 5:
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

    def get_unit_pic(self, name, color=None, zoomed=False):
        if zoomed:
            return "./zoomed/" + name.replace(" ", "-") + ",-" + color + ".jpg"
        else:
            return "./" + self.interface.unit_folder + "/" + name.replace(" ", "-") + ".jpg"

    def refresh(self):
        pygame.display.flip()

    def draw_log(self):

        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)

        for index, log in enumerate(self.logbook):

            action = log.action
            vpos = index * 64
            hpos = 391

            self.draw_turn_box(log, hpos, vpos)

            startpos = (int(hpos * self.zoom), int((vpos + 62) * self.zoom))
            endpos = (int(self.interface.board_size[1] * self.zoom), int((vpos + 62) * self.zoom))
            pygame.draw.line(self.screen, colors.black, startpos, endpos, 4)

            if action.is_attack:
                attacking_unit = action.unit_reference
                defending_unit = action.target_reference
                outcome = get_outcome(attacking_unit, defending_unit, action)

                self.draw_outcome(outcome, hpos, vpos)

                pic = self.get_image(self.interface.attack_icon)
                self.screen.blit(pic, ((hpos + 118) * self.zoom, (vpos + 12) * self.zoom))

                if log.player_color == "Green":
                    self.draw_unit_right(attacking_unit.name, "Green", 0, 0.7, hpos, vpos)
                    self.draw_unit_right(defending_unit.name, "Red", 1, 0.7, hpos, vpos)

                if log.player_color == "Red":
                    self.draw_unit_right(attacking_unit.name, "Red", 0, 0.7, hpos, vpos)
                    self.draw_unit_right(defending_unit.name, "Green", 1, 0.7, hpos, vpos)

            elif action.is_ability:

                attacking_unit = action.unit_reference
                defending_unit = action.target_reference

                pic = self.get_image(self.interface.ability_icon)
                self.screen.blit(pic, ((hpos + 118) * self.zoom, (vpos + 12) * self.zoom))

                if log.player_color == "Green":
                    self.draw_unit_right(attacking_unit.name, "Green", 0, 0.7, hpos, vpos)
                    self.draw_unit_right(defending_unit.name, "Red", 1, 0.7, hpos, vpos)

                if log.player_color == "Red":
                    self.draw_unit_right(attacking_unit.name, "Red", 0, 0.7, hpos, vpos)
                    self.draw_unit_right(defending_unit.name, "Green", 1, 0.7, hpos, vpos)

            else:
                moving_unit = action.unit_reference

                pic = self.get_image(self.interface.move_icon)
                self.screen.blit(pic, ((hpos + 118) * self.zoom, (vpos + 12) * self.zoom))

                if log.player_color == "Green":
                    self.draw_unit_right(moving_unit.name, "Green", 0, 0.7, hpos, vpos)

                if log.player_color == "Red":
                    self.draw_unit_right(moving_unit.name, "Red", 0, 0.7, hpos, vpos)

    def draw_right(self):
        pygame.draw.rect(self.screen, colors.light_grey, self.interface.right_side_rectangle)
        self.draw_log()

    def draw_outcome(self, outcome, hpos, vpos):
        label = self.font_bigger.render(str(outcome), 1, colors.black)
        self.screen.blit(label, ((hpos + 230) * self.zoom, (vpos + 5) * self.zoom))

    def draw_turn_box(self, log, hpos, vpos):
        position_and_size = (hpos * self.zoom, vpos * self.zoom, 40 * self.zoom, 62 * self.zoom)

        if log.player_color == "Green":
            border_color = self.interface.green_player_color
        else:
            border_color = self.interface.red_player_color

        pygame.draw.rect(self.screen, border_color, position_and_size)

        label = self.font_bigger.render(str(2 - log.action_number), 1, colors.black)
        self.screen.blit(label, ((hpos + 7) * self.zoom, vpos * self.zoom))

    def draw_unit_right(self, unit_name, unit_color, index, resize, hpos, vpos):

        vpos = (vpos + 4) * self.zoom
        hpos = (hpos + 65 + index * 100) * self.zoom
        unit_pic = self.get_unit_pic(unit_name, unit_color)
        pic = self.get_image(unit_pic)
        pic = pygame.transform.scale(pic, (int(self.interface.unit_width * resize), int(self.interface.unit_height * resize)))
        self.screen.blit(pic, (hpos, vpos))

        position_and_size_fill = (hpos - 2, vpos - 2, self.interface.unit_width * resize + 4, self.interface.unit_height * resize + 4)

        if unit_color == "Green":
            rect_color = self.interface.green_player_color
        else:
            rect_color = self.interface.red_player_color

        pygame.draw.rect(self.screen, rect_color, position_and_size_fill, 3)

    def draw_line(self, start_position, end_position):
        start_coordinates = self.center_coordinates.get(start_position)
        end_coordinates = self.center_coordinates.get(end_position)
        pygame.draw.line(self.screen, colors.black, start_coordinates, end_coordinates, 5)


def increase_corners(corners, inc):

    corner1 = (corners[0][0] - inc, corners[0][1] - inc)
    corner2 = (corners[1][0] + inc, corners[1][1] - inc)
    corner3 = (corners[2][0] + inc, corners[2][1] + inc)
    corner4 = (corners[3][0] - inc, corners[3][1] + inc)

    return [corner1, corner2, corner3, corner4]


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
