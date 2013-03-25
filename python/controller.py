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
    def __init__(self, view):
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

        self.clear_move()

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

    def left_click(self, x, y):
        if self.start_position and self.start_position == (x, y):
            self.clear_move()
            self.view.draw_game(self.gamestate)

        elif not self.start_position and (x, y) in self.gamestate.units[0]:
            self.start_position = (x, y)
            self.selected_unit = self.gamestate.units[0][self.start_position]

            attack_positions = set()
            move_positions = set()
            ability_positions = set()
            for action in self.gamestate.available_actions:
                if action.start_position == (x, y):
                    if action.is_attack:
                        attack_positions.add(action.attack_position)
                    elif action.is_ability:
                        ability_positions.add(action.attack_position)
                    else:
                        move_positions.add(action.end_position)

            self.view.draw_game(self.gamestate, (x, y), attack_positions, ability_positions, move_positions)

        elif self.start_position \
            and not self.end_position \
            and ((x, y) in self.gamestate.units[1]
                 or (x, y) in self.gamestate.units[0]) and self.selected_unit.abilities:
            if len(self.selected_unit.abilities) > 1:
                index = self.get_input_abilities(self.selected_unit)
                action = Action(self.start_position,
                                self.start_position,
                                (x, y),
                                False,
                                False,
                                True,
                                self.selected_unit.abilities[index])
            else:
                action = Action(self.start_position,
                                self.start_position,
                                (x, y),
                                False,
                                False,
                                True,
                                self.selected_unit.abilities[0])
            self.perform_action(action)

        elif self.start_position and not self.end_position and (x, y) in self.gamestate.units[1] and self.selected_unit.range > 1:
            action = Action(self.start_position, self.start_position, (x, y), True, False)
            self.perform_action(action)

        elif self.start_position and not self.end_position and (x, y) in self.gamestate.units[1]:

            if hasattr(self.gamestate.current_player(), "extra_action"):
                all_actions = self.gamestate.get_actions()
            else:
                all_actions = self.gamestate.get_actions()

            action = None

            for possible_action in all_actions:
                if possible_action.start_position == self.start_position \
                        and possible_action.attack_position == (x, y) \
                        and possible_action.move_with_attack:
                    if possible_action.end_position == self.start_position:
                        action = possible_action
                        break
                    action = possible_action

            if not action:
                print "Action not possible"
                self.clear_move()
            else:
                self.perform_action(action)

        elif self.start_position and not self.end_position:
            self.end_position = (x, y)

        elif self.start_position and self.end_position and (x, y) in self.gamestate.units[1]:
            action = Action(self.start_position, self.end_position, (x, y), True, False)
            self.perform_action(action)

        elif self.start_position and self.end_position and (x, y) not in self.gamestate.units[1]:
            action = Action(self.start_position, (x, y), None, False, False)
            self.perform_action(action)

    def right_click(self, x, y):
        if self.start_position and (x, y) not in self.gamestate.units[1]:
            print "Move to", (x, y)
            action = Action(self.start_position, (x, y), None, False, False)
            self.perform_action(action)
        if self.start_position and (x, y) in self.gamestate.units[1]:
            action = Action(self.start_position, (x, y), (x, y), True, False)
            chance_of_win = ai_methods.chance_of_win(self.selected_unit, self.gamestate.units[1][(x, y)], action)
            print "Chance of win", round(chance_of_win * 100), "%"
            self.start_position = None

    def middle_click(self, x, y):
        if not self.start_position:
            self.show_unit((x, y))

        elif self.start_position and not self.end_position and (x, y) in self.gamestate.units[1]:
            print "Attack", (x, y)

            if hasattr(self.gamestate.current_player(), "extra_action"):
                all_actions = self.gamestate.get_actions()
            else:
                all_actions = self.gamestate.get_actions()

            action = None

            for possible_action in all_actions:
                if possible_action.start_position == self.start_position \
                        and possible_action.attack_position == (x, y) \
                        and not possible_action.move_with_attack:

                    if possible_action.end_position == self.start_position:
                        action = possible_action
                        break
                    action = possible_action

            if not action:
                print "Action not possible"
                self.clear_move()
            else:
                self.perform_action(action)

        elif self.start_position and self.end_position and (x, y) in self.gamestate.units[1]:
            print "Attack", (x, y)
            action = Action(self.start_position, self.end_position, (x, y), True, False)
            self.perform_action(action)

    def list_actions(self):
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

    def clear_move(self):
        self.start_position = self.end_position = self.selected_unit = None

    def run_game(self):

        self.gamestate.set_ais()
        self.gamestate.available_actions = self.gamestate.get_actions()

        self.gamestate.recalculate_special_counters()
        self.view.draw_game(self.gamestate)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.view.get_position_from_mouse_click(event.pos)

                    if event.button == 1:
                        self.left_click(x, y)
                    elif event.button == 2:
                        self.right_click(x, y)
                    elif event.button == 3:
                        self.middle_click(x, y)

                if event.type == KEYDOWN and event.key == K_p:
                    print "paused"
                    self.pause()

                if event.type == KEYDOWN and event.key == K_a:
                    self.list_actions()

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.clear_move()
                    self.view.draw_game(self.gamestate)

                elif event.type == KEYDOWN and self.command_q_down(event.key):
                    self.exit_game()

                elif event.type == QUIT:
                    self.exit_game()

                self.view.refresh()

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
            self.clear_move()
            return

        elif matching_actions > 1:
            print "Action ambiguous"
            self.clear_move()
            return

        self.gamestate.do_action(action)

        self.view.draw_action(action)

        self.save_game()

        pygame.time.delay(settings.pause_for_animation)

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

        self.gamestate.recalculate_special_counters()
        self.view.draw_game(self.gamestate)

        self.gamestate.initialize_action()

        if (self.gamestate.get_actions_remaining() < 1 or len(all_actions) == 1) \
                and not hasattr(self.gamestate.current_player(), "extra_action"):
            self.gamestate.turn_shift()

        self.gamestate.recalculate_special_counters()
        self.view.draw_game(self.gamestate)

        if hasattr(self.gamestate.current_player(), "extra_action"):
            print self.gamestate.current_player().color, "extra action"
        else:
            print self.gamestate.current_player().color

        self.clear_move()

        if self.gamestate.current_player().ai_name != "Human":
            self.trigger_artificial_intelligence()

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
                        self.gamestate.recalculate_special_counters()
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
