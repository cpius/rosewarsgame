import units as unitsmodule
import pygame
import textwrap
import viewmethods as m
import settings

zoom = settings.zoom
zoomed_unit_size = (int(236 * zoom), int(271 * zoom))
upgrade_unit_size = (int(118 * zoom), int(135.5 * zoom))


def show_unit_zoomed(screen, interface, unit):

    unit_pic = m.get_unit_pic(interface, unit.image)
    pic = m.get_image(unit_pic, zoomed_unit_size)

    base = interface.show_unit_location
    title_location = base
    image_location = [base[0], base[1] + 20 * zoom]
    text_location = [base[0], base[1] + 290 * zoom]
    lines = []

    m.write(screen, unit.name, title_location, interface.fonts["normal"])
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

    line_length = 30
    m.show_lines(screen, lines, line_length, interface.line_distances["small"], interface.fonts["small"], *text_location)


    pygame.display.flip()


def draw_upgrade_choice(screen, interface, index, unit):

    base = interface.upgrade_locations[index]
    title_location = base
    image_location = [base[0], base[1] + 20 * zoom]
    text_location = [base[0], base[1] + 160 * zoom]

    unit_pic = m.get_unit_pic(interface, unit.image)
    pic = m.get_image(unit_pic, upgrade_unit_size)
    screen.blit(pic, image_location)

    m.write(screen, unit.name, title_location, interface.fonts["normal"])

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
    m.show_lines(screen, lines, line_length, interface.line_distances["small"], interface.fonts["small"], *text_location)


def draw_upgrade_options(screen, interface, unit):

    for i, upgrade in enumerate(unit.upgrades):
        upgrade = getattr(unitsmodule, unit.upgrades[i].replace(" ", "_"))()
        draw_upgrade_choice(screen, interface, i, upgrade)

    pygame.display.flip()


def draw_ask_about_ability(unit):
    x, y = self.message_location
    lines = ["Select ability:"]
    for i, ability in enumerate(unit.abilities):
        description_string = str(i + 1) + ". " + ability.title() + ": " + unit.descriptions[ability]
        lines += textwrap.wrap(description_string, self.interface.message_line_length)

    for i, line in enumerate(lines):
        line_y = y + i * self.message_line_distance
        m.write(line, (x, line_y), location, font)

    pygame.display.update()


def draw_unit_lower_right(screen, interface, action, color, index, base_x, base_y):

    if not action.is_attack:
        unit = action.unit_reference.name
    elif index == 0:
        unit = action.unit_reference.name
    else:
        unit = action.target_reference.name

    resize = 0.2 * zoom
    location = (base_x + (65 + index * 100) * zoom, base_y + 8 * zoom)
    unit_pic = m.get_unit_pic(interface, unit)
    unit_image = m.get_image(unit_pic)

    unit_image = pygame.transform.scale(unit_image, (int(interface.unit_width * resize),
                                        int(interface.unit_height * resize)))

    screen.blit(unit_image, location)

    m.draw_unit_box(screen, interface, location, color, resize)

