from __future__ import division
from viewcommon import *
from collections import namedtuple
import battle
from operator import attrgetter


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
        lines = ["Attack: " + str(unit.attack) + "  Defence: " + str(defence)
                 + "  Range: " + str(unit.range) + "  Movement: " + str(unit.movement), ""]

        level = unit.get_unit_level()
        if level:
            lines.append("Level: " + str(level + 1))
            lines.append("")

        if unit.zoc:
            lines.append("Zone of control against: " + ", ".join(unit_type.name for unit_type in unit.zoc))
            lines.append("")

        if unit.attack_bonuses:
            for unit_type, value in unit.attack_bonuses.items():
                lines.append("+" + str(value) + " Attack against " + unit_type.name)
                lines.append("")

        if unit.defence_bonuses:
            for unit_type, value in unit.defence_bonuses.items():
                if unit_type == Type.War_Machine:
                    lines.append("+" + str(value) + " Defence against War Machines")
                else:
                    lines.append("+" + str(value) + " Defence against " + unit_type.name)
                lines.append("")

        for trait in unit.get_traits():
            if trait not in [Trait.attack_skill, Trait.defence_skill, Trait.range_skill, Trait.movement_skill, Trait.extra_life]:
                level = unit.get_level(trait)
                if level == 1:
                    lines.append(trait.name + ":")
                    lines.append(trait_descriptions[trait.name][1])
                    lines.append("")
                elif level > 1:
                    lines.append(trait.name + ", level " + str(level) + ":")
                    lines.append(trait_descriptions[trait.name][1])
                    lines.append("")

        for ability in unit.get_abilities():
            level = unit.get_level(ability)
            if level == 1:
                lines.append(ability.name + ":")
                lines.append(get_ability_description(ability, 1))
                lines.append("")
            else:
                lines.append(ability.name + ", " + "level " + str(level) + ":")
                lines.append(get_ability_description(ability, level))
                lines.append("")

        for state in unit.get_states():
            value = unit.get_state(state)
            if value and state not in [State.used, State.recently_upgraded, State.experience, State.lost_extra_life,
                                       State.javelin_thrown]:
                lines.append(state.name + ": " + str(value))

        for effect in unit.get_effects():
            level = unit.get_level(effect)
            duration = unit.get_level(effect)
            if level == 1:
                lines.append(effect.name + ": " + str(duration))
            else:
                lines.append(effect.name + ", level " + str(level) + ": " + str(duration))
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

    def show_battle_hint(self, gamestate, start_at, target_at):
        lines = self.get_battle_hint(gamestate, start_at, target_at)
        line_length = 45
        base = self.interface.show_unit_location
        text_location = [base[0], base[1] + 500 * self.zoom]
        show_lines(self.screen, lines, line_length, self.interface.line_distances["small"], self.interface.fonts["small"], *text_location)

    def show_unit_zoomed(self, unit):

        unit_pic = get_unit_pic(self.interface, unit)
        pic = get_image(unit_pic, self.unit_dimensions)

        base = self.interface.show_unit_location
        title_location = base
        image_location = [base[0], base[1] + 20 * self.zoom]
        text_location = [base[0], base[1] + 290 * self.zoom]

        write(self.screen, unit.name.replace("_", " "), title_location, self.interface.fonts["normal"])
        self.screen.blit(pic, image_location)

        lines = self.get_unit_lines(unit)
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
        for i, ability in enumerate(unit.get_abilities()):
            level = unit.attributes[ability].level
            description_string = str(i + 1) + ": " + ability.name + ": " + get_ability_description(ability, level)
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

    @staticmethod
    def get_battle_hint(gamestate, start_at, target_at):
            actions = [action for action in gamestate.get_actions() if action.target_at == target_at
                       and action.start_at == start_at]

            if actions[0].is_ability():
                return ""

            BattleValues = namedtuple("BattleValues", ["attack", "defence", "chance_of_win", "chance_of_push"])
            battle_values_list = []

            for action in actions:
                player_unit = gamestate.player_units[start_at]
                if player_unit.name == Unit.Assassin:
                    attack = 6
                    defence = 2
                else:
                    attack = battle.get_attack(action, gamestate)
                    defence = battle.get_defence(action, attack, gamestate)
                    attack, defence = min(attack, 6), min(defence, 6)

                chance_of_push = (attack / 6) * (defence/6) if action.is_push() else 0
                chance_of_win = attack * (6 - defence) / 36
                battle_values_list.append(BattleValues(attack=attack, defence=defence, chance_of_push=chance_of_push,
                                                       chance_of_win=chance_of_win))

            best_battle = max(battle_values_list, key=attrgetter("chance_of_win"))
            worst_battle = min(battle_values_list, key=attrgetter("chance_of_win"))
            battle_hint = ["Battle hint:"]
            if best_battle == worst_battle:
                battle_hint += ["Attack: " + str(best_battle.attack),
                                "Defence: " + str(best_battle.defence),
                                "Chance of win: " + str(round(best_battle.chance_of_win * 100, 1)) + "%"]

                if best_battle.chance_of_push > 0:
                    battle_hint += ["Chance of push: " + str(round(best_battle.chance_of_push * 100, 1)) + "%"]

            else:
                if worst_battle.attack == best_battle.attack:
                    battle_hint += ["Attack: " + str(worst_battle.attack)]
                else:
                    battle_hint += ["Attack: " + str(worst_battle.attack) + " – " + str(best_battle.attack)]

                if worst_battle.defence == best_battle.defence:
                    battle_hint += ["Defence: " + str(worst_battle.defence)]
                else:
                    battle_hint += ["Defence: " + str(worst_battle.defence) + " – " + str(best_battle.defence)]

                battle_hint += ["Chance of win: " + str(round(worst_battle.chance_of_win * 100, 1)) + "%" + " – " + \
                               str(round(best_battle.chance_of_win * 100, 1)) + "%"]

                if best_battle.chance_of_push > 0:
                    battle_hint += ["Chance of push: " + str(round(worst_battle.chance_of_push * 100, 1)) + "%" + " – " +
                                    str(round(best_battle.chance_of_push * 100, 1)) + "%"]

            return battle_hint
