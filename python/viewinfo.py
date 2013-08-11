from __future__ import division
import units as unitsmodule
import pygame
import textwrap
from viewcommon import *
import settings
import battle
import common

zoom = settings.zoom
zoomed_unit_size = (int(236 * zoom), int(271 * zoom))
upgrade_unit_size = (int(118 * zoom), int(135.5 * zoom))


def clear(screen, interface):
    pygame.draw.rect(screen, colors["light_grey"], interface.lower_right_rectangle)


def get_unit_lines(unit):
    lines = []
    for attribute in ["attack", "defence", "range", "movement"]:
        if getattr(unit, attribute):
            value = getattr(unit, attribute)
            lines.append(attribute.title() + ": " + str(value))
        else:
            lines.append(attribute.title() + ": %")

    type = Type.write[unit.type]
    lines.append("Type: " + type)
    lines.append("")

    if unit.zoc:
        lines.append("Zone of control against: " + ", ".join(Type.write[type] for type in unit.zoc))
        lines.append("")

    if unit.attack_bonuses:
        for type, value in unit.attack_bonuses.items():
            lines.append("+" + str(value) + " Attack against " + Type.write[type])
            lines.append("")

    if unit.defence_bonuses:
        for type, value in unit.attack_bonuses.items():
            lines.append("+" + str(value) + " Defence against " + Type.write[type])
            lines.append("")

    for trait in unit.constants:
        lines.append(common.trait_descriptions[Trait.reverse_mapping[trait]])
        lines.append("")

    for ability in unit.abilities:
        lines.append(common.ability_descriptions[Ability.reverse_mapping[ability]])
        lines.append("")

    for attribute in unit.variables:
        if unit.variables[attribute]:
            lines.append(Trait.write[attribute] + ": " + str(unit.variables[attribute]))

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
    lines.append("---------------------------------------------")
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
    show_lines(screen, lines, line_length, interface.line_distances["small"], interface.fonts["very_small"], *text_location)


def show_attack(screen, interface, action, player_unit, opponent_unit, gamestate):

    clear(screen, interface)

    attack = battle.get_attack_rating(player_unit, opponent_unit, action, gamestate)
    defence = battle.get_defence_rating(player_unit, opponent_unit, attack, gamestate)
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
        if isinstance(unit.upgrades[i], str):
            upgrade_choice = unit.upgrades[i]
            upgrade = getattr(unitsmodule, upgrade_choice.replace(" ", "_"))()
            draw_upgrade_choice(screen, interface, i, upgrade)
        else:
            upgrade = getattr(unitsmodule, unit.name.replace(" ", "_"))()
            upgrade.constants = unit.constants.copy()
            upgrade.constants = unit.upgrades[0][i]
            draw_upgrade_choice(screen, interface, i, upgrade)


def draw_ask_about_ability(screen, interface, unit):
    clear(screen, interface)
    lines = ["Select ability:"]
    for i, ability in enumerate(unit.abilities):
        description_string = str(i + 1) + ". " + ability.title() + ": " + unit.descriptions[ability]
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

