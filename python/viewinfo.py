from __future__ import division
import units as unitsmodule
import pygame
import textwrap
from viewcommon import *
import settings
import battle

zoom = settings.zoom
zoomed_unit_size = (int(236 * zoom), int(271 * zoom))
upgrade_unit_size = (int(118 * zoom), int(135.5 * zoom))


def clear(screen, interface):
    pygame.draw.rect(screen, colors["light_grey"], interface.lower_right_rectangle)


def show_unit_zoomed(screen, interface, unit):

    unit_pic = get_unit_pic(interface, unit.image)
    pic = get_image(unit_pic, zoomed_unit_size)

    base = interface.show_unit_location
    title_location = base
    image_location = [base[0], base[1] + 20 * zoom]
    text_location = [base[0], base[1] + 290 * zoom]
    lines = []

    write(screen, unit.name, title_location, interface.fonts["normal"])
    screen.blit(pic, image_location)

    for attribute in ["attack", "defence", "range", "movement"]:
        if getattr(unit, attribute):
            value = getattr(unit, attribute)
            lines.append(attribute.title() + ": " + str(value))
        else:
            lines.append(attribute.title() + ": %")
    lines.append("")

    if unit.zoc:
        lines.append("Zone of control against: " + ", ".join(type for type in unit.zoc))
        lines.append("")

    if hasattr(unit, "descriptions"):
        for attribute, description in unit.descriptions.items():
            if attribute in unit.abilities:
                lines.append(attribute.replace("_", " ").title() + ": " + description)
            else:
                lines.append(description)
            lines.append("")

    for attribute in unit.variables:
        if unit.variables[attribute]:
            lines.append(attribute + ": " + str(unit.variables[attribute]))

    line_length = 40
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

    lines = []

    for attribute in ["attack", "defence", "range", "movement"]:
        if getattr(unit, attribute):
            value = getattr(unit, attribute)
            lines.append(attribute.title() + ": " + str(value))
        else:
            lines.append(attribute.title() + ": %")
    lines.append("")

    if unit.zoc:
        lines.append("Zone of control against: " + ", ".join(type for type in unit.zoc))
        lines.append("")

    if hasattr(unit, "descriptions"):
        for attribute, description in unit.descriptions.items():
            if attribute in unit.abilities:
                lines.append(attribute.replace("_", " ").title() + ": " + description)
            else:
                lines.append(description)
            lines.append("")

    line_length = 30
    show_lines(screen, lines, line_length, interface.line_distances["small"], interface.fonts["small"], *text_location)


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

    for i, upgrade in enumerate(unit.upgrades):
        upgrade = getattr(unitsmodule, unit.upgrades[i].replace(" ", "_"))()
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
        unit = action.unit_reference.name
    elif index == 0:
        unit = action.unit_reference.name
    else:
        unit = action.target_reference.name

    resize = 0.2 * zoom
    location = (base_x + (65 + index * 100) * zoom, base_y + 8 * zoom)
    unit_pic = get_unit_pic(interface, unit)
    unit_image = get_image(unit_pic)

    unit_image = pygame.transform.scale(unit_image, (int(interface.unit_width * resize),
                                        int(interface.unit_height * resize)))

    screen.blit(unit_image, location)

    draw_unit_box(screen, interface, location, color, resize)

