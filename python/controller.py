from __future__ import division
import pygame
import sys
from pygame.locals import *
import setup
from gamestate_module import Gamestate
import os
import settings
import shutil
from player import Player
from action import Action, MoveOrStay
import units as units_module
import json
from json import JSONEncoder
import datetime
from client import Client
from action_getter import add_unit_references
from game import Game
from outcome import Outcome, SubOutcome


class Controller(object):
    def __init__(self, view):
        self.view = view
        self.game = None
        self.client = None
        self.action_index = 1

    @classmethod
    def new_game(cls, view):
        controller = Controller(view)

        players = [Player("Green", settings.player1_ai), Player("Red", settings.player2_ai)]

        player1_units, player2_units = setup.get_start_units()
        gamestate = Gamestate(player1_units, player2_units, 1)

        controller.game = Game(players, gamestate)

        controller.game.gamestate.initialize_turn()
        controller.game.gamestate.initialize_action()

        controller.game.gamestate.actions_remaining = 1

        if os.path.exists("./replay"):
            shutil.rmtree('./replay')

        os.makedirs("./replay")

        controller.clear_move()

        return controller

    @classmethod
    def from_network(cls, view, game_id, player):
        controller = cls(view)

        controller.game_id = game_id
        controller.client = Client(game_id)

        controller.gamestate = controller.client.get_gamestate()
        controller.gamestate.set_network_player(player)
        controller.action_index = 1

        controller.clear_move()

        return controller

    def trigger_network_player(self):
        action, outcome = self.client.select_action(self.gamestate.action_number)
        add_unit_references(self.gamestate, action)

        print "received action from network: " + str(action)

        self.perform_action(action, outcome)

        if hasattr(self.gamestate.current_player(), "extra_action"):
            extra_action, extra_outcome = self.client.select_action(self.gamestate)
            self.perform_action(extra_action, extra_outcome)

    def trigger_artificial_intelligence(self):

        action = self.game.current_player().ai.select_action(self.game)

        if action:
            self.perform_action(action)
        else:
            self.game.shift_turn()
            self.game.gamestate.recalculate_special_counters()
            self.view.draw_game(self.game)

        if getattr(self.game.gamestate, "extra_action"):
            extra_action = self.game.current_player().ai.select_action(self.game.gamestate)
            self.perform_action(extra_action)

    def left_click(self, position):
        if self.deselecting_active_unit(position):
            self.clear_move()
            self.view.draw_game(self.game)

        elif self.selecting_active_unit(position):
            self.start_position = position
            self.selected_unit = self.game.gamestate.player_units()[self.start_position]
            illustrate_actions = (action for action in self.game.gamestate.get_actions() if \
                                  action.start_position == position)
            self.view.draw_game(self.game, position, illustrate_actions)

        elif self.selecting_ability_target(position):
            if len(self.selected_unit.abilities) > 1:
                index = self.get_input_abilities(self.selected_unit)

                ability = self.selected_unit.abilities[index]
            else:
                ability = self.selected_unit.abilities[0]

            action = Action(self.start_position, ability_position=position, ability=ability)
            self.perform_action(action)

        elif self.selecting_ranged_target(position):
            action = Action(self.start_position, attack_position=position, move_with_attack=MoveOrStay.STAY)
            self.perform_action(action)

        elif self.selecting_melee_target(position):

            possible_actions = [action for action in self.game.gamestate.get_actions() if
                                action.start_position == self.start_position and action.attack_position == position and
                                not action.is_move_with_attack()]

            if not possible_actions:
                self.view.draw_message("Action not possible")
                self.clear_move()
                self.view.draw_game(self.game)
                return

            if len(possible_actions) == 1:
                action = possible_actions[0]
            else:
                self.view.draw_game(self.game)
                action = self.pick_action_end_position(possible_actions)

            self.perform_action(action)

        elif self.selecting_move(position):
            action = Action(self.start_position, end_position=position)
            self.perform_action(action)

    def pick_action_end_position(self, possible_actions):

        end_positions = [action.end_position for action in possible_actions]

        self.view.shade_positions(end_positions)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = self.view.get_position_from_mouse_click(event.pos)

                    if event.button == 1:
                        for action in possible_actions:
                            if position == action.end_position:
                                return action

                elif event.type == QUIT:
                    self.exit_game()

    def right_click(self, position):
        if not self.start_position:
            self.show_unit(position)
        else:
            if position in self.game.gamestate.opponent_units():
                self.show_attack(position)

    def clear_move(self):
        self.start_position = self.end_position = self.selected_unit = None

    def run_game(self):

        self.game.gamestate.set_available_actions()

        self.game.gamestate.recalculate_special_counters()
        self.view.draw_game(self.game)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = self.view.get_position_from_mouse_click(event.pos)

                    if event.button == 1:
                        self.left_click(position)
                    elif event.button == 3:
                        self.right_click(position)

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.clear_move()
                    self.view.draw_game(self.game)

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

                elif event.type == QUIT:
                    self.exit_game()

    def get_input_upgrade(self, unit):
        self.view.draw_upgrade_options(unit)

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_1:
                    return 0
                if event.type == KEYDOWN and event.key == K_2:
                    return 1

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        if within(event.pos, self.view.interface.upgrade_1_area):
                            return 0
                        elif within(event.pos, self.view.interface.upgrade_2_area):
                            return 1

                elif event.type == QUIT:
                    self.exit_game()

    def get_input_abilities(self, unit):
        self.view.draw_ask_about_ability(unit)

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_1:
                    return 0

                if event.type == KEYDOWN and event.key == K_2:
                    return 1

                elif event.type == QUIT:
                    self.exit_game()

    def ask_about_move_with_attack(self, action):

        self.view.draw_ask_about_move_with_attack(action.attack_position)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = self.view.get_position_from_mouse_click(event.pos)

                    if event.button == 1:
                        if position == action.attack_position:
                            return True
                        if position == action.end_position:
                            return False

                elif event.type == QUIT:
                    self.exit_game()

    def pause(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit_game()
                elif event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def upgrade_units(self, units):
        for pos, unit in units.items():
            if unit.xp == unit.xp_to_upgrade:
                choice = self.get_input_upgrade(unit)
                units[pos] = getattr(units_module, unit.upgrades[choice].replace(" ", "_"))()

    def perform_action(self, action, outcome=None):
        self.draw_action = True

        self.view.draw_game(self.game)

        all_actions = self.game.gamestate.get_actions()

        matching_actions = 0
        for possible_action in all_actions:
            if action == possible_action:
                matching_actions += 1

        if matching_actions == 0:
            self.clear_move()
            self.view.draw_game(self.game)
            self.view.draw_message("Action not allowed")
            return

        assert matching_actions <= 1
        move_with_attack = False

        if self.game.current_player().intelligence == "Human":

            add_unit_references(self.game.gamestate, action)

            if self.game.opponent_player().intelligence == "Network":
                outcome = self.client.send_action(action.to_document())
                action.ensure_outcome(outcome)

            outcome = self.game.do_action(action, outcome)

            self.view.draw_game(self.game)
            self.view.draw_action(action, outcome, self.game)

            if self.is_post_movement_possible(action, outcome):
                move_with_attack = self.ask_about_move_with_attack(action)

                if move_with_attack:
                    self.game.gamestate.update_final_position(action)

        else:
            outcome = self.game.do_action(action)
            self.view.draw_action(action, outcome, self.game, flip=True)

        if move_with_attack:
            self.view.draw_post_movement(action, self.game)

        self.save_game()

        if action.is_attack():
            if settings.pause_for_attack_until_click:
                self.pause()
            else:
                pygame.time.delay(settings.pause_for_animation_attack)
        else:
            pygame.time.delay(settings.pause_for_animation)

        if hasattr(self.game.current_player(), "won"):
            self.game_end(self.game.current_player())
            return

        if self.game.current_player().intelligence == "Human":
            self.view.draw_game(self.game)
            self.upgrade_units(self.game.gamestate.units[0])
        else:
            pass

        self.game.gamestate.recalculate_special_counters()
        self.view.draw_game(self.game)

        self.game.gamestate.initialize_action()
        if self.game.gamestate.turn_done():
            self.game.shift_turn()

        self.game.gamestate.recalculate_special_counters()
        self.view.draw_game(self.game)

        self.clear_move()

        print "Getting move. Current player is: " + self.game.current_player().intelligence

        if self.game.current_player().intelligence not in ["Human", "Network"]:
            self.trigger_artificial_intelligence()
        elif self.game.current_player().intelligence == "Network":
            self.trigger_network_player()

    def is_post_movement_possible(self, action, outcome):
        successful = outcome.for_position(action.attack_position) == SubOutcome.WIN
        return action.is_attack() and successful and action.unit.range == 1

    def show_attack(self, attack_position):
        action = Action(self.start_position, attack_position=attack_position)
        player_unit = self.game.gamestate.player_units()[self.start_position]
        opponent_unit = self.game.gamestate.opponent_units()[attack_position]
        self.view.show_attack(action, player_unit, opponent_unit)

        return

    def show_unit(self, position):

        unit = None
        if position in self.game.gamestate.units[0]:
            unit = self.game.gamestate.units[0][position]
        if position in self.game.gamestate.units[1]:
            unit = self.game.gamestate.units[1][position]

        if unit:
            self.view.show_unit_zoomed(unit)
            self.pause()
            self.view.draw_game(self.game)
            return

    def save_game(self):
        name = str(self.action_index) + ". " + self.game.current_player().color + ", " + str(self.game.turn) \
                                      + "." + str(2 - self.game.gamestate.get_actions_remaining())

        self.view.save_screenshot(name)

        with open("./replay/" + name + ".json", 'w') as file:
            file.write(json.dumps(self.game.gamestate.to_document(), cls=CustomJsonEncoder, indent=4))

        self.action_index += 1

    def command_q_down(self, key):
        return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)

    def game_end(self, player):
        self.view.draw_game_end(player.color)
        self.pause()
        self.exit_game()

    def selecting_active_unit(self, position):
        return not self.start_position and position in self.game.gamestate.player_units()

    def selecting_ability_target(self, position):
        return self.start_position and (
            position in self.game.gamestate.opponent_units() or position in self.game.gamestate.player_units()) and self.selected_unit.abilities

    def selecting_attack_target_unit(self, position):
        pass

    def selecting_attack_ranged_target(self, position):
        return self.start_position and position in self.game.gamestate.opponent_units() and \
               self.selected_unit.range > 1

    def deselecting_active_unit(self, position):
        return self.start_position and self.start_position == position

    def selecting_ranged_target(self, position):
        return self.start_position and position in self.game.gamestate.opponent_units() and \
               self.selected_unit.range > 1

    def selecting_melee_target(self, position):
        return self.start_position and position in self.game.gamestate.opponent_units() and \
               self.selected_unit.range == 1

    def selecting_move(self, position):
        return self.start_position and position not in self.game.gamestate.opponent_units()


def within(point, area):
    return area[0].y <= point[1] <= area[1].y and area[0].x <= point[0] <= area[1].x


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        return JSONEncoder.default(self, obj)
