from __future__ import division
import pygame
import sys
from pygame.locals import *
import setup
from gamestate_module import Gamestate
import os
import settings
import shutil
import ai_methods
from player import Player
from action import Action


class Controller(object):
    def new_game(self, view):
        self.view = view

        self.action_index = 1

        player1 = Player("Green")
        player2 = Player("Red")

        player1.ai_name = settings.player1_ai
        player2.ai_name = settings.player2_ai

        player1_units, player2_units = setup.get_start_units()

        self.gamestate = Gamestate(player1, player1_units, player2, player2_units)

        self.gamestate.initialize_turn()
        self.gamestate.initialize_action()

        self.gamestate.set_actions_remaining(1)

        if os.path.exists("./replay"):
            shutil.rmtree('./replay')

        os.makedirs("./replay")

        self.run_game()

    def trigger_artificial_intelligence(self):
        print "turn", self.gamestate.turn
        print "action", 3 - self.gamestate.get_actions_remaining()
        print

        action = self.gamestate.current_player().ai.select_action(self.gamestate)

        if action:
            self.perform_action(action)
        else:
            self.gamestate.turn_shift()
            self.gamestate.recalculate_special_counters()
            self.view.draw_game(self.gamestate)

        if hasattr(self.gamestate.current_player(), "extra_action"):
            extra_action = self.gamestate.current_player().ai.select_action(self.gamestate)
            self.perform_action(extra_action)
    def run_game(self):

        self.gamestate.set_ais()

        pygame.time.set_timer(USEREVENT + 1, 1000)
        start_position = None
        end_position = None

        self.recalculate_special_counters()
        self.view.draw_game(self.gamestate)

        while True:
            for event in pygame.event.get():

                if event.type == USEREVENT + 1:

                    if self.gamestate.current_player().ai_name != "Human":

                        self.trigger_artificial_intelligence()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = self.view.get_position_from_mouse_click(event.pos)

                    if not start_position and (x, y) in self.gamestate.units[0]:
                        print "Start at", (x, y)
                        start_position = (x, y)
                        selected_unit = self.gamestate.units[0][start_position]

                    elif start_position \
                        and not end_position \
                        and ((x, y) in self.gamestate.units[1]
                             or (x, y) in self.gamestate.units[0]) and selected_unit.abilities:
                        print "Ability", (x, y)
                        if len(selected_unit.abilities) > 1:
                            index = self.get_input_abilities(selected_unit)
                            action = Action(start_position,
                                            start_position,
                                            (x, y),
                                            False,
                                            False,
                                            True,
                                            selected_unit.abilities[index])
                        else:
                            action = Action(start_position,
                                            start_position,
                                            (x, y),
                                            False,
                                            False,
                                            True,
                                            selected_unit.abilities[0])
                        self.perform_action(action)
                        start_position = None
                        end_position = None

                    elif start_position and not end_position and (x, y) in self.gamestate.units[1] and selected_unit.range > 1:
                        print "Attack", (x, y)
                        action = Action(start_position, start_position, (x, y), True, False)
                        self.perform_action(action)
                        start_position = None
                        end_position = None

                    elif start_position and not end_position and (x, y) in self.gamestate.units[1]:
                        print "Attack-Move", (x, y)

                        if hasattr(self.gamestate.current_player(), "extra_action"):
                            all_actions = self.gamestate.get_actions()
                        else:
                            all_actions = self.gamestate.get_actions()

                        action = None

                        for possible_action in all_actions:
                            if possible_action.start_position == start_position \
                                    and possible_action.attack_position == (x, y) \
                                    and possible_action.move_with_attack:
                                if possible_action.end_position == start_position:
                                    action = possible_action
                                    break
                                action = possible_action

                        if not action:
                            print "Action not possible"
                            start_position = None
                            end_position = None
                        else:
                            self.perform_action(action)
                            start_position = None
                            end_position = None

                    elif start_position and not end_position:
                        print "Stop at", (x, y)
                        end_position = (x, y)

                    elif start_position and end_position and (x, y) in self.gamestate.units[1]:
                        print "Attack-Move", (x, y)
                        action = Action(start_position, end_position, (x, y), True, False)
                        self.perform_action(action)
                        start_position = None
                        end_position = None

                    elif start_position and end_position and (x, y) not in self.gamestate.units[1]:
                        print "Move to", (x, y)
                        action = Action(start_position, (x, y), None, False, False)
                        self.perform_action(action)
                        start_position = None
                        end_position = None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    x, y = self.view.get_position_from_mouse_click(event.pos)

                    if start_position and (x, y) not in self.gamestate.units[1]:
                        print "Move to", (x, y)
                        action = Action(start_position, (x, y), None, False, False)
                        self.perform_action(action)
                        start_position = None
                        end_position = None

                    if start_position and (x, y) in self.gamestate.units[1]:
                        action = Action(start_position, (x, y), (x, y), True, False)
                        chance_of_win = ai_methods.chance_of_win(selected_unit, self.gamestate.units[1][(x, y)], action)
                        print "Chance of win", round(chance_of_win * 100), "%"
                        start_position = None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    x, y = self.view.get_position_from_mouse_click(event.pos)

                    if not start_position:
                        self.show_unit((x, y))

                    elif start_position and not end_position and (x, y) in self.gamestate.units[1]:
                        print "Attack", (x, y)

                        if hasattr(self.gamestate.current_player(), "extra_action"):
                            all_actions = self.gamestate.get_actions()
                        else:
                            all_actions = self.gamestate.get_actions()

                        action = None

                        for possible_action in all_actions:
                            if possible_action.start_position == start_position \
                                    and possible_action.attack_position == (x, y) \
                                    and not possible_action.move_with_attack:

                                if possible_action.end_position == start_position:
                                    action = possible_action
                                    break
                                action = possible_action

                        if not action:
                            print "Action not possible"
                            start_position = end_position = None
                        else:
                            self.perform_action(action)
                            start_position = None
                            end_position = None

                    elif start_position and end_position and (x, y) in self.gamestate.units[1]:
                        print "Attack", (x, y)
                        action = Action(start_position, end_position, (x, y), True, False)
                        self.perform_action(action)
                        start_position = None
                        end_position = None

                if event.type == KEYDOWN and event.key == K_p:
                    print "paused"
                    self.pause()

                if event.type == KEYDOWN and event.key == K_a:
                    print
                    print "Possible actions:"
                    if hasattr(self.gamestate.current_player(), "extra_action"):
                        actions = self.gamestate.get_actions()
                        for action in actions:
                            print action
                    else:
                        actions = self.gamestate.get_actions()
                        for action in actions:
                            print action
                    print

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    print "move cleared"
                    start_position, end_position, selected_unit = None, None, None

                elif event.type == KEYDOWN and self.command_q_down(event.key):
                    self.exit_game()

                elif event.type == QUIT:
                    self.exit_game()

                pygame.display.flip()

    def exit_game(self):
        sys.exit()

    def get_input_counter(self, unit):
        self.view.draw_ask_about_counter(unit.name)

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_a:
                    unit.attack_counters += 1
                    return

                if event.type == KEYDOWN and event.key == K_d:
                    unit.defence_counters += 1
                    return

    def get_input_abilities(self, unit):
        self.view.draw_ask_about_ability(unit.abilities[0], unit.abilities[1])

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_1:
                    return 0

                if event.type == KEYDOWN and event.key == K_2:
                    return 1

    def recalculate_special_counters(self):
        for unit in self.gamestate.units[0].itervalues():
            self.add_yellow_counters(unit)
            self.add_blue_counters(unit)

        for unit in self.gamestate.units[1].itervalues():
            self.add_yellow_counters(unit)
            self.add_blue_counters(unit)

    def add_yellow_counters(self, unit):
        if hasattr(unit, "extra_life"):
            unit.yellow_counters = 1
        else:
            unit.yellow_counters = 0

    def add_blue_counters(self, unit):
        unit.blue_counters = 0
        if hasattr(unit, "frozen"):
            unit.blue_counters = unit.frozen
        if hasattr(unit, "attack_frozen"):
            unit.blue_counters = unit.attack_frozen
        if hasattr(unit, "just_bribed"):
            unit.blue_counters = 1

    def pause(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit_game()
                elif event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def add_counters(self, units):
        for unit in units.values():
            if unit.xp == 2:
                if unit.defence + unit.defence_counters == 4:
                    unit.attack_counters += 1
                else:
                    self.get_input_counter(unit)

                unit.xp = 0

    def perform_action(self, action):

        if hasattr(self.gamestate.current_player(), "extra_action"):
            all_actions = self.gamestate.get_actions()
        else:
            all_actions = self.gamestate.get_actions()

        matching_actions = 0
        for possible_action in all_actions:
            if action == possible_action:
                matching_actions += 1
                action = possible_action

        if matching_actions == 0:
            print "Action not allowed"
            return

        elif matching_actions > 1:
            print "Action ambiguous"
            return

        self.view.draw_action(action)
        pygame.time.delay(settings.pause_for_animation)

        self.gamestate.do_action(action)

        self.save_game()

        if settings.show_full_battle_result:
            print action.full_string()
        else:
            print action.string_with_outcome()
        print

        if hasattr(self.gamestate.current_player(), "won"):
            self.game_end(self.gamestate.current_player())
            return

        if self.gamestate.current_player().ai_name == "Human":
            self.add_counters(self.gamestate.units[0])
        else:
            self.gamestate.current_player().ai.add_counters(self.gamestate)

        self.recalculate_special_counters()
        self.view.draw_game(self.gamestate)

        self.gamestate.initialize_action()

        if (self.gamestate.get_actions_remaining() < 1 or len(all_actions) == 1) \
                and not hasattr(self.gamestate.current_player(), "extra_action"):
            self.gamestate.turn_shift()

        self.recalculate_special_counters()
        self.view.draw_game(self.gamestate)

        if hasattr(self.gamestate.current_player(), "extra_action"):
            print self.gamestate.current_player().color, "extra action"
        else:
            print self.gamestate.current_player().color

    def show_unit(self, position):

        unit = color = None
        if position in self.gamestate.units[0]:
            unit = self.gamestate.units[0][position]
            color = self.gamestate.current_player().color
        if position in self.gamestate.units[1]:
            unit = self.gamestate.units[1][position]
            color = self.gamestate.players[1].color

        if unit:
            print
            print unit
            for attribute, value in unit.__dict__.items():
                if attribute not in ["name", "yellow_counters", "blue_counters", "pic",
                                     "color", "range", "movement"]:
                    if value:
                        print attribute, value

            self.view.show_unit_zoomed(unit.name, color)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == KEYDOWN:
                        self.recalculate_special_counters()
                        self.view.draw_game(self.gamestate)
                        return

    def save_game(self):
        name = str(self.action_index) + ". " \
            + self.gamestate.current_player().color \
            + ", " \
            + str(self.gamestate.turn) \
            + "." \
            + str(2 - self.gamestate.get_actions_remaining())
        self.view.save_screenshot(name)

        self.action_index += 1

    def command_q_down(self, key):
        return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)

    def game_end(self, player):
        self.view.draw_game_end(player.color)
        self.pause()
        self.exit_game()
