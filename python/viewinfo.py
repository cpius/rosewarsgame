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
             + "  R: " + str(unit.range) + "  M: " + str(unit.movement), ""]

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

    for trait, info in unit.traits.items():
        if trait not in [Trait.attack_skill, Trait.defence_skill, Trait.range_skill, Trait.movement_skill]:
            level = info[1]
            if level == 1:
                lines.append(Trait.write[trait] + ":")
                lines.append(get_description(trait, 1))
                lines.append("")
            elif level > 1:
                lines.append(Trait.write[trait] + ", level " + str(level) + ":")
                lines.append(get_description(trait, level))
                lines.append("")

    for ability, info in unit.abilities.items():
        level = info[0]
        if level == 1:
            lines.append(Ability.write[ability] + ":")
            lines.append(get_description(ability, 1))
            lines.append("")
        else:
            lines.append(Ability.write[ability] + ", " + "level " + str(level) + ":")
            lines.append(get_description(ability, level))
            lines.append("")

    for state, info in unit.states.items():
        value = info[1]
        if value and state not in [State.used, State.recently_upgraded, State.experience]:
            lines.append(State.name[state] + ": " + str(value))

    for effect, info in unit.effects.items():
        level = info[0]
        value = info[1]
        if level == 1:
            lines.append(Effect.write[effect] + ": " + str(value))
        else:
            lines.append(Effect.write[effect] + ", level " + str(level) + ": " + str(value))
        lines.append("")

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


def draw_upgrade_choice(screen, interface, index, upgrade_choice, unit):

    base = interface.upgrade_locations[index]
    title_location = base
    image_location = [base[0], base[1] + 20 * zoom]
    text_location = [base[0], base[1] + 160 * zoom]
    unit = unit.get_upgraded_unit(upgrade_choice)

    unit_pic = get_unit_pic(interface, unit.image)
    pic = get_image(unit_pic, upgrade_unit_size)
    screen.blit(pic, image_location)
    write(screen, unit.name, title_location, interface.fonts["normal"])

    if isinstance(upgrade_choice, basestring):
        lines = get_unit_lines(unit)
        line_length = 30
        line_distances = interface.line_distances["small"]
        fonts = interface.fonts["very_small"]
        show_lines(screen, lines, line_length, line_distances, fonts, *text_location)

    else:
        upgrade_choice = readable(upgrade_choice)
        lines = []
        for name, level in upgrade_choice.items():
            print name, level
            if level > 1:
                lines.append(name.replace("_", " ") + ", level " + str(level))
            else:
                lines.append(name.replace("_", " "))
            lines.append("")
        line_length = 30
        line_distances = interface.line_distances["small"]
        fonts = interface.fonts["small"]
        print lines
        show_lines(screen, lines, line_length, line_distances, fonts, *text_location)


def show_attack(screen, interface, action, player_unit, opponent_unit, gamestate):

    clear(screen, interface)

    attack = battle.get_attack_rating(player_unit, opponent_unit, action, gamestate.player_units)
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
        draw_upgrade_choice(screen, interface, i, upgrade_choice, unit)


def draw_ask_about_ability(screen, interface, unit):
    clear(screen, interface)
    lines = ["Select ability:"]
    for i, ability in enumerate(unit.abilities):
        level = unit.get_level(ability)
        description_string = str(i + 1) + ": " + Ability.write[ability] + ": " + get_description(ability, level)
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
