from __future__ import division
import pygame
import textwrap
from viewcommon import *
import interface_settings as settings
import battle
import common

zoom = settings.zoom
zoomed_unit_size = (int(236 * zoom), int(271 * zoom))
upgrade_unit_size = (int(118 * zoom), int(135.5 * zoom))


def clear(screen, interface):
    pygame.draw.rect(screen, colors["light_grey"], interface.lower_right_rectangle)


def get_unit_lines(unit):
    lines = ["A: " + str(unit.attack) + "  D: " + str(unit.defence)
             + "  R: " + str(unit.range) + "  M: " + str(unit.movement)]

    if unit.zoc:
        lines.append("Zone of control against: " + ", ".join(Type.write[unit_type] for unit_type in unit.zoc))
        lines.append("")

    if unit.attack_bonuses:
        for unit_type, value in unit.attack_bonuses.items():
            lines.append("+" + str(value) + " Attack against " + Type.write[unit_type])
            lines.append("")

    if unit.defence_bonuses:
        for unit_type, value in unit.attack_bonuses.items():
            lines.append("+" + str(value) + " Defence against " + Type.write[unit_type])
            lines.append("")

    for trait in unit.traits:
        if trait not in [Trait.attack_skill, Trait.defence_skill, Trait.range_skill, Trait.movement_skill]:
            if unit.has(trait):
                lines.append(Trait.write[trait] + ": " + trait_descriptions[Trait.name[trait]])
                lines.append("")

    for ability in unit.abilities:
        lines.append(common.ability_descriptions[Ability.name[ability]])
        lines.append("")

    for state in unit.states:
        if unit.states[state]:
            lines.append(State.name[state] + ": " + str(unit.states[state]))

    return lines


def show_unit_zoomed(screen, interface, unit):

    unit_pic = get_unit_pic(interface, unit.image)
    pic = get_image(unit_pic, zoomed_unit_size)

    base = interface.show_unit_location
    title_location = base
    image_location = [base[0], base[1] + 20 * zoom]
    text_location = [base[0], base[1] + 290 * zoom]

    write(screen, unit.name, title_location, interface.fonts["normal"])
    screen.blit(pic, image_location)

    lines = get_unit_lines(unit)
    line_length = 45
    show_lines(screen, lines, line_length, interface.line_distances["small"], interface.fonts["small"], *text_location)


def draw_upgrade_choice(screen, interface, index, unit):

    base = interface.upgrade_locations[index]
    title_location = base
    image_location = [base[0], base[1] + 20 * zoom]
    text_location = [base[0], base[1] + 160 * zoom]

    unit_pic = get_unit_pic(interface, unit.image)
    pic = get_image(unit_pic, upgrade_unit_size)
    screen.blit(pic, image_location)

    write(screen, unit.name, title_location, interface.fonts["normal"])

    lines = get_unit_lines(unit)

    line_length = 30
    line_distances = interface.line_distances["small"]
    fonts = interface.fonts["very_small"]
    show_lines(screen, lines, line_length, line_distances, fonts, *text_location)


def show_attack(screen, interface, action, player_unit, opponent_unit, gamestate):

    clear(screen, interface)

    attack = battle.get_attack_rating(player_unit, opponent_unit, action, gamestate)
    defence = battle.get_defence_rating(player_unit, opponent_unit, attack, action, gamestate.enemy_units)
    attack = min(attack, 6)
    defence = min(defence, 6)

    lines = ["Attack: " + str(attack),
             "Defence: " + str(defence),
             "Chance of win = " + str(attack) + " / 6 * " + str(6 - defence) + " / 6 = " +
             str(attack * (6 - defence)) + " / 36 = " + str(round(attack * (6 - defence) / 36, 3) * 100) + "%"]

    base = interface.show_attack_location
    text_location = [base[0], base[1] + 160 * zoom]
    line_length = 80
    show_lines(screen, lines, line_length, interface.line_distances["small"], interface.fonts["small"], *text_location)


def draw_upgrade_options(screen, interface, unit):
    for i in range(2):
        upgrade_choice = unit.get_upgrade_choice(i)
        upgraded_unit = unit.get_upgraded_unit(upgrade_choice)
        draw_upgrade_choice(screen, interface, i, upgraded_unit)


def draw_ask_about_ability(screen, interface, unit):
    clear(screen, interface)
    lines = ["Select ability:"]
    for i, ability in enumerate(unit.abilities):
        ability_name = Ability.name[ability]
        description_string = str(i + 1) + ". " + ability_name + ": " + ability_descriptions[ability_name]
        lines += textwrap.wrap(description_string, interface.message_line_length)

    base = interface.ask_about_ability_location
    text_location = [base[0], base[1] + 160 * zoom]
    line_length = 80
    show_lines(screen, lines, line_length, interface.line_distances["small"], interface.fonts["small"], *text_location)


def draw_unit_lower_right(screen, interface, action, color, index, base_x, base_y):

    if not action.is_attack():
        unit = action.unit.name
    elif index == 0:
        unit = action.unit.name
    else:
        unit = action.target_unit.name

    resize = 0.2 * zoom
    location = (base_x + (65 + index * 100) * zoom, base_y + 8 * zoom)
    unit_pic = get_unit_pic(interface, unit)
    unit_image = get_image(unit_pic)

    unit_image = pygame.transform.scale(unit_image, (int(interface.unit_width * resize),
                                        int(interface.unit_height * resize)))

    screen.blit(unit_image, location)

    draw_unit_box(screen, interface, location, color, resize)
