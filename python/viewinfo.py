from __future__ import division
from viewcommon import *


class Viewinfo:

    def __init__(self, interface, screen, zoom):
        self.interface = interface
        self.screen = screen
        self.zoom = zoom
        self.unit_dimensions = (int(236 * zoom), int(271 * zoom))
        self.upgrade_unit_dimensions = (int(118 * zoom), int(135.5 * zoom))

    def clear(self):
        pygame.draw.rect(self.screen, Color.Light_grey, self.interface.lower_right_rectangle)

    @staticmethod
    def get_unit_lines(unit):
        defence = unit.defence
        if unit.has(Effect.sabotaged):
            defence = 0
        lines = ["A: " + str(unit.attack) + "  D: " + str(defence)
                 + "  R: " + str(unit.range) + "  M: " + str(unit.movement), ""]

        level = unit.get_unit_level()
        if level:
            lines.append("Level: " + str(level + 1))
            lines.append("")

        if unit.zoc:
            lines.append("Zone of control against: " + ", ".join(Type.write[unit_type] for unit_type in unit.zoc))
            lines.append("")

        if unit.attack_bonuses:
            for unit_type, value in unit.attack_bonuses.items():
                lines.append("+" + str(value) + " Attack against " + Type.write[unit_type])
                lines.append("")

        if unit.defence_bonuses:
            for unit_type, value in unit.defence_bonuses.items():
                if unit_type == Type.War_Machine:
                    lines.append("+" + str(value) + " Defence against War Machines")
                else:
                    lines.append("+" + str(value) + " Defence against " + Type.write[unit_type])
                lines.append("")

        for trait, level in unit.traits.items():
            if trait not in [Trait.attack_skill, Trait.defence_skill, Trait.range_skill, Trait.movement_skill,
                             Trait.extra_life]:
                if level == 1:
                    lines.append(Trait.write[trait] + ":")
                    lines.append(get_description(trait, 1))
                    lines.append("")
                elif level > 1:
                    lines.append(Trait.write[trait] + ", level " + str(level) + ":")
                    lines.append(get_description(trait, level))
                    lines.append("")

        for ability, level in unit.abilities.items():
            if level == 1:
                lines.append(Ability.write[ability] + ":")
                lines.append(get_description(ability, 1))
                lines.append("")
            else:
                lines.append(Ability.write[ability] + ", " + "level " + str(level) + ":")
                lines.append(get_description(ability, level))
                lines.append("")

        for state, value in unit.states.items():
            if value and state not in [State.used, State.recently_upgraded, State.experience, State.lost_extra_life,
                                       State.javelin_thrown]:
                lines.append(State.name[state] + ": " + str(value))

        for effect, info in unit.effects.items():
            level = info[0]
            duration = info[1]
            if level == 1:
                lines.append(Effect.write[effect] + ": " + str(duration))
            else:
                lines.append(Effect.write[effect] + ", level " + str(level) + ": " + str(duration))
            lines.append("")

        if unit.has(Trait.extra_life):
            if unit.has(State.lost_extra_life):
                lines.append("No extra life")
            else:
                lines.append("Has extra life")
            lines.append("")

        if unit.has(Trait.javelin):
            if unit.has(State.javelin_thrown):
                lines.append("Javelin thrown")
            else:
                lines.append("Has javelin")
            lines.append("")

        return lines

    def show_unit_zoomed(self, unit, attack_hint):

        unit_pic = get_unit_pic(self.interface, unit)
        pic = get_image(unit_pic, self.unit_dimensions)

        base = self.interface.show_unit_location
        title_location = base
        image_location = [base[0], base[1] + 20 * self.zoom]
        text_location = [base[0], base[1] + 290 * self.zoom]

        write(self.screen, unit.name.replace("_", " "), title_location, self.interface.fonts["normal"])
        self.screen.blit(pic, image_location)

        lines = self.get_unit_lines(unit)
        if attack_hint:
            lines += attack_hint
        line_length = 45
        show_lines(self.screen, lines, line_length, self.interface.line_distances["small"], self.interface.fonts["small"], *text_location)

    def show_unit_upgrade_choice(self, unit, index):

        unit_pic = get_unit_pic(self.interface, unit)
        pic = get_image(unit_pic, self.upgrade_unit_dimensions)

        base = self.interface.upgrade_locations[index]
        title_location = base
        image_location = [base[0], base[1] + 20 * self.zoom]
        text_location = [base[0], base[1] + 160 * self.zoom]

        write(self.screen, unit.name, title_location, self.interface.fonts["normal"])
        self.screen.blit(pic, image_location)

        lines = self.get_unit_lines(unit)
        line_length = 30
        show_lines(self.screen, lines, line_length, self.interface.line_distances["small"], self.interface.fonts["small"], *text_location)

    def draw_upgrade_options(self, unit):
        for i in range(2):
            upgraded_unit = unit.get_upgraded_unit_from_choice(i)
            self.show_unit_upgrade_choice(upgraded_unit, i)

    def draw_ask_about_ability(self, unit):
        self.clear()
        lines = ["Select ability:"]
        for i, ability in enumerate(unit.abilities):
            level = unit.abilities[ability]
            description_string = str(i + 1) + ": " + Ability.write[ability] + ": " + get_description(ability, level)
            lines += textwrap.wrap(description_string, self.interface.message_line_length)

        base = self.interface.ask_about_ability_location
        text_location = [base[0], base[1] + 160 * self.zoom]
        line_length = 80
        show_lines(self.screen, lines, line_length, self.interface.line_distances["small"], self.interface.fonts["small"], *text_location)

    def draw_unit_lower_right(self, action, color, index, base_x, base_y):

        if not action.is_attack():
            unit = action.unit.name
        elif index == 0:
            unit = action.unit.name
        else:
            unit = action.target_unit.name

        resize = 0.2 * self.zoom
        location = (base_x + (65 + index * 100) * self.zoom, base_y + 8 * self.zoom)
        unit_pic = get_unit_pic(self.interface, unit)
        unit_image = get_image(unit_pic)

        unit_image = pygame.transform.scale(unit_image, (int(self.interface.unit_width * resize),
                                            int(self.interface.unit_height * resize)))

        self.screen.blit(unit_image, location)

        draw_unit_box(self, location, color, resize)
