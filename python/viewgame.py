import pygame
from viewcommon import colors
import battle
import viewcommon as m
from coordinates import Coordinates
import settings
import common

zoom = settings.zoom


def draw_game(screen, interface, game, start_position=None, actions=()):

    coordinates, fonts = interface.coordinates, interface.fonts

    pic = m.get_image(interface.board_image)
    screen.blit(pic, (0, 0))

    gamestate = game.gamestate.copy()
    if game.current_player().color == "Red":
        gamestate.flip_units()

    recalculate_special_counters(gamestate)

    for position, unit in gamestate.units[0].items():
        if actions and position == start_position:
            draw_unit(screen, interface, unit, position, game.current_player().color, selected=True)
        else:
            draw_unit(screen, interface, unit, position, game.current_player().color)

    for position, unit in gamestate.units[1].items():
        draw_unit(screen, interface, unit, position, game.players[1].color)

    attacks, moves, abilities = [], [], []
    for action in actions:
        if action.is_attack():
            attacks.append(action)
        elif action.is_ability():
            abilities.append(action)
        else:
            moves.append(action)

    unit_dimensions = (interface.unit_width, interface.unit_height)

    move_locations, attack_locations, ability_locations, sub_attack_locations = set(), set(), set(), set()

    for action in moves:
        location = coordinates["base"].get(action.end_position)
        if location not in move_locations:
            move_locations.add(location)
            m.draw_rectangle(screen, unit_dimensions, location, interface.move_shading)

    for action in attacks:
        location = coordinates["base"].get(action.attack_position)
        if location not in attack_locations:
            attack_locations.add(location)

            m.draw_rectangle(screen, unit_dimensions, location, interface.attack_shading)
            if settings.show_chance_of_win:
                chance_of_win_string = str(int(round(action.chance_of_win * 100))) + "%"
                location = coordinates["percentage"].get(action.attack_position)
                m.write(screen, chance_of_win_string, location, fonts["small"], colors["dodger_blue"])

    for action in abilities:
        location = coordinates["base"].get(action.ability_position)
        if location not in ability_locations:
            ability_locations.add(location)

            location = coordinates["base"].get(action.ability_position)
            m.draw_rectangle(screen, unit_dimensions, location, interface.ability_shading)

    for attack in attacks:
        for sub_attack in attack.sub_actions:
            location = coordinates["base"].get(sub_attack.attack_position)
            if location not in sub_attack_locations and location not in attack_locations:
                sub_attack_locations.add(location)
                m.draw_rectangle(screen, unit_dimensions, location, interface.attack_shading)


def show_attack(self, action, player_unit, opponent_unit):

    self.clear_lower_right()

    base = self.interface.message_location

    attack = battle.get_attack_rating(player_unit, opponent_unit, action)

    defence = battle.get_defence_rating(player_unit, opponent_unit, attack)

    attack = min(attack, 6)

    defence = min(defence, 6)

    lines = ["Attack: " + str(attack),
             "Defence: " + str(defence),
             "Chance of win = " + str(attack) + " / 6 * " + str(6 - defence) + " / 6 = " +
             str(attack * (6 - defence)) + " / 36 = " + str(round(attack * (6 - defence) / 36, 3) * 100) + "%"]

    self.show_lines(lines, *base)

    pygame.display.flip()


def draw_post_movement(screen, interface, action):
    coordinates = interface.coordinates

    pygame.draw.circle(screen, colors["black"], coordinates["center"].get(action.start_position), 10)
    draw_line(screen, interface, action.end_position, action.attack_position)

    pic = m.get_image(interface.move_icon)
    screen.blit(pic, coordinates["battle"].get(action.attack_position))

    pygame.display.update()


def draw_action(screen, interface, action, flip=False):

    if flip:
        action = flip_action(action)

    coordinates = interface.coordinates

    pygame.draw.circle(screen, colors["black"], coordinates["center"].get(action.start_position), 10)
    draw_line(screen, interface, action.start_position, action.end_position)

    if action.is_attack():

        draw_line(screen, interface, action.end_position, action.attack_position)

        if settings.show_dice_game:
            attack_dice = m.get_image(interface.dice[action.rolls[0]])
            screen.blit(attack_dice, coordinates["battle"].get(action.start_position))

            if battle.attack_successful(action):
                defence_dice = m.get_image(interface.dice[action.rolls[1]])
                screen.blit(defence_dice, coordinates["battle"].get(action.attack_position))

        if hasattr(action, "high_morale"):
            pic = m.get_image(interface.high_morale_icon)
            screen.blit(pic, coordinates["battle"].get(action.end_position))

    elif action.is_ability():
        draw_line(screen, interface, action.end_position, action.ability_position)
        pic = m.get_image(interface.ability_icon)
        screen.blit(pic, coordinates["battle"].get(action.ability_position))

    else:
        pic = m.get_image(interface.move_icon)
        screen.blit(pic, coordinates["battle"].get(action.end_position))

    pygame.display.update()


def draw_line(screen, interface, start_position, end_position):
    start_coordinates = interface.coordinates["center"].get(start_position)
    end_coordinates = interface.coordinates["center"].get(end_position)
    pygame.draw.line(screen, colors["black"], start_coordinates, end_coordinates, 5)


def shade_positions(screen, interface, positions):
    for position in positions:
        base = interface.coordinates["base"].get(position)

        dimensions = (interface.unit_width, interface.unit_height)
        m.draw_rectangle(screen, dimensions, base, interface.selected_shading)

    pygame.display.update()


def draw_counters(screen, interface, unit, counters, color, position, counter_coordinates, font_coordinates):
    draw_bordered_circle(screen, counter_coordinates.get(position), interface.counter_size, color)

    if counters > 1:
        m.write(screen, str(unit.blue_counters), font_coordinates.get(position), interface.fonts["small"])


def draw_bordered_circle(screen, position, size, color):
    pygame.draw.circle(screen, colors["black"], position, size + 2)
    pygame.draw.circle(screen, color, position, size)


def draw_symbols(screen, interface, unit, position):
    if unit.get_xp():
        m.write(screen, str(unit.get_xp()), interface.coordinates["flag"].get(position), interface.fonts["xp"])

    if unit.get_bribed():
        draw_bribed(screen, interface, position)
    if hasattr(unit, "is_crusading"):
        draw_crusading(screen, interface, position)


def draw_bribed(screen, interface, position):
    pic = m.get_image(interface.ability_icon)
    screen.blit(pic, interface.coordinates["flag"].get(position))


def draw_crusading(screen, interface, position):
    pic = m.get_image(interface.crusading_icon)
    screen.blit(pic, interface.coordinates["flag"].get(position))


def draw_unit(screen, interface, unit, position, color, selected=False):
    unit_pic = m.get_unit_pic(interface, unit.image)
    counters_drawn = 0

    if unit.blue_counters:
        counter_coordinates = get_counter_coordinates(interface, counters_drawn)
        font_coordinates = get_font_coordinates(interface, counters_drawn)
        counters = unit.blue_counters
        draw_counters(screen, interface, unit, counters, colors["blue"], position, counter_coordinates, font_coordinates)
        counters_drawn += 1
    if unit.yellow_counters:
        counter_coordinates = get_counter_coordinates(interface, counters_drawn)
        font_coordinates = get_font_coordinates(interface, counters_drawn)
        counters = unit.yellow_counters
        draw_counters(screen, interface, unit, counters, colors["yellow"], position, counter_coordinates, font_coordinates)

    dimensions = (int(interface.unit_width), int(interface.unit_height))
    pic = m.get_image(unit_pic, dimensions)

    base_coordinates = Coordinates(interface.base_coordinates, interface)
    base = base_coordinates.get(position)
    screen.blit(pic, base)

    if selected:
        dimensions = (interface.unit_width, interface.unit_height)
        m.draw_rectangle(screen, dimensions, base, interface.selected_shading)

    m.draw_unit_box(screen, interface, base, color)
    draw_symbols(screen, interface, unit, position)


def get_counter_coordinates(interface, counters_drawn):
    return {
        0: Coordinates(interface.first_counter_coordinates, interface),
        1: Coordinates(interface.second_counter_coordinates, interface),
        2: Coordinates(interface.third_counter_coordinates, interface),
    }[counters_drawn]


def get_font_coordinates(interface, counters_drawn):
    return {
        0: Coordinates(interface.first_font_coordinates, interface),
        1: Coordinates(interface.second_font_coordinates, interface),
        2: Coordinates(interface.third_font_coordinates, interface),
    }[counters_drawn]


def flip_action(action):

    action.start_position = common.flip(action.start_position)
    action.end_position = common.flip(action.end_position)
    action.attack_position = common.flip(action.attack_position)
    action.ability_position = common.flip(action.ability_position)

    for sub_action in action.sub_actions:
        action.sub_action = flip_action(sub_action)
    if hasattr(action, "push"):
        action.push_direction = get_transformed_direction(action.push_direction)

    return action


def get_transformed_direction(direction):

    if direction.y == -1:
        return Direction(0, 1)

    if direction.y == 1:
        return Direction(0, -1)

    return direction


def recalculate_special_counters(gamestate):
    for unit in gamestate.units[0].itervalues():
        add_yellow_counters(unit)
        add_blue_counters(unit)

    for unit in gamestate.units[1].itervalues():
        add_yellow_counters(unit)
        add_blue_counters(unit)


def add_yellow_counters(unit):
    if unit.get_extra_life():
        unit.yellow_counters = 1
    else:
        unit.yellow_counters = 0


def add_blue_counters(unit):
    unit.blue_counters = 0
    if unit.is_frozen():
        unit.blue_counters = unit.get_frozen_counters()
    if unit.is_attack_frozen():
        unit.blue_counters = unit.get_attack_frozen_counter()
    if unit.get_recently_bribed():
        unit.blue_counters = 1
