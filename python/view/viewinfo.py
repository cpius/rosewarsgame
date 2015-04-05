from view.view_display_library import *
import gamestate.battle as battle
from gamestate.gamestate_library import *
from game.game_library import prettify
from functools import total_ordering
from view.rounded_rect import AAfilledRoundedRect


@total_ordering
class BattleValues:
    def __init__(self, attack, defence, chance_of_push, chance_of_win):
        self.attack = attack
        self.defence = defence
        self.chance_of_push = chance_of_push
        self.chance_of_win = chance_of_win

    @staticmethod
    def show_chance(value):
        return str(round(value * 100, 1)) + "%"

    def show_chance_of_win(self):
        return self.show_chance(self.chance_of_win)

    def show_chance_of_push(self):
        return self.show_chance(self.chance_of_push)

    def __eq__(self, other):
        return self.chance_of_win == other.chance_of_win

    def __gt__(self, other):
        return self.chance_of_win > other.chance_of_win


class Viewinfo:

    def __init__(self, interface, screen, zoom):
        self.interface = interface
        self.screen = screen
        self.zoom = zoom
        self.unit_dimensions = (int(236 * zoom), int(271 * zoom))
        self.upgrade_unit_dimensions = (int(118 * zoom), int(135.5 * zoom))
        self.small_line_height = self.interface.line_distances["small"]
        self.small_font = self.interface.fonts["small"]

    def clear(self):
        pygame.draw.rect(self.screen, Color.Light_grey, self.interface.lower_right_rectangle)

    @staticmethod
    def get_unit_lines(unit):
        defence = unit.defence
        if unit.has(Effect.sabotaged):
            defence = 0
        lines = ["Attack: " + str(unit.attack) + "  Defence: " + str(defence)
                 + "  Range: " + str(unit.range) + "  Movement: " + str(unit.movement)]

        lines += [unit.type.name, ""]
        if unit.unit_level:
            lines += ["Level: " + str(unit.unit_level + 1), ""]

        dont_show = {State.used, State.recently_upgraded, State.experience, State.lost_extra_life, State.javelin_thrown,
                     Trait.attack_skill, Trait.defence_skill, Trait.range_skill, Trait.movement_skill, Trait.extra_life,
                     Trait.javelin}

        for attribute in set(unit.attributes) - dont_show:
            values = unit.attributes[attribute]
            if attribute in State:
                if unit.has(attribute):
                    lines.append(prettify(attribute.name))

            elif attribute in Trait or attribute in Ability:
                lines += [prettify(attribute.name) + ":", get_description(attribute, values.level), ""]

            elif attribute in Effect:
                lines += [prettify(attribute.name) + ":", get_description(attribute, values.level)]
                if values.duration == 1:
                    lines += ["Duration: " + str(values.duration) + " turn.", ""]
                else:
                    lines += ["Duration: " + str(values.duration) + " turns.", ""]

        if unit.has(Trait.extra_life):
            if unit.has(State.lost_extra_life):
                lines += ["No extra life", ""]
            else:
                lines += ["Has extra life", ""]

        if unit.has(Trait.javelin):
            if unit.has(State.javelin_thrown):
                lines += ["Javelin thrown", ""]
            else:
                lines += [prettify(Trait.javelin.name) + ":", get_description(Trait.javelin, 1), ""]

        return lines

    def show_battle_hint(self, gamestate, start_at, target_at):
        lines = self.get_battle_hint(gamestate, start_at, target_at)
        line_length = 45
        base = self.interface.show_unit_location
        text_location = [base[0], base[1] + 500 * self.zoom]
        show_lines(self.screen, lines, line_length, self.small_line_height, self.small_font, *text_location)

    def show_unit_zoomed(self, unit):

        unit_pic = get_unit_pic(self.interface, unit)
        pic = get_image(unit_pic, self.unit_dimensions)

        base = self.interface.show_unit_location
        title_location = base
        image_location = [base[0], base[1] + 25 * self.zoom]
        text_location = [base[0], base[1] + 290 * self.zoom]

        write(self.screen, unit.pretty_name, title_location, self.interface.fonts["normal"])
        self.screen.blit(pic, image_location)

        lines = self.get_unit_lines(unit)
        line_length = 45
        show_lines(self.screen, lines, line_length, self.small_line_height, self.small_font, *text_location)

    def show_unit_upgrade_choice(self, unit, index):

        unit_pic = get_unit_pic(self.interface, unit)
        pic = get_image(unit_pic, self.upgrade_unit_dimensions)

        base = self.interface.upgrade_locations[index]
        title_location = base
        image_location = [base[0], base[1] + 25 * self.zoom]
        text_location = [base[0], base[1] + 160 * self.zoom]

        write(self.screen, unit.pretty_name, title_location, self.interface.fonts["normal"])
        self.screen.blit(pic, image_location)

        lines = self.get_unit_lines(unit)
        line_length = 25
        show_lines(self.screen, lines, line_length, self.small_line_height, self.small_font, *text_location)

    def draw_upgrade_options(self, unit):
        for i in range(2):
            upgrade = unit.get_upgrade(i)
            if upgrade in Unit:
                upgraded_unit = unit.get_upgraded_unit_from_choice(i)
                self.show_unit_upgrade_choice(upgraded_unit, i)
            else:
                base = self.interface.upgrade_locations[i]
                (attribute, values), = upgrade.items()
                lines = [prettify(attribute.name) + ":" + get_description(attribute, values.level)]
                line_length = 25
                show_lines(self.screen, lines, line_length, self.small_line_height, self.small_font, *base)

    def draw_ask_about_ability(self, unit):
        self.clear()
        lines = ["Select ability:"]
        for i, ability in enumerate(unit.abilities):
            level = unit.attributes[ability].level
            description_string = str(i + 1) + ": " + ability.name + ": " + get_description(ability, level)
            lines += textwrap.wrap(description_string, self.interface.message_line_length)

        base = self.interface.ask_about_ability_location
        text_location = [base[0], base[1] + 160 * self.zoom]
        line_length = 80
        show_lines(self.screen, lines, line_length, self.small_line_height, self.small_font, *text_location)

    @staticmethod
    def get_battle_hint(gamestate, start_at, target_at):
        actions = [action for action in gamestate.get_actions({"target_at": target_at, "start_at": start_at})]

        if actions[0].is_ability:
            return ""

        battle_values_list = []

        for action in actions:
            attack = battle.get_attack(action, gamestate)
            defence = battle.get_defence(action, attack, gamestate)
            attack, defence = min(attack, 6), min(defence, 6)
            chance_of_push = (attack / 6) * (defence/6) if action.is_push else 0
            chance_of_win = attack * (6 - defence) / 36
            battle_values_list.append(BattleValues(attack, defence, chance_of_push, chance_of_win))

        best_battle = max(battle_values_list)
        worst_battle = min(battle_values_list)
        battle_hint = ["Battle hint:"]
        if best_battle == worst_battle:
            battle_hint += ["Attack: " + str(best_battle.attack),
                            "Defence: " + str(best_battle.defence),
                            "Chance of win: " + best_battle.show_chance_of_win()]

            if best_battle.chance_of_push > 0:
                battle_hint += ["Chance of push: " + best_battle.show_chance_of_push]

        else:
            if worst_battle.attack == best_battle.attack:
                battle_hint += ["Attack: " + str(worst_battle.attack)]
            else:
                battle_hint += ["Attack: " + str(worst_battle.attack) + " – " + str(best_battle.attack)]

            if worst_battle.defence == best_battle.defence:
                battle_hint += ["Defence: " + str(worst_battle.defence)]
            else:
                battle_hint += ["Defence: " + str(worst_battle.defence) + " – " + str(best_battle.defence)]

            battle_hint += ["Chance of win: " + worst_battle.show_chance_of_win() + " – " +
                            best_battle.show_chance_of_win()]

            if best_battle.chance_of_push > 0:
                battle_hint += ["Chance of push: " + worst_battle.show_chance_of_push + " – " +
                                best_battle.show_chance_of_push()]

        return battle_hint

    def draw_pass_action_button(self):
        area = self.interface.pass_action_area
        draw_rounded_rectangle_from_area(self.screen, area)
        write(self.screen, "Pass action", (area[0][0] + 9, area[0][1] + 4), self.interface.fonts["normal"])
