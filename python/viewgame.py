from viewcommon import *
from coordinates import Coordinates


def draw_game(screen, interface, game, start_at=None, actions=()):

    screen.blit(get_image(interface.board_image), (0, 0))

    gamestate = game.gamestate.copy()
    if not game.is_player_human():
        gamestate.flip_all_units()

    current_color = game.current_player().color
    enemy_color = game.opponent_player().color
    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units

    draw_units(screen, interface, player_units, current_color, enemy_units, enemy_color, start_at, actions)

    if actions:
        shade_actions(screen, interface, actions)


def draw_units(screen, interface, player_units, player_color, enemy_units, opponent_color, start_position, actions):
    for position, unit in player_units.items():
        if actions and position == start_position:
            draw_unit(screen, interface, unit, position, player_color, selected=True)
        else:
            draw_unit(screen, interface, unit, position, player_color)

    for position, unit in enemy_units.items():
        draw_unit(screen, interface, unit, position, opponent_color)


def shade_actions(screen, interface, actions):
    unit_dimensions = (interface.unit_box_width, interface.unit_box_height)
    drawn_tiles = set()
    for action in actions:
        if action.is_attack():
            location = interface.coordinates["base_box"].get(action.target_at)
            if location not in drawn_tiles:
                drawn_tiles.add(location)
                draw_rectangle(screen, unit_dimensions, location, interface.attack_shading)
        elif action.is_ability():
            location = interface.coordinates["base_box"].get(action.target_at)
            if location not in drawn_tiles:
                drawn_tiles.add(location)
                draw_rectangle(screen, unit_dimensions, location, interface.ability_shading)
        else:
            location = interface.coordinates["base_box"].get(action.end_at)
            if location not in drawn_tiles:
                drawn_tiles.add(location)
                draw_rectangle(screen, unit_dimensions, location, interface.move_shading)


def draw_post_movement(screen, interface, action):
    pygame.draw.circle(screen, Color.Black, interface.coordinates["center"].get(action.start_at), 10)
    draw_line(screen, interface, action.end_at, action.target_at)
    pic = get_image(interface.move_icon)
    screen.blit(pic, interface.coordinates["battle"].get(action.target_at))


def draw_action_dice(screen, interface, action, rolls):

    pass


def draw_action(screen, interface, action, outcome, flip=False):
    if flip:
        aligned_action = flip_action(action)
    else:
        aligned_action = action

    coordinates = interface.coordinates

    pygame.draw.circle(screen, Color.Black, coordinates["center"].get(aligned_action.start_at), 10)
    draw_line(screen, interface, aligned_action.start_at, aligned_action.end_at)

    if aligned_action.is_attack():
        draw_line(screen, interface, aligned_action.end_at, aligned_action.target_at)

        rolls = outcome.for_position(action.target_at)
        if rolls:
            draw_action_dice(screen, interface, aligned_action, rolls)
        else:
            pic = get_image(interface.attack_icon)
            screen.blit(pic, coordinates["battle"].get(aligned_action.target_at))

    elif aligned_action.is_ability():
        draw_line(screen, interface, aligned_action.end_at, aligned_action.target_at)
        pic = get_image(interface.ability_icon)
        screen.blit(pic, coordinates["battle"].get(aligned_action.target_at))

    else:
        pic = get_image(interface.move_icon)
        screen.blit(pic, coordinates["battle"].get(aligned_action.end_at))


def draw_line(screen, interface, start_position, end_position):
    start_coordinates = interface.coordinates["center"].get(start_position)
    end_coordinates = interface.coordinates["center"].get(end_position)
    pygame.draw.line(screen, Color.Black, start_coordinates, end_coordinates, 5)


def shade_positions(screen, interface, positions, color=None):
    for position in positions:
        base = interface.coordinates["base"].get(position)
        dimensions = (interface.unit_width, interface.unit_height)
        if color:
            draw_rectangle(screen, dimensions, base, color)
        else:
            draw_rectangle(screen, dimensions, base, interface.selected_shading)


def draw_counters(screen, interface, counters, color, position, counter_coordinates, font_coordinates):
    draw_bordered_circle(screen, counter_coordinates.get(position), interface.counter_size, color)

    if counters > 1:
        write(screen, str(counters), font_coordinates.get(position), interface.fonts["small"])


def draw_bordered_circle(screen, position, size, color):
    pygame.draw.circle(screen, Color.Black, position, size + 2)
    pygame.draw.circle(screen, color, position, size)


def draw_symbols(screen, interface, unit, position):

    def find_base(index):
        base = interface.coordinates["bottom_left"].get(position)
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
        pygame.draw.lines(screen, Color.Black, True, base_corners)
        draw_rectangle(screen, (3, 6), (base[0] + 1, base[1] + 1), color)

    total_boxes = unit.experience_to_upgrade
    blue_boxes = unit.get(State.experience) % unit.experience_to_upgrade
    for index in range(blue_boxes):
        draw_box(index, Color.Light_blue)

    for index in range(blue_boxes, total_boxes):
        draw_box(index, Color.White)

    if unit.has(Effect.bribed):
        draw_bribed(screen, interface, position)

    level = unit.get_unit_level()
    if not unit.should_be_upgraded() and level:
        if level > 3:
            level = 3
        pic = get_image(interface.level_icons[level], (14, 14))
        screen.blit(pic, interface.coordinates["top_left"].get(position))


def draw_bribed(screen, interface, position):
    pic = get_image(interface.ability_icon)
    screen.blit(pic, interface.coordinates["flag"].get(position))


def draw_unit(screen, interface, unit, position, color, selected=False):
    unit_pic = get_unit_pic(interface, unit)
    counters_drawn = 0

    dimensions = (int(interface.unit_width), int(interface.unit_height))
    pic = get_image(unit_pic, dimensions)

    base_coordinates = Coordinates(interface.base_coordinates, interface)
    base = base_coordinates.get(position)
    screen.blit(pic, base)

    if selected:
        draw_rectangle(screen, dimensions, base, interface.selected_shading)

    if get_blue_counters(unit):
        counter_coordinates = get_counter_coordinates(interface, counters_drawn)
        font_coordinates = get_font_coordinates(interface, counters_drawn)
        counters = get_blue_counters(unit)
        draw_counters(screen, interface, counters, Color.Blue, position, counter_coordinates, font_coordinates)
        counters_drawn += 1
    if get_yellow_counters(unit):
        counter_coordinates = get_counter_coordinates(interface, counters_drawn)
        font_coordinates = get_font_coordinates(interface, counters_drawn)
        counters = get_yellow_counters(unit)
        draw_counters(screen, interface, counters, Color.Yellow, position, counter_coordinates, font_coordinates)

    draw_unit_box(screen, interface, base, color)
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

    flipped_action = action.copy()

    for attribute in ["start_at", "end_at", "target_at"]:
        if getattr(flipped_action, attribute):
            setattr(flipped_action, attribute, getattr(flipped_action, attribute).flip())

    return flipped_action


def get_yellow_counters(unit):
    return 1 if (unit.has_extra_life() or unit.has(Effect.improved_weapons)) else 0


def get_blue_counters(unit):
    return max(unit.get(Effect.poisoned), unit.get(Effect.attack_frozen), unit.has(State.recently_bribed))


def draw_ask_about_move_with_attack(screen, interface, position):
    base = interface.coordinates["base"].get(position)
    dimensions = (interface.unit_width, interface.unit_height)
    draw_rectangle(screen, dimensions, base, interface.selected_shading)
